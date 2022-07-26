from typing import List
from datetime import date
from src import BaseData
from data_models.example_class import ExampleClass


class OtherExample(BaseData):

    def __init__(self, classId: int, name: str, values: List[ExampleClass], dates: List[date]):
        self.classId = classId
        self.name = name
        self.values = values
        self.dates = dates

    def get_id(self):
        return (self.classId, )

    def to_data(self):
        data = self.__dict__.copy()
        data['values'] = [v.to_data() for v in data['values']]
        data['dates'] = [v.isoformat() for v in data['dates']]
        return data

    @classmethod
    def from_data(cls, data):
        data['values'] = [ExampleClass.from_data(v) for v in data['values']]
        data['dates'] = [date.fromisoformat(v) for v in data['dates']]
        return cls(**data)
