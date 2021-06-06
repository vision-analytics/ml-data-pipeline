import unittest

from models.Style import Style
from api import query


class TestMyCode(unittest.TestCase):

    def test_query(self):
        filters = [Style.gender == "Unisex", Style.articleType == "Watches", Style.year >= 2013]
        # query
        items = query.run_query(Style, filters, limit=10, upload_to_s3=False)           
        self.assertEqual(items.count(), 10)
