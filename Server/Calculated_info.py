from dataclasses import dataclass, field
from typing import  List


@dataclass
class Points:
    data: List[float] = field(default_factory=list)

    def get_data(self):
        return self.__dict__
