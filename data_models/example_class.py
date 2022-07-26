from datetime import datetime
from src import BaseData


class ExampleClass(BaseData):

    def __init__(self, classId: int, value: float, name: str, creation: datetime):
        self.classId = classId
        self.value = value
        self.name = name
        self.creation = creation

    def get_id(self):
        return (self.classId, )

    def to_data(self):
        data = self.__dict__.copy()
        data['creation'] = data['creation'].isoformat()
        return data

    @classmethod
    def from_data(cls, data):
        data['creation'] = datetime.fromisoformat(data['creation'])
        return cls(**data)
