from torchvision import transforms

def get_transforms_for_predictions() -> transforms:

    """Create transforms for octane classification model

    Returns:
        torchvision.transforms: transform layer
    """
    
    data_transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize(299),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
    ])
    
    return data_transform

def decode_class_names(pred: int) -> str:
    """Decode model prediction to str

    Args:
        pred (int): model prediction

    Returns:
        str: octane number or no_bubble class
    """
    dict_classes = {
        0: '92',
        1: '95',
        2: '98',
        3: 'Unknow'
    }
    
    return dict_classes[pred]