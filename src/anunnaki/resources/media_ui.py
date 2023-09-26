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
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QTabWidget, QVBoxLayout,
    QWidget)

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
        self.media_main_layout = QGridLayout()
        self.media_main_layout.setObjectName(u"media_main_layout")
        self.poster = QLabel(self.media_main)
        self.poster.setObjectName(u"poster")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.poster.sizePolicy().hasHeightForWidth())
        self.poster.setSizePolicy(sizePolicy)
        self.poster.setMinimumSize(QSize(210, 300))
        self.poster.setFrameShape(QFrame.Panel)
        self.poster.setFrameShadow(QFrame.Raised)
        self.poster.setText(u"")
        self.poster.setScaledContents(True)
        self.poster.setTextInteractionFlags(Qt.NoTextInteraction)

        self.media_main_layout.addWidget(self.poster, 0, 0, 1, 1)

        self.seasons_tabs = QTabWidget(self.media_main)
        self.seasons_tabs.setObjectName(u"seasons_tabs")

        self.media_main_layout.addWidget(self.seasons_tabs, 0, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.media_main_layout.addItem(self.verticalSpacer, 5, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.media_main_layout.addItem(self.horizontalSpacer, 4, 1, 1, 1)

        self.info_layout = QFormLayout()
        self.info_layout.setObjectName(u"info_layout")

        self.media_main_layout.addLayout(self.info_layout, 4, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.play_btn = QPushButton(self.media_main)
        self.play_btn.setObjectName(u"play_btn")
        self.play_btn.setEnabled(False)

        self.horizontalLayout.addWidget(self.play_btn)


        self.media_main_layout.addLayout(self.horizontalLayout, 4, 2, 1, 1)


        self.gridLayout_2.addLayout(self.media_main_layout, 0, 0, 1, 1)

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

        self.media_stack.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(media_widget)
    # setupUi

    def retranslateUi(self, media_widget):
        media_widget.setWindowTitle(QCoreApplication.translate("media_widget", u"Form", None))
        self.play_btn.setText(QCoreApplication.translate("media_widget", u"Play", None))
    # retranslateUi

