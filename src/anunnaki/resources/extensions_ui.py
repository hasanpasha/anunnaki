# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'extensions.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_ext_widget(object):
    def setupUi(self, ext_widget):
        if not ext_widget.objectName():
            ext_widget.setObjectName(u"ext_widget")
        ext_widget.resize(684, 472)
        self.verticalLayout = QVBoxLayout(ext_widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.ext_tabs = QTabWidget(ext_widget)
        self.ext_tabs.setObjectName(u"ext_tabs")
        self.ext_tabs.setTabPosition(QTabWidget.North)
        self.ext_tabs.setUsesScrollButtons(True)
        self.ext_sources = QWidget()
        self.ext_sources.setObjectName(u"ext_sources")
        self.verticalLayout_3 = QVBoxLayout(self.ext_sources)
        self.verticalLayout_3.setSpacing(8)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(8, 8, 8, 8)
        self.sources_list = QListWidget(self.ext_sources)
        self.sources_list.setObjectName(u"sources_list")

        self.verticalLayout_3.addWidget(self.sources_list)

        self.ext_tabs.addTab(self.ext_sources, "")
        self.ext_extensions = QWidget()
        self.ext_extensions.setObjectName(u"ext_extensions")
        self.verticalLayout_2 = QVBoxLayout(self.ext_extensions)
        self.verticalLayout_2.setSpacing(8)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(8, 8, 8, 8)
        self.extensions_list = QListWidget(self.ext_extensions)
        self.extensions_list.setObjectName(u"extensions_list")

        self.verticalLayout_2.addWidget(self.extensions_list)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.ext_install = QPushButton(self.ext_extensions)
        self.ext_install.setObjectName(u"ext_install")
        self.ext_install.setEnabled(False)

        self.horizontalLayout.addWidget(self.ext_install)

        self.ext_uninstall = QPushButton(self.ext_extensions)
        self.ext_uninstall.setObjectName(u"ext_uninstall")
        self.ext_uninstall.setEnabled(False)

        self.horizontalLayout.addWidget(self.ext_uninstall)

        self.ext_update = QPushButton(self.ext_extensions)
        self.ext_update.setObjectName(u"ext_update")
        self.ext_update.setEnabled(False)

        self.horizontalLayout.addWidget(self.ext_update)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.ext_refresh = QPushButton(self.ext_extensions)
        self.ext_refresh.setObjectName(u"ext_refresh")

        self.horizontalLayout.addWidget(self.ext_refresh)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.ext_tabs.addTab(self.ext_extensions, "")

        self.verticalLayout.addWidget(self.ext_tabs)


        self.retranslateUi(ext_widget)

        self.ext_tabs.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(ext_widget)
    # setupUi

    def retranslateUi(self, ext_widget):
        ext_widget.setWindowTitle(QCoreApplication.translate("ext_widget", u"Form", None))
        self.ext_tabs.setTabText(self.ext_tabs.indexOf(self.ext_sources), QCoreApplication.translate("ext_widget", u"sources", None))
        self.ext_install.setText(QCoreApplication.translate("ext_widget", u"install", None))
        self.ext_uninstall.setText(QCoreApplication.translate("ext_widget", u"uninstall", None))
        self.ext_update.setText(QCoreApplication.translate("ext_widget", u"update", None))
        self.ext_refresh.setText(QCoreApplication.translate("ext_widget", u"refresh", None))
        self.ext_tabs.setTabText(self.ext_tabs.indexOf(self.ext_extensions), QCoreApplication.translate("ext_widget", u"extensions", None))
    # retranslateUi

