# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'browse.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLineEdit, QPushButton,
    QSizePolicy, QTabWidget, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(669, 544)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 5, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, 6, 9, 5)
        self.search_line = QLineEdit(Form)
        self.search_line.setObjectName(u"search_line")

        self.horizontalLayout.addWidget(self.search_line)

        self.search_btn = QPushButton(Form)
        self.search_btn.setObjectName(u"search_btn")

        self.horizontalLayout.addWidget(self.search_btn)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.browse_tabs = QTabWidget(Form)
        self.browse_tabs.setObjectName(u"browse_tabs")
        self.popular = QWidget()
        self.popular.setObjectName(u"popular")
        self.verticalLayout_3 = QVBoxLayout(self.popular)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.popular_layout = QVBoxLayout()
        self.popular_layout.setSpacing(0)
        self.popular_layout.setObjectName(u"popular_layout")

        self.verticalLayout_3.addLayout(self.popular_layout)

        self.browse_tabs.addTab(self.popular, "")
        self.search = QWidget()
        self.search.setObjectName(u"search")
        self.verticalLayout_4 = QVBoxLayout(self.search)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.search_layout = QVBoxLayout()
        self.search_layout.setSpacing(0)
        self.search_layout.setObjectName(u"search_layout")

        self.verticalLayout_4.addLayout(self.search_layout)

        self.browse_tabs.addTab(self.search, "")
        self.latest = QWidget()
        self.latest.setObjectName(u"latest")
        self.verticalLayout_2 = QVBoxLayout(self.latest)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.latest_layout = QVBoxLayout()
        self.latest_layout.setSpacing(0)
        self.latest_layout.setObjectName(u"latest_layout")

        self.verticalLayout_2.addLayout(self.latest_layout)

        self.browse_tabs.addTab(self.latest, "")

        self.verticalLayout.addWidget(self.browse_tabs)


        self.retranslateUi(Form)

        self.browse_tabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.search_btn.setText(QCoreApplication.translate("Form", u"search", None))
        self.browse_tabs.setTabText(self.browse_tabs.indexOf(self.popular), QCoreApplication.translate("Form", u"Popular", None))
        self.browse_tabs.setTabText(self.browse_tabs.indexOf(self.search), QCoreApplication.translate("Form", u"Search", None))
        self.browse_tabs.setTabText(self.browse_tabs.indexOf(self.latest), QCoreApplication.translate("Form", u"Latest", None))
    # retranslateUi

