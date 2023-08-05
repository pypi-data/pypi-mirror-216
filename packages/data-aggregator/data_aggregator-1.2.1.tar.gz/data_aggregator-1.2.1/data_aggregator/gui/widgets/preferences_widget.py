# Copyright (C) 2023, NG:ITL
from typing import List, Optional

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QFileDialog, QWidget

from data_aggregator.gui.ui.preferences_widget import Ui_PreferencesWidget
from data_aggregator.gui.widgets.input_directory_entry_widget import InputDirectoryEntryWidget
from ngitl_common_py.config import get_config_param
from ngitl_common_py.autostart import is_autostart_enabled


class PreferencesWidget(QWidget):
    apply_signal = Signal()

    def __init__(self, parent: Optional[QWidget] = None):
        super(PreferencesWidget, self).__init__(parent)
        self.preferences_widget = Ui_PreferencesWidget()
        self.preferences_widget.setupUi(self)

        self.setup_ui()

    def setup_ui(self):
        self.preferences_widget.select_output_directory_push_button.clicked.connect(
            self.handle_select_output_directory_push_button_clicked
        )
        self.preferences_widget.apply_push_button.clicked.connect(self.handle_apply_push_button_clicked)
        self.preferences_widget.add_push_button.clicked.connect(self.handle_add_push_button_clicked)
        self.preferences_widget.output_directory_line_edit.setText(get_config_param("output_directory"))
        self.preferences_widget.autostart_check_box.setChecked(is_autostart_enabled())

        for input_directory in get_config_param("input_directories"):
            self.__add_input_directory_entry(input_directory)

    def get_input_directories(self) -> List[str]:
        input_directories: List[str] = []
        for i in range(self.preferences_widget.input_directories_vertical_layout.count()):
            input_directories.append(
                self.preferences_widget.input_directories_vertical_layout.itemAt(i).widget().get_value()
            )
        return input_directories

    def get_output_directory(self) -> str:
        return self.preferences_widget.output_directory_line_edit.text()

    def __add_input_directory_entry(self, path: str = ""):
        new_entry = InputDirectoryEntryWidget(path)
        new_entry.remove_signal.connect(self.handle_input_directory_entry_remove_requested)
        self.preferences_widget.input_directories_vertical_layout.addWidget(new_entry)

    @Slot()
    def handle_add_push_button_clicked(self):
        self.__add_input_directory_entry()

    @Slot(QWidget)
    def handle_input_directory_entry_remove_requested(self, entry: QWidget):
        entry.close()
        self.preferences_widget.input_directories_vertical_layout.removeWidget(entry)

    @Slot()
    def handle_select_output_directory_push_button_clicked(self):
        selected_directory = QFileDialog.getExistingDirectory(
            self,
            "Open Directory",
            "C:",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
        )
        self.preferences_widget.output_directory_line_edit.setText(selected_directory)

    @Slot()
    def handle_apply_push_button_clicked(self):
        self.apply_signal.emit()
