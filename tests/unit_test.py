import unittest
import torch

from api import query
from models.Style import Style
from utils.ModelInference import ModelInference



class TestMyCode(unittest.TestCase):

    def test_query(self):
        filters = [Style.gender == "Unisex", Style.articleType == "Watches", Style.year >= 2013]
        # query
        items = query.run_query(Style, filters, limit=10, upload_to_s3=False)           
        self.assertEqual(items.count(), 10)

    def test_model(self):
        model = ModelInference()
        image = torch.Tensor(torch.rand(1, 3, 224, 224))
        out = model.model(image)
        self.assertEqual(len(out[0][0]), 1000)
        self.assertEqual(len(out[1][0]), 50)