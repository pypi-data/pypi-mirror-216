# Copyright (C) 2023, NG:ITL
from typing import Optional, List

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QWidget, QMessageBox

from data_aggregator.gui.ui.status_widget import Ui_StatusWidget


class StatusWidget(QWidget):
    request_cache_flush_signal = Signal()

    def __init__(self, parent: Optional[QWidget] = None):
        super(StatusWidget, self).__init__(parent)
        self.status_widget = Ui_StatusWidget()
        self.status_widget.setupUi(self)

        self.setup_ui()

    def setup_ui(self):
        self.status_widget.flushCachePushButton.clicked.connect(self.handle_flush_cache_push_button_clicked)

    def update_status(self, processed_files_list: List[str], cached_files_list: List[str]):
        self.status_widget.processedFilesListWidget.clear()
        self.status_widget.cachedFilesListWidget.clear()

        self.status_widget.processedFilesListWidget.addItems(processed_files_list)
        self.status_widget.cachedFilesListWidget.addItems(cached_files_list)

        if not self.status_widget.cachedFilesListWidget.isEnabled():
            message_box = QMessageBox(self)
            message_box.setWindowTitle("Cache flushed!")
            message_box.setText(f"{len(cached_files_list)} input files remain in cache!")
            message_box.exec_()

            self.status_widget.cachedFilesListWidget.setEnabled(True)
            self.status_widget.flushCachePushButton.setEnabled(True)

    @Slot()
    def handle_flush_cache_push_button_clicked(self):
        self.status_widget.cachedFilesListWidget.setEnabled(False)
        self.status_widget.flushCachePushButton.setEnabled(False)

        self.request_cache_flush_signal.emit()
