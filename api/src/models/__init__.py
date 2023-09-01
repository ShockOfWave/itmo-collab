import os

from api.src.utils.paths import get_project_path, PATH_TO_SEGMENTATION_MODEL, PATH_TO_CLASSIFICATION_MODEL
from api.src.utils.s3 import download_file_from_s3
from api.src.models.classification_model import OctaneClassifier
from api.src.models.segmentation_model import SegmentationModel
from api.src.models.predict_model import get_octane_number_from_model, get_prediction_from_segmentation_model

def check_models() -> None:
    """ Download from s3 bucket models weights
    """
    save_path = os.path.join(get_project_path(), 'api', 'weights')
    
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        
        print('################################################')
        print('####### Downloading classification model #######')
        print('################################################')
        
        download_file_from_s3(s3_uri=os.path.join('weights', 'classification_model.ckpt'),
                              path_to_local_storage=os.path.join(save_path, 'classification_model.ckpt'))
        
        print('################################################')
        print('######## Downloading segmentation model ########')
        print('################################################')
        
        download_file_from_s3(s3_uri=os.path.join('weights', 'segmentation_model.pt'),
                              path_to_local_storage=os.path.join(save_path, 'segmentation_model.pt'))
        
    else:
        if not os.path.isfile(os.path.join(save_path, 'classification_model.ckpt')):
            
            print('################################################')
            print('####### Downloading classification model #######')
            print('################################################')
            
            download_file_from_s3(s3_uri=os.path.join('weights', 'classification_model.ckpt'),
                              path_to_local_storage=os.path.join(save_path, 'classification_model.ckpt'))
        
        if not os.path.isfile(os.path.join(save_path, 'segmentation_model.pt')):
            
            print('################################################')
            print('######## Downloading segmentation model ########')
            print('################################################')
            
            download_file_from_s3(s3_uri=os.path.join('weights', 'segmentation_model.pt'),
                              path_to_local_storage=os.path.join(save_path, 'segmentation_model.pt'))
            
def init_models() -> [OctaneClassifier, SegmentationModel]:
    """Create variables with models

    Returns:
        [OctaneClassifier, SegmentationModel]: Classification model and segmentation model
    """
    segmentation_model = SegmentationModel(model_path=PATH_TO_SEGMENTATION_MODEL)
    classification_model = OctaneClassifier.load_from_checkpoint(checkpoint_path=PATH_TO_CLASSIFICATION_MODEL, map_location='cuda:0')
    
    return segmentation_model, classification_model

# TODO: Need to delete this fucntion after testing, use init_models unsteed
def test_models():
    """Check models working
    """
    segmentation_model, classification_model = init_models()
    
    print(get_prediction_from_segmentation_model(segmentation_model,
                                                 os.path.join(get_project_path(), 'images', '10_1001.jpg')))
    
    print(get_octane_number_from_model(classification_model,
                                       os.path.join(get_project_path(), 'images', '10_1001.jpg')))
    
        
if __name__ == '__main__':
    check_models()