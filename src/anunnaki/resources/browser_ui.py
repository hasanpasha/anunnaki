# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'browser.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QListView,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(669, 544)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.popular = QPushButton(Form)
        self.popular.setObjectName(u"popular")

        self.horizontalLayout.addWidget(self.popular)

        self.recent = QPushButton(Form)
        self.recent.setObjectName(u"recent")

        self.horizontalLayout.addWidget(self.recent)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.browse_list = QListWidget(Form)
        self.browse_list.setObjectName(u"browse_list")
        self.browse_list.setProperty("showDropIndicator", False)
        self.browse_list.setDragDropMode(QAbstractItemView.InternalMove)
        self.browse_list.setDefaultDropAction(Qt.IgnoreAction)
        self.browse_list.setMovement(QListView.Free)
        self.browse_list.setFlow(QListView.LeftToRight)
        self.browse_list.setViewMode(QListView.ListMode)

        self.verticalLayout.addWidget(self.browse_list)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.popular.setText(QCoreApplication.translate("Form", u"Popular", None))
        self.recent.setText(QCoreApplication.translate("Form", u"Recent", None))
    # retranslateUi

