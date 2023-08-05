# Copyright (C) 2023, NG:ITL
import abc
import logging
import os
from pathlib import Path
from os import PathLike

from data_aggregator.processing.writer.cached_writer import CachedWriter


class GenericExcelWriter(CachedWriter):
    def __init__(self, cache_filepath: Path):
        super().__init__(cache_filepath)

    @abc.abstractmethod
    def write_cached_data(self, data: dict):
        raise NotImplementedError

    @classmethod
    def is_output_file_existing(cls, output_file_path: PathLike) -> bool:
        return os.path.exists(output_file_path)

    @classmethod
    def is_output_file_open(cls, output_file_path: Path) -> bool:
        output_directory = output_file_path.parent
        output_filename = output_file_path.name
        logging.debug("Checking if file is open: %s", output_filename)
        return os.path.exists(output_directory / f"~${output_filename}")
