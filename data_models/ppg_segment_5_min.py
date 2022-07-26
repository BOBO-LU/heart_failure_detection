from typing import List
from datetime import datetime
from hypergol import BaseData


class PpgSegment5Min(BaseData):

    def __init__(self, id: int, age: int, pid: int, event: int, nyha: int, start_time: datetime, ppg: List[float], tri_acc: List[float]):
        self.id = id
        self.age = age
        self.pid = pid
        self.event = event
        self.nyha = nyha
        self.start_time = start_time
        self.ppg = ppg
        self.tri_acc = tri_acc

    def get_id(self):
        return (self.id, )

    def to_data(self):
        data = self.__dict__.copy()
        data['start_time'] = data['start_time'].isoformat()
        return data

    @classmethod
    def from_data(cls, data):
        data['start_time'] = datetime.fromisoformat(data['start_time'])
        return cls(**data)
