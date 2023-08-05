# Copyright (C) 2022, NG:ITL
import os

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QFileDialog, QWidget

from data_aggregator.gui.ui.input_directory_entry_widget import (
    Ui_InputDirectoryEntryWidget,
)


class InputDirectoryEntryWidget(QWidget):
    remove_signal = Signal(QWidget)

    def __init__(self, directory_path: str = ""):
        super(InputDirectoryEntryWidget, self).__init__()
        self.widget = Ui_InputDirectoryEntryWidget()
        self.widget.setupUi(self)
        self.create_connections()

        self.widget.directory_line_edit.setText(str(directory_path))

    def create_connections(self) -> None:
        self.widget.remove_directory_push_button.clicked.connect(self.handle_remove_directory_button_clicked)
        self.widget.select_directory_push_button.clicked.connect(self.handle_select_directory_push_button_clicked)

    def get_value(self) -> str:
        return self.widget.directory_line_edit.text()

    @Slot()
    def handle_remove_directory_button_clicked(self):
        self.remove_signal.emit(self)

    @Slot()
    def handle_select_directory_push_button_clicked(self):
        selected_directory = QFileDialog.getExistingDirectory(
            self,
            "Open Directory",
            os.getcwd(),
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
        )
        self.widget.directory_line_edit.setText(selected_directory)
