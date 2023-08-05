# Copyright (C) 2023, NG:ITL
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseReader(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def read(self, input_filepath: Path) -> Any:
        raise NotImplementedError
