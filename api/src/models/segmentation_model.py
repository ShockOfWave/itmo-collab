from typing import List
import numpy as np
from ultralytics import YOLO

class SegmentationModel:
    def __init__(
            self, 
            model_path: str = None,
            conf: float = 0.3
            ) -> None:
        
        '''
        Args:
        model_path - path to segmentation yolo model
        conf - model coinfidence (recommended 0.3)
        '''

        self._model = YOLO(model_path)
        self._conf = conf

    def predict(
            self, 
            image: np.array = None
            ) -> List:
        
        '''
        Main function for prediction

        Args:
        image - image as numpy array

        Returns list like [(poly1, area1), (poly2, area2), ...]
        '''

        result = self._model.predict(
            image,
            conf = self._conf,
            verbose = False
            )
        
        if len(result[0]):
            polygons = [np.array(poly, np.int32) for poly in result[0].masks.xy]
            
            return polygons
        else:
            return None