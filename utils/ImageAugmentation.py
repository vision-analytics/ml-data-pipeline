import albumentations

class ImageAugmentation:
    def __init__(self):
        pass

    def random_resized_crop(self, image, height, width, scale):
        
        fnc = albumentations.crops.transforms.RandomResizedCrop(
            height=height, 
            width=width, 
            scale=scale
        )
        return fnc(image=image)['image']
        