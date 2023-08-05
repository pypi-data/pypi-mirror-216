from pathlib import Path
from typing import Optional


class ProcessorException(Exception):
    def __init__(self, message: str, *args):
        super().__init__(args)
        self.message = message

    def __str__(self):
        return f"error: {self.message}"


class ReaderException(Exception):
    def __init__(self, message: str, input_file_path: Optional[Path] = None, *args):
        super().__init__(args)
        self.input_file_path = input_file_path
        self.message = message

    def __str__(self):
        return f"input_file_path: {self.input_file_path}, error: {self.message}"


class WriterException(Exception):
    def __init__(self, message: str, *args):
        super().__init__(args)
        self.message = message

    def __str__(self):
        return f"error: {self.message}"
