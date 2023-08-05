# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'status_widget.ui'
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
    QGridLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSizePolicy,
    QWidget,
)


class Ui_StatusWidget(object):
    def setupUi(self, StatusWidget):
        if not StatusWidget.objectName():
            StatusWidget.setObjectName("StatusWidget")
        StatusWidget.resize(400, 300)
        self.gridLayout = QGridLayout(StatusWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QLabel(StatusWidget)
        self.label.setObjectName("label")

        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)

        self.processedFilesListWidget = QListWidget(StatusWidget)
        self.processedFilesListWidget.setObjectName("processedFilesListWidget")

        self.gridLayout.addWidget(self.processedFilesListWidget, 1, 0, 1, 1)

        self.cachedFilesListWidget = QListWidget(StatusWidget)
        self.cachedFilesListWidget.setObjectName("cachedFilesListWidget")

        self.gridLayout.addWidget(self.cachedFilesListWidget, 1, 1, 1, 1)

        self.label_2 = QLabel(StatusWidget)
        self.label_2.setObjectName("label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.flushCachePushButton = QPushButton(StatusWidget)
        self.flushCachePushButton.setObjectName("flushCachePushButton")

        self.gridLayout.addWidget(self.flushCachePushButton, 2, 1, 1, 1)

        self.retranslateUi(StatusWidget)

        QMetaObject.connectSlotsByName(StatusWidget)

    # setupUi

    def retranslateUi(self, StatusWidget):
        StatusWidget.setWindowTitle(QCoreApplication.translate("StatusWidget", "Form", None))
        self.label.setText(QCoreApplication.translate("StatusWidget", "Cached Files", None))
        self.label_2.setText(QCoreApplication.translate("StatusWidget", "Processed Files", None))
        self.flushCachePushButton.setText(QCoreApplication.translate("StatusWidget", "Flush Cache", None))

    # retranslateUi
