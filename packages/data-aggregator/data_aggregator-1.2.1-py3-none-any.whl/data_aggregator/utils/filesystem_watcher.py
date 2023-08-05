# Copyright (C) 2022, NG:ITL
from pathlib import Path
from typing import List, Callable
from threading import Timer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import logging


class ResettableTimer:
    def __init__(self, time, function, args=None, kwargs=None):
        self._time = time
        self._function = function
        self._args = args
        self._kwargs = kwargs
        self._set()
        self._running = False

    def _set(self):
        self._timer = Timer(self._time, self._function, self._args, self._kwargs)

    def start(self):
        self._running = True
        self._timer.start()

    def cancel(self):
        self._running = False
        self._timer.cancel()

    def reset(self, start=True):
        if self._running:
            self._timer.cancel()

        self._set()

        if self._running or start:
            self.start()


class FilesystemWatcher(FileSystemEventHandler):
    def __init__(self, directory_paths: List[Path], startup_delay=0.3):
        self.observer = Observer()
        self.directory_paths = directory_paths
        self.files_added_list: List[Path] = []
        self.timer = ResettableTimer(startup_delay, self.timer_timeout_callback)
        self.callbacks: List[Callable] = []
        logging.info("Filesystem Watcher created!")

    def stop(self):
        self.observer.stop()
        try:
            self.observer.join()
            for directory_path in self.directory_paths:
                logging.info("Filesystem Watcher stopped to watch at %s", directory_path)
        except RuntimeError:
            logging.info("Filesystem Watcher wasn't running!")
        logging.info("Filesystem Watcher stopped!")

    def start(self) -> None:
        for directory_path in self.directory_paths:
            self.observer.schedule(self, directory_path, recursive=True)
            logging.info("FilesystemWatcher watching at %s", directory_path)
        self.observer.start()

    def register_callback(self, callback):
        self.callbacks.append(callback)

    def timer_timeout_callback(self):
        for callback in self.callbacks:
            callback(self.files_added_list.copy())
        self.files_added_list.clear()

    def on_any_event(self, event):
        if event.event_type == "created":
            logging.debug("Detected create event: %s", event.src_path)
            self.files_added_list.append(Path(event.src_path))
            self.timer.reset()
        elif event.event_type == "updated":
            logging.debug("Detected updated event: %s", event.src_path)
