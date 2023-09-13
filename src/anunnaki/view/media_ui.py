# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'media.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QSizePolicy, QStackedWidget,
    QVBoxLayout, QWidget)

class Ui_media_widget(object):
    def setupUi(self, media_widget):
        if not media_widget.objectName():
            media_widget.setObjectName(u"media_widget")
        media_widget.resize(760, 526)
        self.verticalLayout_2 = QVBoxLayout(media_widget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.media_stack = QStackedWidget(media_widget)
        self.media_stack.setObjectName(u"media_stack")
        self.media_main = QWidget()
        self.media_main.setObjectName(u"media_main")
        self.gridLayout_2 = QGridLayout(self.media_main)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.media_stack.addWidget(self.media_main)
        self.media_player = QWidget()
        self.media_player.setObjectName(u"media_player")
        self.verticalLayout_3 = QVBoxLayout(self.media_player)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.media_stack.addWidget(self.media_player)

        self.verticalLayout_2.addWidget(self.media_stack)


        self.retranslateUi(media_widget)

        QMetaObject.connectSlotsByName(media_widget)
    # setupUi

    def retranslateUi(self, media_widget):
        media_widget.setWindowTitle(QCoreApplication.translate("media_widget", u"Form", None))
    # retranslateUi

