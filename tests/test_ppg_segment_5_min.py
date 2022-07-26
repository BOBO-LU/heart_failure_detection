from datetime import time
from datetime import date
from datetime import datetime
from unittest import TestCase
from data_models.ppg_segment_5_min import PpgSegment5Min


class TestPpgSegment5Min(TestCase):

    def __init__(self, methodName):
        super(TestPpgSegment5Min, self).__init__(methodName=methodName)
        self.ppgSegment5Min = PpgSegment5Min(id=0, age=0, pid=0, event=0, nyha=0, start_time=datetime.now(), ppg=[0.0, 0.0], x=[0.0, 0.0], y=[0.0, 0.0], z=[0.0, 0.0])

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_ppg_segment_5_min_test_get_hash_id(self):
        self.assertEqual(self.ppgSegment5Min.test_get_hash_id(), True)

    def test_ppg_segment_5_min_test_to_data(self):
        self.assertEqual(self.ppgSegment5Min.test_to_data(), True)

    def test_ppg_segment_5_min_test_from_data(self):
        self.assertEqual(self.ppgSegment5Min.test_from_data(), True)
