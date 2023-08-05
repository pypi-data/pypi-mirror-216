# Copyright (C) 2022, NG:ITL
import logging
import abc
import sys
import traceback

from abc import ABCMeta
from pathlib import Path
from PySide6.QtCore import QObject, Slot
from typing import Optional
from argparse import ArgumentParser

from data_aggregator.processing.processor.base_processor import BaseProcessor
from data_aggregator.processing.reader.base_reader import BaseReader
from data_aggregator.processing.writer.cached_writer import CachedWriter
from data_aggregator.gui.gui import Gui
from data_aggregator.aggregator import DataAggregator

from ngitl_common_py.log import init_logging, init_emergency_logging, validate_log_level
from ngitl_common_py.config import (
    get_config,
    get_config_param,
    find_config_file,
    read_config,
    write_config_to_file,
    ConfigEntryError,
    DEFAULT_CONFIG_SEARCH_PATHS,
)


class BaseDataAggregatorAppMeta(type(QObject), ABCMeta):  # type: ignore
    pass


class BaseDataAggregatorApp(QObject, metaclass=BaseDataAggregatorAppMeta):
    def __init__(self, parent: Optional[QObject] = None):
        QObject.__init__(self, parent)

        self.input_reader: Optional[BaseReader] = None
        self.processor: Optional[BaseProcessor] = None
        self.output_writer: Optional[CachedWriter] = None

        self.args = self._parse_args()
        self.config_filepath = self._setup_config()
        self._setup_logging()

        self.gui = self._setup_gui()

        self.setup_processing()

        self.data_aggregator = self._setup_aggregator()

    @abc.abstractmethod
    def add_cli_arguments(self, argument_parser: ArgumentParser) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def setup_processing(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def setup_gui(self, gui: Gui) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def validate_config(self, config: dict) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_version(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_app_name(self) -> str:
        raise NotImplementedError

    def _parse_args(self):
        arg_parser = ArgumentParser(prog="data_aggregator", description="Smart data processing")
        arg_parser.add_argument("--version", action="store_true", help="Prints the version.")
        arg_parser.add_argument("-c", "--config", dest="config_filepath", help="Override the config filepath.")
        arg_parser.add_argument("-l", "--log-level", dest="log_level", help="Override the log level.")
        self.add_cli_arguments(arg_parser)
        return arg_parser.parse_args()

    def _determine_config_filepath(self) -> Optional[Path]:
        if self.args.config_filepath:
            return self.args.config_filepath
        else:
            app_name = self.get_app_name()
            return find_config_file(f"{app_name}_config.json")

    def _setup_config(self) -> Path:
        app_name = self.get_app_name()
        config_filepath = self._determine_config_filepath()
        if config_filepath is None:
            init_emergency_logging(app_name)
            logging.error("Unable to find config file in search paths: %s", DEFAULT_CONFIG_SEARCH_PATHS)
            sys.exit(-1)
        read_config(config_filepath)
        try:
            config = get_config()
            self.validate_config(config)
        except ConfigEntryError as e:
            init_emergency_logging(app_name)
            logging.error(e)
            sys.exit(-1)
        return config_filepath

    def _determine_log_level(self) -> str:
        log_level: Optional[str] = None
        if self.args.log_level:
            log_level = self.args.log_level
        else:
            log_level = get_config_param("logging_level")

        if log_level and validate_log_level(log_level):
            return log_level
        else:
            return "DEBUG"

    def _setup_logging(self) -> None:
        log_file_directory = Path(get_config_param("log_file_directory"))
        logging_level = self._determine_log_level()
        init_logging("data_aggregator", log_file_directory, logging_level)
        logging.info("Config search paths: %s", DEFAULT_CONFIG_SEARCH_PATHS)
        logging.info("Using config file: %s", self.config_filepath)

    def _setup_gui(self) -> Gui:
        gui = Gui()
        gui.request_reinit_signal.connect(self.handle_reinit_signal)
        return gui

    def _setup_aggregator(self) -> DataAggregator:
        assert self.input_reader
        assert self.processor
        assert self.output_writer

        data_aggregator = DataAggregator(self.input_reader, self.processor, self.output_writer)

        data_aggregator.show_message_signal.connect(self.gui.handle_show_message_signal)
        data_aggregator.processing_results_signal.connect(self.gui.handle_processing_results)
        self.gui.request_cache_flush_signal.connect(data_aggregator.handle_cache_flush_request)
        self.gui.request_write_config_to_file_signal.connect(self.handle_request_write_config_to_file_signal)

        data_aggregator.start_initial_file_check()
        data_aggregator.start_filesystem_watcher()
        return data_aggregator

    def _stop_aggregator(self) -> None:
        if self.data_aggregator:
            self.data_aggregator.stop()

    @Slot()
    def handle_reinit_signal(self) -> None:
        logging.info("Reinit signal triggered")
        self._stop_aggregator()
        self.data_aggregator = self._setup_aggregator()

    @Slot()
    def handle_request_write_config_to_file_signal(self) -> None:
        logging.info("Writing config to file")
        write_config_to_file(self.config_filepath)

    def process_cli_arguments(self):
        if self.args.version:
            print(self.get_version())
            sys.exit(0)

    def run(self) -> None:
        try:
            self.process_cli_arguments()

            self.gui.run()

        except Exception as e:
            logging.error(traceback.format_exc())
            raise e
