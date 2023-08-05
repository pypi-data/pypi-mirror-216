# Copyright (C) 2023, NG:ITL
import logging
from abc import abstractmethod
from pathlib import Path
from typing import List

from data_aggregator.processing.writer.base_writer import BaseWriter
from data_aggregator.utils.writer_cache import WriterCache


class CachedWriter(BaseWriter):
    def __init__(self, cache_filepath: Path):
        super().__init__()
        self.writer_cache = WriterCache(cache_filepath)

    @abstractmethod
    def write_cached_data(self, data: dict):
        raise NotImplementedError

    def write_to_cache_file(self, output_data) -> None:
        logging.info("Writing to cache: %s", output_data)
        self.writer_cache.write_to_cache(output_data)

    def flush_cache(self):
        cache_lines = self.writer_cache.read_cache()
        self.writer_cache.clear()
        if len(cache_lines) == 0:
            logging.info("Cache is empty!")
        else:
            for cache_line in cache_lines:
                self.write_cached_data(cache_line)

    def get_cached_files_list(self) -> List[str]:
        cache_lines = self.writer_cache.read_cache()
        return [cache_line["input_file_path"] for cache_line in cache_lines]
