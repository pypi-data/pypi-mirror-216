# Copyright (C) 2023, NG:ITL
from typing import Optional

from PySide6.QtWidgets import QMainWindow, QWidget

from data_aggregator.gui.ui.main_window import Ui_MainWindow
from data_aggregator.gui.widgets.preferences_widget import PreferencesWidget
from data_aggregator.gui.widgets.status_widget import StatusWidget


class MainWindow(QMainWindow):
    def __init__(self, parent: Optional[QWidget] = None):
        super(MainWindow, self).__init__(parent)
        self.main_window = Ui_MainWindow()
        self.main_window.setupUi(self)

        self.preferences_widget = PreferencesWidget(self)
        self.status_widget = StatusWidget(self)

    def setup_ui(self):
        self.setWindowTitle("DataAggregator")
        self.main_window.tabWidget.addTab(self.status_widget, "Status")
        self.main_window.tabWidget.addTab(self.preferences_widget, "Preferences")

        self.show()
