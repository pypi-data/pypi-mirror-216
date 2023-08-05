# Copyright (C) 2023, NG:ITL
import os
import logging

from threading import Lock, Event
from pathlib import Path
from typing import Optional, List
from PySide6.QtCore import QObject, Signal, Slot

from data_aggregator.gui.gui import MessageType
from data_aggregator.processing.writer.cached_writer import CachedWriter
from data_aggregator.processing.processor.base_processor import BaseProcessor
from data_aggregator.processing.reader.base_reader import BaseReader
from data_aggregator.processing.exceptions import ReaderException, ProcessorException, WriterException
from data_aggregator.utils.input_file_tracker import InputFileTracker
from data_aggregator.utils.filesystem_watcher import FilesystemWatcher

from ngitl_common_py.config import get_config_param


class DataAggregator(QObject):
    show_message_signal = Signal(str, str, MessageType)
    processing_results_signal = Signal(list, list)

    def __init__(self, input_reader: BaseReader, processor: BaseProcessor, output_writer: CachedWriter, parent=None):
        QObject.__init__(self, parent)
        self.input_file_tracker = InputFileTracker(Path(get_config_param("input_file_tracker_history_filepath")))
        self.filesystem_watcher = FilesystemWatcher(get_config_param("input_directories"))
        self.filesystem_watcher.register_callback(self.handle_file_creation)

        self.input_reader = input_reader
        self.processor = processor
        self.output_writer = output_writer

        self.handled_input_files_count = 0
        self.handled_input_files_count_lock = Lock()
        self.handled_input_files_count_increased_event = Event()

        logging.info("Starting DataAggregator")

    def __inc_handled_input_files_count(self) -> None:
        with self.handled_input_files_count_lock:
            self.handled_input_files_count += 1
        self.handled_input_files_count_increased_event.set()

    def stop(self):
        self.filesystem_watcher.stop()
        self.input_file_tracker.stop()
        logging.info("DataAggregator stopped!")

    def start_filesystem_watcher(self):
        self.filesystem_watcher.start()

    def start_initial_file_check(self):
        logging.info("Start initial file check")
        for input_directory in get_config_param("input_directories"):
            input_files_paths = [
                Path(input_directory) / input_file_path for input_file_path in os.listdir(input_directory)
            ]
            logging.info('Checking %d file(s) in input directory "%s"', len(input_files_paths), input_directory)
            self.process_input_files(input_files_paths)
        self.output_writer.flush_cache()
        self.processing_results_signal.emit(
            self.input_file_tracker.get_files_list(), self.output_writer.get_cached_files_list()
        )

    def process_input_files(self, input_files_paths: List[Path]) -> None:
        for input_file_path in input_files_paths:
            self.process_input_file(input_file_path)

    def process_input_file(self, input_file_path: Path) -> None:
        if self.check_if_file_should_be_processed(input_file_path):
            try:
                input_data = self.input_reader.read(input_file_path)
                output_data = self.processor.process(input_data)

                if not self.output_writer.write(output_data):
                    self.output_writer.write_to_cache_file(output_data)
                    self.handle_warning_message(
                        "Unable to write output", f'Output file for "{input_file_path}" is open, please close the file.'
                    )
            except (ReaderException, ProcessorException, WriterException) as e:
                self.handle_error_message("Error", f"{e.__class__.__name__}: {e}")

            self.input_file_tracker.add_file_to_history(input_file_path)
            self.input_file_tracker.write_history_to_file()

        self.__inc_handled_input_files_count()

    def check_if_file_should_be_processed(self, input_filepath: Path) -> bool:
        filename = input_filepath.name

        if filename.startswith("~"):
            logging.info('Ignoring file "%s" because it is a tmp file', input_filepath)
            return False
        elif not filename.endswith(".xlsx") and not filename.endswith(".xlsm"):
            logging.info('Ignoring file "%s" because it is not a xlsx/xlsm file', input_filepath)
            return False
        elif self.input_file_tracker.is_file_tracked(input_filepath):
            logging.info('Ignoring file "%s" because it was already processed', input_filepath)
            return False
        else:
            return True

    def handle_file_creation(self, input_files_paths: List[Path]) -> None:
        self.handle_info_message("New files detected!", f"Checking {len(input_files_paths)} new input files.")
        self.process_input_files(input_files_paths)
        self.handle_info_message("Done!", f"Processed {len(input_files_paths)} input files!")
        self.processing_results_signal.emit(
            self.input_file_tracker.get_files_list(), self.output_writer.get_cached_files_list()
        )

    def handle_info_message(self, title: str, message: str):
        logging.info("%s - %s", title, message)
        self.show_message_signal.emit(title, message, MessageType.INFO)

    def handle_warning_message(self, title: str, message: str):
        logging.warning("%s - %s", title, message)
        self.show_message_signal.emit(title, message, MessageType.WARNING)

    def handle_error_message(self, title: str, message: str):
        logging.error("%s - %s", title, message)
        self.show_message_signal.emit(title, message, MessageType.ERROR)

    @Slot()
    def handle_cache_flush_request(self) -> None:
        logging.info("Cache flush request received.")
        self.output_writer.flush_cache()
        self.processing_results_signal.emit(
            self.input_file_tracker.get_files_list(), self.output_writer.get_cached_files_list()
        )

    def get_handled_input_files_count(self) -> int:
        with self.handled_input_files_count_lock:
            return self.handled_input_files_count

    def wait_for_handled_input_files_count_increased(self, timeout: Optional[float] = None) -> int:
        if self.handled_input_files_count_increased_event.wait(timeout):
            self.handled_input_files_count_increased_event.clear()
            return self.get_handled_input_files_count()
        else:
            raise TimeoutError
