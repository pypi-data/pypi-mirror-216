# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'input_directory_entry_widget.ui'
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
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLineEdit, QPushButton, QSizePolicy, QWidget


class Ui_InputDirectoryEntryWidget(object):
    def setupUi(self, InputDirectoryEntryWidget):
        if not InputDirectoryEntryWidget.objectName():
            InputDirectoryEntryWidget.setObjectName("InputDirectoryEntryWidget")
        InputDirectoryEntryWidget.resize(400, 300)
        self.horizontalLayout = QHBoxLayout(InputDirectoryEntryWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.directory_line_edit = QLineEdit(InputDirectoryEntryWidget)
        self.directory_line_edit.setObjectName("directory_line_edit")

        self.horizontalLayout.addWidget(self.directory_line_edit)

        self.select_directory_push_button = QPushButton(InputDirectoryEntryWidget)
        self.select_directory_push_button.setObjectName("select_directory_push_button")

        self.horizontalLayout.addWidget(self.select_directory_push_button)

        self.remove_directory_push_button = QPushButton(InputDirectoryEntryWidget)
        self.remove_directory_push_button.setObjectName("remove_directory_push_button")

        self.horizontalLayout.addWidget(self.remove_directory_push_button)

        self.retranslateUi(InputDirectoryEntryWidget)

        QMetaObject.connectSlotsByName(InputDirectoryEntryWidget)

    # setupUi

    def retranslateUi(self, InputDirectoryEntryWidget):
        InputDirectoryEntryWidget.setWindowTitle(QCoreApplication.translate("InputDirectoryEntryWidget", "Form", None))
        self.select_directory_push_button.setText(
            QCoreApplication.translate("InputDirectoryEntryWidget", "Browse", None)
        )
        self.remove_directory_push_button.setText(
            QCoreApplication.translate("InputDirectoryEntryWidget", "Remove", None)
        )

    # retranslateUi
