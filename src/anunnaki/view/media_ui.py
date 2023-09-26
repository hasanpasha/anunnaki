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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QStackedWidget, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_media_widget(object):
    def setupUi(self, media_widget):
        if not media_widget.objectName():
            media_widget.setObjectName(u"media_widget")
        media_widget.resize(1247, 915)
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
        self.scrollArea = QScrollArea(self.media_main)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 1227, 895))
        self.verticalLayout_9 = QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.player_stack = QStackedWidget(self.scrollAreaWidgetContents_3)
        self.player_stack.setObjectName(u"player_stack")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.player_stack.sizePolicy().hasHeightForWidth())
        self.player_stack.setSizePolicy(sizePolicy)
        self.player_stack.setMinimumSize(QSize(640, 480))
        self.player_stack.setFrameShape(QFrame.WinPanel)

        self.verticalLayout_9.addWidget(self.player_stack)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.poster = QLabel(self.scrollAreaWidgetContents_3)
        self.poster.setObjectName(u"poster")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.poster.sizePolicy().hasHeightForWidth())
        self.poster.setSizePolicy(sizePolicy1)
        self.poster.setMinimumSize(QSize(210, 300))
        self.poster.setFrameShape(QFrame.Panel)
        self.poster.setFrameShadow(QFrame.Raised)
        self.poster.setText(u"")
        self.poster.setScaledContents(True)
        self.poster.setTextInteractionFlags(Qt.NoTextInteraction)

        self.verticalLayout.addWidget(self.poster)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.title_lbl = QLabel(self.scrollAreaWidgetContents_3)
        self.title_lbl.setObjectName(u"title_lbl")
        font = QFont()
        font.setPointSize(18)
        self.title_lbl.setFont(font)
        self.title_lbl.setAlignment(Qt.AlignCenter)
        self.title_lbl.setWordWrap(True)
        self.title_lbl.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.verticalLayout_11.addWidget(self.title_lbl)

        self.story_lbl = QLabel(self.scrollAreaWidgetContents_3)
        self.story_lbl.setObjectName(u"story_lbl")
        self.story_lbl.setWordWrap(True)
        self.story_lbl.setTextInteractionFlags(Qt.TextBrowserInteraction)

        self.verticalLayout_11.addWidget(self.story_lbl)

        self.tags_lbl = QLabel(self.scrollAreaWidgetContents_3)
        self.tags_lbl.setObjectName(u"tags_lbl")

        self.verticalLayout_11.addWidget(self.tags_lbl)

        self.play_btn = QPushButton(self.scrollAreaWidgetContents_3)
        self.play_btn.setObjectName(u"play_btn")
        self.play_btn.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.play_btn.sizePolicy().hasHeightForWidth())
        self.play_btn.setSizePolicy(sizePolicy1)
        self.play_btn.setMinimumSize(QSize(200, 50))
        self.play_btn.setMaximumSize(QSize(200, 50))
        font1 = QFont()
        font1.setPointSize(16)
        self.play_btn.setFont(font1)
        self.play_btn.setAutoDefault(True)
        self.play_btn.setFlat(False)

        self.verticalLayout_11.addWidget(self.play_btn)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.verticalLayout_11.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addLayout(self.verticalLayout_11)

        self.seasons_tabs = QTabWidget(self.scrollAreaWidgetContents_3)
        self.seasons_tabs.setObjectName(u"seasons_tabs")

        self.horizontalLayout_2.addWidget(self.seasons_tabs)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)


        self.verticalLayout_10.addLayout(self.horizontalLayout_2)


        self.verticalLayout_9.addLayout(self.verticalLayout_10)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_3)

        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.media_stack.addWidget(self.media_main)

        self.verticalLayout_2.addWidget(self.media_stack)


        self.retranslateUi(media_widget)

        self.media_stack.setCurrentIndex(0)
        self.play_btn.setDefault(False)


        QMetaObject.connectSlotsByName(media_widget)
    # setupUi

    def retranslateUi(self, media_widget):
        media_widget.setWindowTitle(QCoreApplication.translate("media_widget", u"Form", None))
        self.title_lbl.setText("")
        self.story_lbl.setText("")
        self.tags_lbl.setText("")
        self.play_btn.setText(QCoreApplication.translate("media_widget", u"play", None))
#if QT_CONFIG(shortcut)
        self.play_btn.setShortcut(QCoreApplication.translate("media_widget", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

