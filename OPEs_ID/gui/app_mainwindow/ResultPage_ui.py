# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ResultPage.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QHeaderView,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from ..dataframe_table import DataFrameView

class Ui_ResultPage(object):
    def setupUi(self, ResultPage):
        if not ResultPage.objectName():
            ResultPage.setObjectName(u"ResultPage")
        ResultPage.resize(580, 700)
        self.verticalLayout = QVBoxLayout(ResultPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_5 = QGroupBox(ResultPage)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.resultsTableView = DataFrameView(self.groupBox_5)
        self.resultsTableView.setObjectName(u"resultsTableView")

        self.verticalLayout_4.addWidget(self.resultsTableView)


        self.verticalLayout.addWidget(self.groupBox_5)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.metfragButton = QPushButton(ResultPage)
        self.metfragButton.setObjectName(u"metfragButton")

        self.horizontalLayout_3.addWidget(self.metfragButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.saveButton = QPushButton(ResultPage)
        self.saveButton.setObjectName(u"saveButton")

        self.horizontalLayout_3.addWidget(self.saveButton)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(ResultPage)

        QMetaObject.connectSlotsByName(ResultPage)
    # setupUi

    def retranslateUi(self, ResultPage):
        ResultPage.setWindowTitle(QCoreApplication.translate("ResultPage", u"Form", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("ResultPage", u"Screened out results", None))
        self.metfragButton.setText(QCoreApplication.translate("ResultPage", u"Metfrag Analysis", None))
        self.saveButton.setText(QCoreApplication.translate("ResultPage", u"Save", None))
    # retranslateUi

