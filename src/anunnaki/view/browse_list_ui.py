# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'browse_list.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QListView, QListWidget,
    QListWidgetItem, QSizePolicy, QVBoxLayout, QWidget)

class Ui_list_widget(object):
    def setupUi(self, list_widget):
        if not list_widget.objectName():
            list_widget.setObjectName(u"list_widget")
        list_widget.resize(400, 300)
        self.verticalLayout = QVBoxLayout(list_widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.browse_list = QListWidget(list_widget)
        self.browse_list.setObjectName(u"browse_list")
        self.browse_list.setProperty("showDropIndicator", False)
        self.browse_list.setDragDropMode(QAbstractItemView.InternalMove)
        self.browse_list.setDefaultDropAction(Qt.IgnoreAction)
        self.browse_list.setMovement(QListView.Free)
        self.browse_list.setFlow(QListView.LeftToRight)
        self.browse_list.setProperty("isWrapping", True)
        self.browse_list.setResizeMode(QListView.Adjust)
        self.browse_list.setViewMode(QListView.ListMode)

        self.verticalLayout.addWidget(self.browse_list)


        self.retranslateUi(list_widget)

        QMetaObject.connectSlotsByName(list_widget)
    # setupUi

    def retranslateUi(self, list_widget):
        list_widget.setWindowTitle(QCoreApplication.translate("list_widget", u"Form", None))
    # retranslateUi

