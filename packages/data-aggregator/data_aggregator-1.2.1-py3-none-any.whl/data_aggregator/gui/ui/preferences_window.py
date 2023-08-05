# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preferences_window.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFrame,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)


class Ui_PreferencesWindow(object):
    def setupUi(self, PreferencesWindow):
        if not PreferencesWindow.objectName():
            PreferencesWindow.setObjectName("PreferencesWindow")
        PreferencesWindow.resize(946, 622)
        self.centralwidget = QWidget(PreferencesWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.select_output_directory_push_button = QPushButton(self.centralwidget)
        self.select_output_directory_push_button.setObjectName("select_output_directory_push_button")

        self.gridLayout.addWidget(self.select_output_directory_push_button, 15, 1, 1, 1)

        self.apply_push_button = QPushButton(self.centralwidget)
        self.apply_push_button.setObjectName("apply_push_button")

        self.gridLayout.addWidget(self.apply_push_button, 24, 0, 1, 3)

        self.input_directory_label = QLabel(self.centralwidget)
        self.input_directory_label.setObjectName("input_directory_label")

        self.gridLayout.addWidget(self.input_directory_label, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 9, 0, 1, 1)

        self.input_directories_vertical_layout = QVBoxLayout()
        self.input_directories_vertical_layout.setSpacing(1)
        self.input_directories_vertical_layout.setObjectName("input_directories_vertical_layout")

        self.gridLayout.addLayout(self.input_directories_vertical_layout, 1, 0, 1, 3)

        self.autostart_check_box = QCheckBox(self.centralwidget)
        self.autostart_check_box.setObjectName("autostart_check_box")

        self.gridLayout.addWidget(self.autostart_check_box, 23, 0, 1, 1)

        self.output_directory_line_edit = QLineEdit(self.centralwidget)
        self.output_directory_line_edit.setObjectName("output_directory_line_edit")

        self.gridLayout.addWidget(self.output_directory_line_edit, 15, 0, 1, 1)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName("line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_2, 19, 0, 1, 3)

        self.clear_output_directory_push_button = QPushButton(self.centralwidget)
        self.clear_output_directory_push_button.setObjectName("clear_output_directory_push_button")

        self.gridLayout.addWidget(self.clear_output_directory_push_button, 15, 2, 1, 1)

        self.output_directory_label = QLabel(self.centralwidget)
        self.output_directory_label.setObjectName("output_directory_label")

        self.gridLayout.addWidget(self.output_directory_label, 13, 0, 1, 1)

        self.add_push_button = QPushButton(self.centralwidget)
        self.add_push_button.setObjectName("add_push_button")
        self.add_push_button.setFlat(False)

        self.gridLayout.addWidget(self.add_push_button, 4, 0, 1, 3)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName("line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 10, 0, 1, 3)

        PreferencesWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(PreferencesWindow)
        self.statusbar.setObjectName("statusbar")
        PreferencesWindow.setStatusBar(self.statusbar)

        self.retranslateUi(PreferencesWindow)

        self.add_push_button.setDefault(False)

        QMetaObject.connectSlotsByName(PreferencesWindow)

    # setupUi

    def retranslateUi(self, PreferencesWindow):
        PreferencesWindow.setWindowTitle(QCoreApplication.translate("PreferencesWindow", "Preferences", None))
        self.select_output_directory_push_button.setText(
            QCoreApplication.translate("PreferencesWindow", "Browse", None)
        )
        self.apply_push_button.setText(QCoreApplication.translate("PreferencesWindow", "Apply", None))
        self.input_directory_label.setText(QCoreApplication.translate("PreferencesWindow", "Input Directory", None))
        self.autostart_check_box.setText(QCoreApplication.translate("PreferencesWindow", "Autostart", None))
        self.clear_output_directory_push_button.setText(QCoreApplication.translate("PreferencesWindow", "Clear", None))
        self.output_directory_label.setText(QCoreApplication.translate("PreferencesWindow", "Output Directory", None))
        self.add_push_button.setText(QCoreApplication.translate("PreferencesWindow", "Add", None))

    # retranslateUi
