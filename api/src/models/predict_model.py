import os
import torch
import cv2
import numpy as np
from api.src.models.classification_model import OctaneClassifier
from api.src.models.segmentation_model import SegmentationModel
from api.src.utils.models_decoders import get_transforms_for_predictions, decode_class_names
from api.src.utils.paths import get_project_path

def get_octane_number_from_model(model: OctaneClassifier, device: str, path_to_image: str = None, image: np.array = None):
    
    """Get prediction from the model

    Args:
        path_to_image (str, optional): Path to image need to be segmentated. Defaults to None.
        image (np.array, optional): Image need to be segmentated. Defaults to None.
        
    Raises:
        ValueError: raise when input was not path to image or np.array

    Returns:
        str: predicted octane number or no_bubble class
    """
    
    transform = get_transforms_for_predictions()
    
    if not path_to_image is None:

        image = cv2.imread(path_to_image)
        image = transform(image)
        image = image.unsqueeze_(0)
    
    elif not image is None:
        
        image = transform(image)
        image = image.unsqueeze_(0)
        
    else:
        raise ValueError('Model can predict only on path to image or np.array')
        
    image = image.to(device)
        
    with torch.no_grad():
        model.eval()
        probs = model(image)
        preds = np.argmax(probs.detach().cpu().numpy(), 1)
        
        return decode_class_names(preds[0])
    
def get_prediction_from_segmentation_model(path_to_image: str = None, image: np.array = None):
    """Model predict countors

    Args:
        path_to_image (str, optional): Path to image need to be segmentated. Defaults to None.
        image (np.array, optional): Image need to be segmentated. Defaults to None.

    Raises:
        ValueError: Raises if all args if None

    Returns:
        list: polygons and area of bubble [(poly, area)]. If no bubble on image, returns [(None, None)]
    """
    if not path_to_image is None:
        
        image = cv2.imread(path_to_image)
        
    elif not image is None:
        image = image
        
    else:
        raise ValueError('Model can predict only on path to image or np.array')
    
    model = SegmentationModel(model_path=os.path.join(get_project_path(), 'api',
                                                      'weights', 'segmentation_model.pt'))
    
    return model.predict(image)