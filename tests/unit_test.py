import unittest
import torch

from api import query
from celery_worker import tasks
from models.Style import Style
from utils.ModelInference import ModelInference


class TestMyCode(unittest.TestCase):

    def test_query(self):
        # test running new query
        filters = [Style.gender == "Unisex", Style.articleType == "Watches", Style.year >= 2013]
        # query
        items = query.run_query(Style, filters, limit=10, upload_to_s3=False)           
        self.assertEqual(items.count(), 10)

    def test_model(self):
        # test model inference with random input
        model = ModelInference()
        image = torch.Tensor(torch.rand(1, 3, 224, 224))
        out = model.model(image)
        self.assertEqual(len(out[0][0]), 1000)
        self.assertEqual(len(out[1][0]), 50)

    def test_celery_sample_task(self):
        # test running celery task  
        t = tasks.add.apply(args=[1, 2])
        self.assertEqual(t.status, "SUCCESS")
        self.assertEqual(t.result, 3)

