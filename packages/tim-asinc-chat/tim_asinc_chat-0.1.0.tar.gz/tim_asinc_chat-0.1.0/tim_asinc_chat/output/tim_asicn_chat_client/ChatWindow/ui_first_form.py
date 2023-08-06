# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'first_formujyvzk.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFormLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(568, 373)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(240, 10, 141, 41))
        font = QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.register_button = QPushButton(Dialog)
        self.register_button.setObjectName(u"register_button")
        self.register_button.setEnabled(False)
        self.register_button.setGeometry(QRect(80, 220, 75, 24))
        self.join_chat_button = QPushButton(Dialog)
        self.join_chat_button.setObjectName(u"join_chat_button")
        self.join_chat_button.setEnabled(False)
        self.join_chat_button.setGeometry(QRect(400, 220, 75, 24))
        self.formLayoutWidget = QWidget(Dialog)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(320, 110, 231, 51))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.loginLabel = QLabel(self.formLayoutWidget)
        self.loginLabel.setObjectName(u"loginLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.loginLabel)

        self.loginLineEdit = QLineEdit(self.formLayoutWidget)
        self.loginLineEdit.setObjectName(u"loginLineEdit")
        self.loginLineEdit.setEnabled(False)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.loginLineEdit)

        self.passwordLabel = QLabel(self.formLayoutWidget)
        self.passwordLabel.setObjectName(u"passwordLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.passwordLabel)

        self.passwordLineEdit = QLineEdit(self.formLayoutWidget)
        self.passwordLineEdit.setObjectName(u"passwordLineEdit")
        self.passwordLineEdit.setEnabled(False)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.passwordLineEdit)

        self.formLayoutWidget_2 = QWidget(Dialog)
        self.formLayoutWidget_2.setObjectName(u"formLayoutWidget_2")
        self.formLayoutWidget_2.setGeometry(QRect(20, 110, 261, 81))
        self.formLayout_2 = QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.loginLabel_2 = QLabel(self.formLayoutWidget_2)
        self.loginLabel_2.setObjectName(u"loginLabel_2")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.loginLabel_2)

        self.loginLineEdit_2 = QLineEdit(self.formLayoutWidget_2)
        self.loginLineEdit_2.setObjectName(u"loginLineEdit_2")
        self.loginLineEdit_2.setEnabled(False)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.loginLineEdit_2)

        self.passwordLabel_2 = QLabel(self.formLayoutWidget_2)
        self.passwordLabel_2.setObjectName(u"passwordLabel_2")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.passwordLabel_2)

        self.passwordLineEdit_2 = QLineEdit(self.formLayoutWidget_2)
        self.passwordLineEdit_2.setObjectName(u"passwordLineEdit_2")
        self.passwordLineEdit_2.setEnabled(False)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.passwordLineEdit_2)

        self.confrimPasswordLabel = QLabel(self.formLayoutWidget_2)
        self.confrimPasswordLabel.setObjectName(u"confrimPasswordLabel")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.confrimPasswordLabel)

        self.confrimPasswordLineEdit = QLineEdit(self.formLayoutWidget_2)
        self.confrimPasswordLineEdit.setObjectName(u"confrimPasswordLineEdit")
        self.confrimPasswordLineEdit.setEnabled(False)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.confrimPasswordLineEdit)

        self.checkBox_new_user = QCheckBox(Dialog)
        self.checkBox_new_user.setObjectName(u"checkBox_new_user")
        self.checkBox_new_user.setGeometry(QRect(90, 60, 75, 20))
        self.checkBox_exist_user = QCheckBox(Dialog)
        self.checkBox_exist_user.setObjectName(u"checkBox_exist_user")
        self.checkBox_exist_user.setGeometry(QRect(380, 60, 75, 20))
        self.pushButton_exit = QPushButton(Dialog)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        self.pushButton_exit.setGeometry(QRect(450, 330, 75, 24))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Hello, user!", None))
        self.register_button.setText(QCoreApplication.translate("Dialog", u"Register", None))
        self.join_chat_button.setText(QCoreApplication.translate("Dialog", u"Join Chat!", None))
        self.loginLabel.setText(QCoreApplication.translate("Dialog", u"Login:", None))
        self.passwordLabel.setText(QCoreApplication.translate("Dialog", u"Password:", None))
        self.loginLabel_2.setText(QCoreApplication.translate("Dialog", u"Login:", None))
        self.passwordLabel_2.setText(QCoreApplication.translate("Dialog", u"Password:", None))
        self.confrimPasswordLabel.setText(QCoreApplication.translate("Dialog", u"Confrim password", None))
        self.checkBox_new_user.setText(QCoreApplication.translate("Dialog", u"New user", None))
        self.checkBox_exist_user.setText(QCoreApplication.translate("Dialog", u"Exists user", None))
        self.pushButton_exit.setText(QCoreApplication.translate("Dialog", u"Exit", None))
    # retranslateUi

