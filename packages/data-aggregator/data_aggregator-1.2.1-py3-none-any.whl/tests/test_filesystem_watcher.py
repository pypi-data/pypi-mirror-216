# Copyright (C) 2023, NG:ITL
import tempfile
import time
import unittest

from pathlib import Path
from typing import List

from data_aggregator.utils.filesystem_watcher import FilesystemWatcher


class FilesystemWatcherTest(unittest.TestCase):
    FILESYSTEM_WATCHER_DELAY = 0.3

    def setUp(self) -> None:
        self.tmp_dir = Path(tempfile.mkdtemp())
        self.filesystem_watcher = FilesystemWatcher([self.tmp_dir], startup_delay=self.FILESYSTEM_WATCHER_DELAY)
        self.filesystem_watcher.register_callback(self.files_created_callback)
        self.filesystem_watcher.start()

        self.files_created_list: List[List[str]] = []
        self.test_file_index = 0

    def tearDown(self) -> None:
        self.filesystem_watcher.stop()

    def create_test_file(self) -> Path:
        filename = f"{self.test_file_index}.txt"
        self.test_file_index += 1
        filepath = self.tmp_dir / filename
        filepath.touch()
        return filepath

    def exceed_filesystem_watcher_delay(self):
        time.sleep(self.FILESYSTEM_WATCHER_DELAY * 1.2)

    def assert_files_returned(self, files_created_list: List[List[Path]]):
        self.assertEqual(files_created_list, self.files_created_list)

    def files_created_callback(self, file_list: List[str]):
        self.files_created_list.append(file_list)

    def test_FilesystemWatcherWaiting_SingleFileCreated_FileReturned(self):
        f0 = self.create_test_file()
        self.exceed_filesystem_watcher_delay()

        self.assert_files_returned([[f0]])

    def test_FilesystemWatcherWaiting_SingleFileCreatedButFilesystemWatcherFrameNotFinished_FileNotReturned(self):
        f0 = self.create_test_file()

        self.assert_files_returned([])

    def test_FilesystemWatcherWaiting_MultipleFilesCreatedInSingleTimeFrame_FilesReturnedInSingleFrame(self):
        f0 = self.create_test_file()
        f1 = self.create_test_file()
        self.exceed_filesystem_watcher_delay()

        self.assert_files_returned([[f0, f1]])

    def test_FilesystemWatcherWaiting_MultipleFilesCreatedInTwoTimeFrames_FilesReturnedInTwoFrames(self):
        f0 = self.create_test_file()
        f1 = self.create_test_file()
        self.exceed_filesystem_watcher_delay()
        f2 = self.create_test_file()
        f3 = self.create_test_file()
        self.exceed_filesystem_watcher_delay()

        self.assert_files_returned([[f0, f1], [f2, f3]])

    def test_FilesystemWatcherWaiting_MultipleFilesCreatedInThreeTimeFrames_FilesReturnedInThreeFrames(self):
        f0 = self.create_test_file()
        f1 = self.create_test_file()
        self.exceed_filesystem_watcher_delay()
        f2 = self.create_test_file()
        f3 = self.create_test_file()
        self.exceed_filesystem_watcher_delay()
        f4 = self.create_test_file()
        f5 = self.create_test_file()
        f6 = self.create_test_file()
        self.exceed_filesystem_watcher_delay()

        self.assert_files_returned([[f0, f1], [f2, f3], [f4, f5, f6]])
