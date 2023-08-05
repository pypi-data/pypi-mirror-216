# Copyright (C) 2023, NG:ITL
import json

from pathlib import Path
from typing import NamedTuple, List


class WriterCache:
    def __init__(self, cache_filepath: Path):
        self.cache_filepath = cache_filepath
        pass

    def write_to_cache(self, output_data: NamedTuple):
        cache_line = json.dumps(output_data._asdict())
        with open(self.cache_filepath, "a") as cache_file:
            cache_file.write(cache_line + "\n")

    def read_cache(self) -> List[dict]:
        try:
            with open(self.cache_filepath, "r") as cache_file:
                cache_lines = cache_file.readlines()
                return [json.loads(cache_line) for cache_line in cache_lines]
        except FileNotFoundError:
            return []

    def clear(self) -> None:
        if self.cache_filepath.exists():
            with open(self.cache_filepath, "r+") as file:
                file.truncate(0)
