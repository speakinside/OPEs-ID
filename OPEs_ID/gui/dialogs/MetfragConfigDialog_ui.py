# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MetfragConfigDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialog, QDialogButtonBox, QGridLayout, QGroupBox,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(340, 545)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_2 = QGroupBox(Dialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout = QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.downloadJavaButton = QPushButton(self.groupBox_2)
        self.downloadJavaButton.setObjectName(u"downloadJavaButton")

        self.gridLayout.addWidget(self.downloadJavaButton, 2, 2, 1, 1)

        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 2)

        self.javaPathEdit = QLineEdit(self.groupBox_2)
        self.javaPathEdit.setObjectName(u"javaPathEdit")

        self.gridLayout.addWidget(self.javaPathEdit, 1, 0, 1, 1)

        self.selectJavaPathButton = QPushButton(self.groupBox_2)
        self.selectJavaPathButton.setObjectName(u"selectJavaPathButton")

        self.gridLayout.addWidget(self.selectJavaPathButton, 1, 2, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(Dialog)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_3 = QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.sysTempDirCheckBox = QCheckBox(self.groupBox_3)
        self.sysTempDirCheckBox.setObjectName(u"sysTempDirCheckBox")

        self.gridLayout_3.addWidget(self.sysTempDirCheckBox, 2, 0, 1, 3)

        self.label_5 = QLabel(self.groupBox_3)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_3.addWidget(self.label_5, 3, 0, 1, 1)

        self.label_8 = QLabel(self.groupBox_3)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_8, 0, 0, 1, 3)

        self.tempDirPath = QLineEdit(self.groupBox_3)
        self.tempDirPath.setObjectName(u"tempDirPath")

        self.gridLayout_3.addWidget(self.tempDirPath, 4, 0, 1, 1)

        self.tempDirButton = QPushButton(self.groupBox_3)
        self.tempDirButton.setObjectName(u"tempDirButton")

        self.gridLayout_3.addWidget(self.tempDirButton, 4, 1, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_3)

        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.dbComboBox = QComboBox(self.groupBox)
        self.dbComboBox.setObjectName(u"dbComboBox")

        self.gridLayout_2.addWidget(self.dbComboBox, 0, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)

        self.dbExtraInfoWidget = QWidget(self.groupBox)
        self.dbExtraInfoWidget.setObjectName(u"dbExtraInfoWidget")
        self.gridLayout_5 = QGridLayout(self.dbExtraInfoWidget)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_9 = QLabel(self.dbExtraInfoWidget)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_5.addWidget(self.label_9, 0, 0, 1, 1)

        self.dbPathEdit = QLineEdit(self.dbExtraInfoWidget)
        self.dbPathEdit.setObjectName(u"dbPathEdit")

        self.gridLayout_5.addWidget(self.dbPathEdit, 1, 0, 1, 1)

        self.selectDBPathButton = QPushButton(self.dbExtraInfoWidget)
        self.selectDBPathButton.setObjectName(u"selectDBPathButton")

        self.gridLayout_5.addWidget(self.selectDBPathButton, 1, 1, 1, 1)


        self.gridLayout_2.addWidget(self.dbExtraInfoWidget, 1, 0, 1, 2)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_4 = QGroupBox(Dialog)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout_4 = QGridLayout(self.groupBox_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.filterTargetIonCheckBox = QCheckBox(self.groupBox_4)
        self.filterTargetIonCheckBox.setObjectName(u"filterTargetIonCheckBox")
        self.filterTargetIonCheckBox.setAcceptDrops(False)
        self.filterTargetIonCheckBox.setChecked(True)

        self.gridLayout_4.addWidget(self.filterTargetIonCheckBox, 1, 1, 1, 1)

        self.maxTreeDepthSpinBox = QSpinBox(self.groupBox_4)
        self.maxTreeDepthSpinBox.setObjectName(u"maxTreeDepthSpinBox")
        self.maxTreeDepthSpinBox.setMinimum(1)
        self.maxTreeDepthSpinBox.setValue(2)

        self.gridLayout_4.addWidget(self.maxTreeDepthSpinBox, 0, 1, 1, 1)

        self.label_7 = QLabel(self.groupBox_4)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_4.addWidget(self.label_7, 1, 0, 1, 1)

        self.label_6 = QLabel(self.groupBox_4)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_4.addWidget(self.label_6, 0, 0, 1, 1)

        self.filterEsterTypeCheckBox = QCheckBox(self.groupBox_4)
        self.filterEsterTypeCheckBox.setObjectName(u"filterEsterTypeCheckBox")
        self.filterEsterTypeCheckBox.setChecked(True)

        self.gridLayout_4.addWidget(self.filterEsterTypeCheckBox, 2, 1, 1, 1)

        self.label_10 = QLabel(self.groupBox_4)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_4.addWidget(self.label_10, 2, 0, 1, 1)

        self.label_3 = QLabel(self.groupBox_4)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_4.addWidget(self.label_3, 3, 0, 1, 1)

        self.nJobSpinBox = QSpinBox(self.groupBox_4)
        self.nJobSpinBox.setObjectName(u"nJobSpinBox")
        self.nJobSpinBox.setMinimum(1)

        self.gridLayout_4.addWidget(self.nJobSpinBox, 3, 1, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_4)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"Java config", None))
        self.downloadJavaButton.setText(QCoreApplication.translate("Dialog", u"Downlaod", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Java Path:", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Metfrag needs jdk11 to run.", None))
        self.selectJavaPathButton.setText(QCoreApplication.translate("Dialog", u"Select", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Dialog", u"Temp Directory", None))
        self.sysTempDirCheckBox.setText(QCoreApplication.translate("Dialog", u"Use System Temp Directory", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Directory Path:", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Directory for storing temp files.", None))
        self.tempDirButton.setText(QCoreApplication.translate("Dialog", u"Select", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Database", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Source:", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Local Path:", None))
        self.selectDBPathButton.setText(QCoreApplication.translate("Dialog", u"Select", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Dialog", u"Metfrag config", None))
        self.filterTargetIonCheckBox.setText("")
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Targe Ion Filter:", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"MaximumTreeDepth:", None))
        self.filterEsterTypeCheckBox.setText("")
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Tri/di/mono Filter:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Multiple Job:", None))
    # retranslateUi

