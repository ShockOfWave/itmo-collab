from pathlib import Path
import os

def get_project_path() -> str:
    
    """ Get the project path based on project/api/src/models/utils.py path

    Returns:
        str: path to project
    """
    
    path = Path(__file__).parent.parent.parent.parent
    
    return path

PATH_TO_SEGMENTATION_MODEL = os.path.join(get_project_path(), 'api', 'weights', 'segmentation_model.pt')
PATH_TO_CLASSIFICATION_MODEL = os.path.join(get_project_path(), 'api', 'weights', 'classification_model.ckpt')