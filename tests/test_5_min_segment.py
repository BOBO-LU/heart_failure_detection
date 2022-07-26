from datetime import time
from datetime import date
from datetime import datetime
from unittest import TestCase
from data_models.5_min_segment import 5MinSegment


class Test5MinSegment(TestCase):

    def __init__(self, methodName):
        super(Test5MinSegment, self).__init__(methodName=methodName)
        self.5MinSegment = 5MinSegment(id=0, age=0, pid=0, event=0, nyha=0, start_time=datetime.now(), ppg=[0.0, 0.0], x=[0.0, 0.0], y=[0.0, 0.0], z=[0.0, 0.0])

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_5_min_segment_test_get_hash_id(self):
        self.assertEqual(self.5MinSegment.test_get_hash_id(), True)

    def test_5_min_segment_test_to_data(self):
        self.assertEqual(self.5MinSegment.test_to_data(), True)

    def test_5_min_segment_test_from_data(self):
        self.assertEqual(self.5MinSegment.test_from_data(), True)
