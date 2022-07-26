from datetime import time
from datetime import date
from datetime import datetime
from unittest import TestCase
from data_models.other_example import OtherExample


class TestOtherExample(TestCase):

    def __init__(self, methodName):
        super(TestOtherExample, self).__init__(methodName=methodName)
        self.otherExample = OtherExample(classId=0, name='', values=None, dates=[date.today(), date.today()])

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_other_example_test_get_hash_id(self):
        self.assertEqual(self.otherExample.test_get_hash_id(), True)

    def test_other_example_test_to_data(self):
        self.assertEqual(self.otherExample.test_to_data(), True)

    def test_other_example_test_from_data(self):
        self.assertEqual(self.otherExample.test_from_data(), True)
