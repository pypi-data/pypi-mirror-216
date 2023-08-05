# Copyright (C) 2023, NG:ITL
from abc import ABC, abstractmethod
from typing import Any


class BaseWriter(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def write(self, output_data: Any):
        raise NotImplementedError
