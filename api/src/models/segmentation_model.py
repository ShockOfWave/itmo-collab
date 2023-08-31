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
        Аргументы:
        model_path - путь к yolo модели для сегментации
        conf - порог уверенности модели (желательно 0.3)
        '''

        self._model = YOLO(model_path)
        self._conf = conf

    def predict(
            self, 
            image: np.array = None
            ) -> List:
        
        '''
        Основная функция для предсказания

        Аргументы:
        image - изображение в виде numpy array

        Возвращает список типа [(poly1, area1), (poly2, area2), ...]
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