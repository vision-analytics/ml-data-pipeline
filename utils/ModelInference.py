import os

import numpy as np
import pandas as pd
from PIL import Image
import torch
from torchvision import transforms


from utils.FashionNetVgg16NoBn import FashionNetVgg16NoBn

class ModelInference:
    def __init__(self):
        self.device = "cpu"
        self.model = FashionNetVgg16NoBn()
        self.model.to(self.device)
        self.model.eval()

        self.loader = transforms.Compose([transforms.Resize((224,224)), 
                             transforms.ToTensor(),
                             transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                  std=[0.229, 0.224, 0.225])
                            ])


        #FASHION
        self.model_category_cloth = pd.read_csv(os.environ.get('PYTHONPATH')+'/config/list_category_cloth.txt', delimiter=r'[ \t]{2,}', header=1, usecols=["category_name", "category_type"])
        self.model_attr_cloth = pd.read_csv(os.environ.get('PYTHONPATH')+'/config/list_attr_cloth.txt', delimiter=r'[ \t]{2,}', header=1, usecols=["attribute_name", "attribute_type"])

    def image_loader(self, image_path):
        image = Image.open(image_path)
        image = self.loader(image).float()
        image = torch.autograd.Variable(image, requires_grad=True)
        return image.unsqueeze(0)


    def predict(self, image_path):
        inputs = self.image_loader(image_path)
        #inputs = inputs.to(self.device)
        output = self.model(inputs)
        
        return self.decode_predictions(output)

    def decode_predictions(self, output):

        preds_attr = output[0][0].detach().numpy()
        max_ind_attr = np.argmax(preds_attr)
        attribute_name = self.model_attr_cloth.iloc[[max_ind_attr]]['attribute_name'].item()
        attribute_type = self.model_attr_cloth.iloc[[max_ind_attr]]['attribute_type'].item()
        attribute_prob = preds_attr[max_ind_attr]


        preds_cat = output[1][0].detach().numpy()
        max_ind_cat = np.argmax(preds_cat)

        category_name = self.model_category_cloth.iloc[[max_ind_cat]]['category_name'].item()
        category_type = self.model_category_cloth.iloc[[max_ind_cat]]['category_type'].item()
        category_prob = preds_cat[max_ind_cat]
        return {
            'category_name': category_name,
            'category_type': category_type,
            'category_prob': category_prob,
            'attribute_name': attribute_name,
            'attribute_type': attribute_type,
            'attribute_prob': attribute_prob
        }