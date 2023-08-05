# Copyright (C) 2023, NG:ITL
from abc import ABC, abstractmethod
from typing import Any


class BaseProcessor(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def process(self, input_data: Any) -> Any:
        raise NotImplementedError
