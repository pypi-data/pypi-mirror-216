# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preferences_widget.ui'
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
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class Ui_PreferencesWidget(object):
    def setupUi(self, PreferencesWidget):
        if not PreferencesWidget.objectName():
            PreferencesWidget.setObjectName("PreferencesWidget")
        PreferencesWidget.resize(1492, 669)
        self.gridLayout = QGridLayout(PreferencesWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.input_directory_label = QLabel(PreferencesWidget)
        self.input_directory_label.setObjectName("input_directory_label")

        self.gridLayout.addWidget(self.input_directory_label, 4, 1, 1, 1)

        self.select_output_directory_push_button = QPushButton(PreferencesWidget)
        self.select_output_directory_push_button.setObjectName("select_output_directory_push_button")

        self.gridLayout.addWidget(self.select_output_directory_push_button, 10, 2, 1, 1)

        self.apply_push_button = QPushButton(PreferencesWidget)
        self.apply_push_button.setObjectName("apply_push_button")

        self.gridLayout.addWidget(self.apply_push_button, 13, 1, 1, 3)

        self.line = QFrame(PreferencesWidget)
        self.line.setObjectName("line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 8, 1, 1, 3)

        self.output_directory_line_edit = QLineEdit(PreferencesWidget)
        self.output_directory_line_edit.setObjectName("output_directory_line_edit")

        self.gridLayout.addWidget(self.output_directory_line_edit, 10, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 462, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 7, 1, 1, 1)

        self.add_push_button = QPushButton(PreferencesWidget)
        self.add_push_button.setObjectName("add_push_button")
        self.add_push_button.setFlat(False)

        self.gridLayout.addWidget(self.add_push_button, 6, 1, 1, 3)

        self.clear_output_directory_push_button = QPushButton(PreferencesWidget)
        self.clear_output_directory_push_button.setObjectName("clear_output_directory_push_button")

        self.gridLayout.addWidget(self.clear_output_directory_push_button, 10, 3, 1, 1)

        self.line_2 = QFrame(PreferencesWidget)
        self.line_2.setObjectName("line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_2, 11, 1, 1, 3)

        self.output_directory_label = QLabel(PreferencesWidget)
        self.output_directory_label.setObjectName("output_directory_label")

        self.gridLayout.addWidget(self.output_directory_label, 9, 1, 1, 1)

        self.autostart_check_box = QCheckBox(PreferencesWidget)
        self.autostart_check_box.setObjectName("autostart_check_box")

        self.gridLayout.addWidget(self.autostart_check_box, 12, 1, 1, 1)

        self.input_directories_vertical_layout = QVBoxLayout()
        self.input_directories_vertical_layout.setSpacing(1)
        self.input_directories_vertical_layout.setObjectName("input_directories_vertical_layout")

        self.gridLayout.addLayout(self.input_directories_vertical_layout, 5, 1, 1, 3)

        self.retranslateUi(PreferencesWidget)

        self.add_push_button.setDefault(False)

        QMetaObject.connectSlotsByName(PreferencesWidget)

    # setupUi

    def retranslateUi(self, PreferencesWidget):
        PreferencesWidget.setWindowTitle(QCoreApplication.translate("PreferencesWidget", "Form", None))
        self.input_directory_label.setText(QCoreApplication.translate("PreferencesWidget", "Input Directory", None))
        self.select_output_directory_push_button.setText(
            QCoreApplication.translate("PreferencesWidget", "Browse", None)
        )
        self.apply_push_button.setText(QCoreApplication.translate("PreferencesWidget", "Apply", None))
        self.add_push_button.setText(QCoreApplication.translate("PreferencesWidget", "Add", None))
        self.clear_output_directory_push_button.setText(QCoreApplication.translate("PreferencesWidget", "Clear", None))
        self.output_directory_label.setText(QCoreApplication.translate("PreferencesWidget", "Output Directory", None))
        self.autostart_check_box.setText(QCoreApplication.translate("PreferencesWidget", "Autostart", None))

    # retranslateUi
