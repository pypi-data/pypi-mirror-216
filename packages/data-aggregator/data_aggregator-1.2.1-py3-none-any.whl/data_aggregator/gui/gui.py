# Copyright (C) 2022, NG:ITL
import logging
import os
import pkgutil
import sys
from enum import Enum
from pathlib import Path
from typing import Optional, List

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu

from data_aggregator.gui.main_window import MainWindow

from ngitl_common_py.config import set_config_param
from ngitl_common_py.log import get_log_filepath
from ngitl_common_py.autostart import activate_autostart, deactivate_autostart
from ngitl_common_py.file_viewer_starter import open_file_viewer


BASE_DIR = Path(__file__).parent


class MessageType(Enum):
    INFO = QSystemTrayIcon.Information  # type: ignore
    WARNING = QSystemTrayIcon.Warning  # type: ignore
    ERROR = QSystemTrayIcon.Critical  # type: ignore


def resource_path() -> Path:
    base_path = getattr(sys, "_MEIPASS", os.getcwd())
    return Path(base_path)


class Gui(QObject):
    show_message_signal = Signal(str, str, MessageType)
    request_write_config_to_file_signal = Signal()
    request_reinit_signal = Signal()
    request_cache_flush_signal = Signal()

    def __init__(self, parent: Optional[QObject] = None):
        QObject.__init__(self, parent)

        self.icon = QIcon(str(resource_path() / "resources/img/icon.svg"))

        self.app: QApplication
        self.main_window: MainWindow
        self.tray_icon: QSystemTrayIcon
        self.menu: QMenu
        self.about_action: QAction
        self.preferences_action: QAction
        self.log_action: QAction
        self.flush_cache_action: QAction
        self.quit_action: QAction

        self.setup_application()
        self.setup_main_window()
        self.setup_trayicon()

        self.create_connections()

        self.show_info_message("DataAggregator Started!", "Running in the background and waiting for new files.")
        logging.info("GUI started")

    def setup_application(self):
        self.app = QApplication([])
        self.app.setQuitOnLastWindowClosed(False)
        self.app.setApplicationName("DataAggregator")

    def setup_main_window(self):
        self.main_window = MainWindow()
        self.main_window.setup_ui()
        self.main_window.setWindowIcon(self.icon)

    def setup_trayicon(self):
        # Create the icon

        # Create the tray
        self.tray_icon = QSystemTrayIcon()
        self.tray_icon.setIcon(self.icon)
        self.tray_icon.setVisible(True)

        # Create the menu
        self.menu = QMenu()

        self.about_action = QAction("About")
        self.menu.addAction(self.about_action)

        self.status_action = QAction("Status")
        self.menu.addAction(self.status_action)

        self.preferences_action = QAction("Preferences")
        self.menu.addAction(self.preferences_action)

        self.log_action = QAction("Open log")
        self.menu.addAction(self.log_action)

        self.flush_cache_action = QAction("Flush Cache")
        self.menu.addAction(self.flush_cache_action)

        # Add a Quit option to the menu.
        self.quit_action = QAction("Quit")
        self.menu.addAction(self.quit_action)

        # Add the menu to the tray
        self.tray_icon.setContextMenu(self.menu)

    def create_connections(self):
        self.status_action.triggered.connect(self.handle_status_action_triggered)
        self.preferences_action.triggered.connect(self.handle_preferences_action_triggered)
        self.log_action.triggered.connect(self.handle_log_action_triggered)
        self.flush_cache_action.triggered.connect(self.request_cache_flush_signal)
        self.quit_action.triggered.connect(self.app.quit)

        self.main_window.preferences_widget.apply_signal.connect(self.handle_preferences_apply_signal)
        self.main_window.status_widget.request_cache_flush_signal.connect(self.request_cache_flush_signal)
        self.show_message_signal.connect(self.handle_show_message_signal)

    @Slot()
    def handle_preferences_apply_signal(self):
        set_config_param("input_directories", self.main_window.preferences_widget.get_input_directories())
        set_config_param("output_directory", self.main_window.preferences_widget.get_output_directory())

        if self.main_window.preferences_widget.preferences_widget.autostart_check_box.isChecked():
            activate_autostart()
        else:
            deactivate_autostart()

        self.request_write_config_to_file_signal.emit()
        self.request_reinit_signal.emit()

    @Slot()
    def handle_processing_results(self, processed_files: List[str], cached_files: List[str]):
        self.main_window.status_widget.update_status(processed_files, cached_files)

    @Slot()
    def handle_show_message_signal(self, title: str, message: str, type: MessageType):
        self.tray_icon.showMessage(title, message, type.value)

    @Slot()
    def handle_status_action_triggered(self):
        self.main_window.show()
        self.main_window.main_window.tabWidget.setCurrentIndex(0)

    @Slot()
    def handle_preferences_action_triggered(self):
        self.main_window.show()
        self.main_window.main_window.tabWidget.setCurrentIndex(1)

    @Slot()
    def handle_log_action_triggered(self):
        open_file_viewer(get_log_filepath())

    def show_info_message(self, title: str, message: str):
        self.show_message_signal.emit(title, message, MessageType.INFO)

    def run(self):
        self.app.exec_()
