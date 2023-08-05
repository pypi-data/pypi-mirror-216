# Copyright (C) 2023, NG:ITL
import os
import tempfile
import unittest
import csv

from datetime import datetime
from pathlib import Path
from typing import Optional

from data_aggregator.utils.input_file_tracker import InputFileTracker


class FilesystemWatcherTest(unittest.TestCase):
    INPUT_FILE_TRACKER_FILENAME = "input_file_tracker_history.csv"

    def setUp(self) -> None:
        self.tmp_dir = Path(tempfile.mkdtemp())
        self.input_file_tracker_history_filepath = self.tmp_dir / self.INPUT_FILE_TRACKER_FILENAME
        self.input_file_tracker: Optional[InputFileTracker] = None
        self.test_file_index = 0

    def tearDown(self) -> None:
        pass

    def prepare_input_file_tracker(self) -> None:
        self.input_file_tracker = InputFileTracker(self.input_file_tracker_history_filepath)

    def restart_input_file_tracker(self) -> None:
        assert self.input_file_tracker
        self.input_file_tracker.stop()
        self.prepare_input_file_tracker()

    def create_test_fileppath(self) -> Path:
        filename = f"{self.test_file_index}.txt"
        self.test_file_index += 1
        filepath = self.tmp_dir / filename
        return filepath

    def manually_add_entry_to_history_file(self, filepath: Path, timestamp=datetime.now()) -> None:
        file_exists = os.path.isfile(self.input_file_tracker_history_filepath)
        with open(self.input_file_tracker_history_filepath, "a", newline="") as csvfile:
            fieldnames = ["timestamp", "filename"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow({"timestamp": timestamp.isoformat(), "filename": filepath.name})
        self.assert_history_file_contains_file(filepath)

    def assert_file_tracked(self, filepath: Path) -> None:
        assert self.input_file_tracker
        self.assertTrue(self.input_file_tracker.is_file_tracked(filepath))

    def assert_file_untracked(self, filepath: Path):
        assert self.input_file_tracker
        self.assertFalse(self.input_file_tracker.is_file_tracked(filepath))

    def assert_history_file_contains_file(self, filepath: Path) -> bool:
        with open(self.input_file_tracker_history_filepath, "r") as history_file:
            lines = history_file.readlines()
            for line in lines:
                timestamp, filename = line.split(",")
                if filename == filepath.name:
                    return True
            return False

    def assert_number_of_tracked_files(self, expected_number_of_tracked_files: int) -> None:
        assert self.input_file_tracker
        self.assertEqual(len(self.input_file_tracker.history_dict), expected_number_of_tracked_files)

    def test_EmptyHistoryFile_AddFile_FileTracked(self) -> None:
        self.prepare_input_file_tracker()
        f0 = self.create_test_fileppath()
        self.assert_file_untracked(f0)

        assert self.input_file_tracker
        self.input_file_tracker.add_file_to_history(f0)
        self.assert_file_tracked(f0)

    def test_PreloadedHistoryFile_AddAlreadyTrackedFile_FileTracked(self) -> None:
        f0 = self.create_test_fileppath()
        f1 = self.create_test_fileppath()
        self.manually_add_entry_to_history_file(f0)
        self.manually_add_entry_to_history_file(f1)

        self.prepare_input_file_tracker()
        self.assert_number_of_tracked_files(2)
        self.assert_file_tracked(f0)

        assert self.input_file_tracker
        self.assertFalse(self.input_file_tracker.add_file_to_history(f0))

    def test_EmptyInputFileTracker_AddFilesAndRestartInputFileTracker_FilesTracked(self) -> None:
        self.prepare_input_file_tracker()

        f0 = self.create_test_fileppath()
        f1 = self.create_test_fileppath()
        assert self.input_file_tracker
        self.input_file_tracker.add_file_to_history(f0)
        self.input_file_tracker.add_file_to_history(f1)

        self.restart_input_file_tracker()

        self.assert_number_of_tracked_files(2)
        self.assert_file_tracked(f0)
        self.assert_file_tracked(f1)

        self.assertFalse(self.input_file_tracker.add_file_to_history(f0))
        self.assertFalse(self.input_file_tracker.add_file_to_history(f1))
