from datetime import time
from datetime import date
from datetime import datetime
from unittest import TestCase
from data_models.example_class import ExampleClass


class TestExampleClass(TestCase):

    def __init__(self, methodName):
        super(TestExampleClass, self).__init__(methodName=methodName)
        self.exampleClass = ExampleClass(classId=0, value=0.0, name='', creation=datetime.now())

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_example_class_test_get_hash_id(self):
        self.assertEqual(self.exampleClass.test_get_hash_id(), True)

    def test_example_class_test_to_data(self):
        self.assertEqual(self.exampleClass.test_to_data(), True)

    def test_example_class_test_from_data(self):
        self.assertEqual(self.exampleClass.test_from_data(), True)
