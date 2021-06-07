import albumentations
import numpy as np
from PIL import Image


class ImageAugmentation:
    def __init__(self):
        pass

    def random_resized_crop(self, image_path, height, width, scale):
        img = np.asarray(Image.open(image_path))
        fnc = albumentations.crops.transforms.RandomResizedCrop(
            height=height, 
            width=width, 
            scale=scale
        )
        return fnc(image=img)['image']
        