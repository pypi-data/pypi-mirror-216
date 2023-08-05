# Copyright (C) 2022, NG:ITL
import csv
import logging
from datetime import datetime
from typing import Tuple, Dict, List
from collections import OrderedDict
from pathlib import Path


class InputFileTracker:
    def __init__(self, history_filepath: Path):
        self.history_file_path = history_filepath
        self.history_dict: OrderedDict[str, Dict[str, str]] = OrderedDict()
        self.read_history_from_file()
        logging.info("Initialized InputFileTracker")
        logging.info("Using history file: %s", history_filepath)
        logging.info("Number of entries in history file: %s", len(self.history_dict))

    def stop(self) -> None:
        self.write_history_to_file()
        logging.info("InputFileTracker stopped!")

    def is_file_tracked(self, file_path: Path) -> bool:
        return file_path.name in self.history_dict

    def clear_history(self) -> None:
        self.history_dict.clear()

    def read_history_from_file(self) -> None:
        try:
            with open(self.history_file_path, "r") as history_file:
                reader = csv.DictReader(history_file)
                self.clear_history()
                for row in reader:
                    self.history_dict[row["filename"]] = row
        except FileNotFoundError:
            logging.warning("History file not found: %s", self.history_file_path)

    def write_history_to_file(self) -> None:
        with open(self.history_file_path, "w", newline="") as history_file:
            fieldnames = ["timestamp", "filename"]
            writer = csv.DictWriter(history_file, fieldnames=fieldnames)
            writer.writeheader()
            for value in self.history_dict.values():
                writer.writerow(value)

        logging.debug("History written to file: %s", self.history_file_path)

    def add_file_to_history(self, filepath: Path) -> bool:
        if not self.is_file_tracked(filepath):
            filename = filepath.name
            timestamp = datetime.now().isoformat()
            self.history_dict[filename] = {"filename": filename, "timestamp": timestamp}
            logging.debug("File added to history: %s", filepath)
            return True
        return False

    def get_files_list(self) -> List[str]:
        return [filename for filename in self.history_dict.keys()]
