# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ConfigPage.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QGroupBox,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

from ..dataframe_table import DataFrameView

class Ui_ConfigPage(object):
    def setupUi(self, ConfigPage):
        if not ConfigPage.objectName():
            ConfigPage.setObjectName(u"ConfigPage")
        ConfigPage.resize(580, 700)
        self.verticalLayout_2 = QVBoxLayout(ConfigPage)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.fileGroupBox = QGroupBox(ConfigPage)
        self.fileGroupBox.setObjectName(u"fileGroupBox")
        self.gridLayout = QGridLayout(self.fileGroupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.selectNegPath = QPushButton(self.fileGroupBox)
        self.selectNegPath.setObjectName(u"selectNegPath")

        self.gridLayout.addWidget(self.selectNegPath, 3, 2, 1, 1)

        self.label_2 = QLabel(self.fileGroupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)

        self.negFilePath = QLineEdit(self.fileGroupBox)
        self.negFilePath.setObjectName(u"negFilePath")

        self.gridLayout.addWidget(self.negFilePath, 3, 1, 1, 1)

        self.posFilePath = QLineEdit(self.fileGroupBox)
        self.posFilePath.setObjectName(u"posFilePath")

        self.gridLayout.addWidget(self.posFilePath, 1, 1, 1, 1)

        self.label = QLabel(self.fileGroupBox)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.selectPosPath = QPushButton(self.fileGroupBox)
        self.selectPosPath.setObjectName(u"selectPosPath")

        self.gridLayout.addWidget(self.selectPosPath, 1, 2, 1, 1)


        self.verticalLayout_2.addWidget(self.fileGroupBox)

        self.groupBox_3 = QGroupBox(ConfigPage)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_3 = QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.groupBox_2 = QGroupBox(self.groupBox_3)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.ms2FilterAccLineEdit = QLineEdit(self.groupBox_2)
        self.ms2FilterAccLineEdit.setObjectName(u"ms2FilterAccLineEdit")

        self.gridLayout_2.addWidget(self.ms2FilterAccLineEdit, 1, 1, 1, 2)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)

        self.ROIAccLineEdit = QLineEdit(self.groupBox_2)
        self.ROIAccLineEdit.setObjectName(u"ROIAccLineEdit")

        self.gridLayout_2.addWidget(self.ROIAccLineEdit, 2, 1, 1, 2)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox_2, 0, 0, 1, 1)

        self.groupBox = QGroupBox(self.groupBox_3)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.targetIonTableView = DataFrameView(self.groupBox)
        self.targetIonTableView.setObjectName(u"targetIonTableView")
        self.targetIonTableView.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.targetIonTableView.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.verticalLayout.addWidget(self.targetIonTableView)


        self.gridLayout_3.addWidget(self.groupBox, 1, 0, 1, 3)

        self.groupBox_4 = QGroupBox(self.groupBox_3)
        self.groupBox_4.setObjectName(u"groupBox_4")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy1)
        self.gridLayout_4 = QGridLayout(self.groupBox_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_5 = QLabel(self.groupBox_4)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_4.addWidget(self.label_5, 0, 0, 1, 1)

        self.IsoClRangeLineEdit = QLineEdit(self.groupBox_4)
        self.IsoClRangeLineEdit.setObjectName(u"IsoClRangeLineEdit")

        self.gridLayout_4.addWidget(self.IsoClRangeLineEdit, 0, 1, 1, 1)

        self.label_7 = QLabel(self.groupBox_4)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_4.addWidget(self.label_7, 1, 0, 1, 1)

        self.IsoTopNLineEdit = QLineEdit(self.groupBox_4)
        self.IsoTopNLineEdit.setObjectName(u"IsoTopNLineEdit")

        self.gridLayout_4.addWidget(self.IsoTopNLineEdit, 1, 1, 1, 1)

        self.label_6 = QLabel(self.groupBox_4)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_4.addWidget(self.label_6, 0, 2, 1, 1)

        self.IsoMassAccLineEdit = QLineEdit(self.groupBox_4)
        self.IsoMassAccLineEdit.setObjectName(u"IsoMassAccLineEdit")

        self.gridLayout_4.addWidget(self.IsoMassAccLineEdit, 0, 3, 1, 1)

        self.label_8 = QLabel(self.groupBox_4)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_4.addWidget(self.label_8, 1, 2, 1, 1)

        self.formulaConfigButton = QPushButton(self.groupBox_4)
        self.formulaConfigButton.setObjectName(u"formulaConfigButton")

        self.gridLayout_4.addWidget(self.formulaConfigButton, 1, 3, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox_4, 0, 2, 1, 1)


        self.verticalLayout_2.addWidget(self.groupBox_3)

        self.calButton = QPushButton(ConfigPage)
        self.calButton.setObjectName(u"calButton")

        self.verticalLayout_2.addWidget(self.calButton)


        self.retranslateUi(ConfigPage)

        QMetaObject.connectSlotsByName(ConfigPage)
    # setupUi

    def retranslateUi(self, ConfigPage):
        ConfigPage.setWindowTitle(QCoreApplication.translate("ConfigPage", u"Form", None))
        self.fileGroupBox.setTitle(QCoreApplication.translate("ConfigPage", u"File", None))
        self.selectNegPath.setText(QCoreApplication.translate("ConfigPage", u"Select", None))
        self.label_2.setText(QCoreApplication.translate("ConfigPage", u"Negative mode LC-MS/MS:", None))
        self.label.setText(QCoreApplication.translate("ConfigPage", u"Positive mode LC-MS/MS:", None))
        self.selectPosPath.setText(QCoreApplication.translate("ConfigPage", u"Select", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("ConfigPage", u"Config", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("ConfigPage", u"Target ion in MS/MS ", None))
        self.ms2FilterAccLineEdit.setText(QCoreApplication.translate("ConfigPage", u"20e-6", None))
        self.label_3.setText(QCoreApplication.translate("ConfigPage", u"MS2 ACC", None))
        self.ROIAccLineEdit.setText(QCoreApplication.translate("ConfigPage", u"20e-6", None))
        self.label_4.setText(QCoreApplication.translate("ConfigPage", u"ROI ACC", None))
        self.groupBox.setTitle(QCoreApplication.translate("ConfigPage", u"Target ion list", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("ConfigPage", u"formula", None))
        self.label_5.setText(QCoreApplication.translate("ConfigPage", u"Cl range", None))
        self.IsoClRangeLineEdit.setText(QCoreApplication.translate("ConfigPage", u"0-10", None))
        self.label_7.setText(QCoreApplication.translate("ConfigPage", u"Top n:", None))
        self.IsoTopNLineEdit.setText(QCoreApplication.translate("ConfigPage", u"5", None))
        self.label_6.setText(QCoreApplication.translate("ConfigPage", u"Mass acc:", None))
        self.IsoMassAccLineEdit.setText(QCoreApplication.translate("ConfigPage", u"5e-6", None))
        self.label_8.setText(QCoreApplication.translate("ConfigPage", u"Formula Prediction:", None))
        self.formulaConfigButton.setText(QCoreApplication.translate("ConfigPage", u"config", None))
        self.calButton.setText(QCoreApplication.translate("ConfigPage", u"Calculate", None))
    # retranslateUi

