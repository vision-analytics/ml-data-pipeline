import albumentations
import cv2


class ImageAugmentation:
    def __init__(self):
        pass

    def random_resized_crop(self, image_path, height, width, scale):
        img = cv2.imread(image_path)[:,:,::-1] #bgr to rgb
        fnc = albumentations.crops.transforms.RandomResizedCrop(
            height=height, 
            width=width, 
            scale=scale
        )
        return fnc(image=img)['image']
        