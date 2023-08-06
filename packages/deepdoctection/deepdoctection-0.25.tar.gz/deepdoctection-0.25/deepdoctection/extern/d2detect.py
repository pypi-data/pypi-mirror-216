# -*- coding: utf-8 -*-
# File: d2detect.py

# Copyright 2021 Dr. Janis Meyer. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
D2 GeneralizedRCNN model as predictor for deepdoctection pipeline
"""

from copy import copy
from pathlib import Path
from typing import Dict, List, Literal, Mapping, Optional, Sequence

from ..utils.detection_types import ImageType, Requirement
from ..utils.file_utils import (
    detectron2_available,
    get_detectron2_requirement,
    get_pytorch_requirement,
    pytorch_available,
)
from ..utils.settings import ObjectTypes, TypeOrStr, get_type
from ..utils.transform import InferenceResize
from .base import DetectionResult, ObjectDetector, PredictorBase
from .pt.ptutils import set_torch_auto_device

if pytorch_available():
    import torch
    import torch.cuda
    from torch import nn  # pylint: disable=W0611

if detectron2_available():
    from detectron2.checkpoint import DetectionCheckpointer
    from detectron2.config import CfgNode, get_cfg  # pylint: disable=W0611
    from detectron2.layers import batched_nms
    from detectron2.modeling import GeneralizedRCNN, build_model  # pylint: disable=W0611
    from detectron2.structures import Instances  # pylint: disable=W0611


def _d2_post_processing(
    predictions: Dict[str, "Instances"], nms_thresh_class_agnostic: float
) -> Dict[str, "Instances"]:
    """
    D2 postprocessing steps, so that detection outputs are aligned with outputs of other packages (e.g. Tensorpack).
    Apply a class agnostic NMS.

    :param predictions: Prediction outputs from the model.
    :param nms_thresh_class_agnostic: Nms being performed over all class predictions
    :return: filtered predictions outputs
    """
    instances = predictions["instances"]
    class_masks = torch.ones(instances.pred_classes.shape, dtype=torch.uint8)
    keep = batched_nms(instances.pred_boxes.tensor, instances.scores, class_masks, nms_thresh_class_agnostic)
    fg_instances_keep = instances[keep]
    return {"instances": fg_instances_keep}


def d2_predict_image(
    np_img: ImageType,
    predictor: "nn.Module",
    preproc_short_edge_size: int,
    preproc_max_size: int,
    nms_thresh_class_agnostic: float,
) -> List[DetectionResult]:
    """
    Run detection on one image, using the D2 model callable. It will also handle the preprocessing internally which
    is using a custom resizing within some bounds.

    :param np_img: ndarray
    :param predictor: torch nn module implemented in Detectron2
    :param preproc_short_edge_size: the short edge to resize to
    :param preproc_max_size: upper bound of one edge when resizing
    :param nms_thresh_class_agnostic: class agnostic nms threshold
    :return: list of DetectionResult
    """
    height, width = np_img.shape[:2]
    resizer = InferenceResize(preproc_short_edge_size, preproc_max_size)
    resized_img = resizer.get_transform(np_img).apply_image(np_img)
    image = torch.as_tensor(resized_img.astype("float32").transpose(2, 0, 1))

    with torch.no_grad():
        inputs = {"image": image, "height": height, "width": width}
        predictions = predictor([inputs])[0]
        predictions = _d2_post_processing(predictions, nms_thresh_class_agnostic)
    instances = predictions["instances"]
    results = [
        DetectionResult(
            box=instances[k].pred_boxes.tensor.tolist()[0],
            score=instances[k].scores.tolist()[0],
            class_id=instances[k].pred_classes.tolist()[0],
        )
        for k in range(len(instances))
    ]
    return results


class D2FrcnnDetector(ObjectDetector):
    """
    D2 Faster-RCNN implementation with all the available backbones, normalizations throughout the model
    as well as FPN, optional Cascade-RCNN and many more.

    Currently, masks are not included in the data model.

    There are no adjustment to the original implementation of Detectron2. Only one post-processing step is followed by
    the standard D2 output that takes into account of the situation that detected objects are disjoint. For more infos
    on this topic, see <https://github.com/facebookresearch/detectron2/issues/978> .

        config_path = ModelCatalog.get_full_path_configs("dd/d2/item/CASCADE_RCNN_R_50_FPN_GN.yaml")
        weights_path = ModelDownloadManager.maybe_download_weights_and_configs("item/d2_model-800000-layout.pkl")
        categories = ModelCatalog.get_profile("item/d2_model-800000-layout.pkl").categories

        d2_predictor = D2FrcnnDetector(config_path,weights_path,categories,device="cpu")

        detection_results = d2_predictor.predict(bgr_image_np_array)
    """

    def __init__(
        self,
        path_yaml: str,
        path_weights: str,
        categories: Mapping[str, TypeOrStr],
        config_overwrite: Optional[List[str]] = None,
        device: Optional[Literal["cpu", "cuda"]] = None,
        filter_categories: Optional[Sequence[TypeOrStr]] = None,
    ):
        """
        Set up the predictor.

        The configuration of the model uses the full stack of build model tools of D2. For more information
        please check <https://detectron2.readthedocs.io/en/latest/tutorials/models.html#build-models-from-yacs-config>.

        :param path_yaml: The path to the yaml config. If the model is built using several config files, always use
                          the highest level .yaml file.
        :param path_weights: The path to the model checkpoint.
        :param categories: A dict with key (indices) and values (category names). Index 0 must be reserved for a
                           dummy 'BG' category. Note, that this convention is different from the builtin D2 framework,
                           where models in the model zoo are trained with 'BG' class having the highest index.
        :param config_overwrite:  Overwrite some hyperparameters defined by the yaml file with some new values. E.g.
                                 ["OUTPUT.FRCNN_NMS_THRESH=0.3","OUTPUT.RESULT_SCORE_THRESH=0.6"].
        :param device: "cpu" or "cuda". If not specified will auto select depending on what is available
        :param filter_categories: The model might return objects that are not supposed to be predicted and that should
                                  be filtered. Pass a list of category names that must not be returned
        """

        self.name = "_".join(Path(path_weights).parts[-3:])
        self._categories_d2 = self._map_to_d2_categories(copy(categories))
        if config_overwrite is None:
            config_overwrite = []
        self.path_weights = path_weights
        d2_conf_list = ["MODEL.WEIGHTS", path_weights]
        for conf in config_overwrite:
            key, val = conf.split("=", maxsplit=1)
            d2_conf_list.extend([key, val])

        self.path_yaml = path_yaml
        self.categories = copy(categories)  # type: ignore
        self.config_overwrite = config_overwrite
        if device is not None:
            self.device = device
        else:
            self.device = set_torch_auto_device()
        if filter_categories:
            filter_categories = [get_type(cat) for cat in filter_categories]
        self.filter_categories = filter_categories
        self.cfg = self._set_config(path_yaml, d2_conf_list, device)
        self.d2_predictor = D2FrcnnDetector.set_model(self.cfg)
        self._instantiate_d2_predictor()

    @staticmethod
    def _set_config(
        path_yaml: str, d2_conf_list: List[str], device: Optional[Literal["cpu", "cuda"]] = None
    ) -> "CfgNode":
        cfg = get_cfg()
        # additional attribute with default value, so that the true value can be loaded from the configs
        cfg.NMS_THRESH_CLASS_AGNOSTIC = 0.1
        cfg.merge_from_file(path_yaml)
        cfg.merge_from_list(d2_conf_list)
        if not torch.cuda.is_available() or device == "cpu":
            cfg.MODEL.DEVICE = "cpu"
        cfg.freeze()
        return cfg

    @staticmethod
    def set_model(config: "CfgNode") -> "GeneralizedRCNN":
        """
        Build the D2 model. It uses the available builtin tools of D2

        :param config: Model config
        :return: The GeneralizedRCNN model
        """
        return build_model(config.clone()).eval()

    def _instantiate_d2_predictor(self) -> None:
        checkpointer = DetectionCheckpointer(self.d2_predictor)
        checkpointer.load(self.cfg.MODEL.WEIGHTS)

    def predict(self, np_img: ImageType) -> List[DetectionResult]:
        """
        Prediction per image.

        :param np_img: image as numpy array
        :return: A list of DetectionResult
        """
        detection_results = d2_predict_image(
            np_img,
            self.d2_predictor,
            self.cfg.INPUT.MIN_SIZE_TEST,
            self.cfg.INPUT.MAX_SIZE_TEST,
            self.cfg.NMS_THRESH_CLASS_AGNOSTIC,
        )
        return self._map_category_names(detection_results)

    def _map_category_names(self, detection_results: List[DetectionResult]) -> List[DetectionResult]:
        """
        Populating category names to detection results

        :param detection_results: list of detection results. Will also filter categories
        :return: List of detection results with attribute class_name populated
        """
        filtered_detection_result: List[DetectionResult] = []
        for result in detection_results:
            result.class_name = self._categories_d2[str(result.class_id)]
            if isinstance(result.class_id, int):
                result.class_id += 1
            if self.filter_categories:
                if result.class_name not in self.filter_categories:
                    filtered_detection_result.append(result)
            else:
                filtered_detection_result.append(result)
        return filtered_detection_result

    @classmethod
    def get_requirements(cls) -> List[Requirement]:
        return [get_pytorch_requirement(), get_detectron2_requirement()]

    @classmethod
    def _map_to_d2_categories(cls, categories: Mapping[str, TypeOrStr]) -> Dict[str, ObjectTypes]:
        return {str(int(k) - 1): get_type(v) for k, v in categories.items()}

    def clone(self) -> PredictorBase:
        return self.__class__(
            self.path_yaml,
            self.path_weights,
            self.categories,
            self.config_overwrite,
            self.device,
            self.filter_categories,
        )

    def possible_categories(self) -> List[ObjectTypes]:
        return list(self.categories.values())
