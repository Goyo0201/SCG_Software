# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Login.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from CapaPresentacion.RecursosPresentacion import Login_icons

class Ui_login(object):
    def setupUi(self, login):
        login.setObjectName("login")
        login.setEnabled(True)
        login.resize(1000, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(login.sizePolicy().hasHeightForWidth())
        login.setSizePolicy(sizePolicy)
        login.setMinimumSize(QtCore.QSize(1000, 600))
        login.setMaximumSize(QtCore.QSize(1000, 604))
        login.setStyleSheet("")
        login.setAnimated(True)
        self.centralwidget = QtWidgets.QWidget(login)
        self.centralwidget.setObjectName("centralwidget")
        self.bt_cerrar = QtWidgets.QPushButton(self.centralwidget)
        self.bt_cerrar.setGeometry(QtCore.QRect(900, 520, 81, 51))
        self.bt_cerrar.setMinimumSize(QtCore.QSize(40, 40))
        self.bt_cerrar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bt_cerrar.setStyleSheet("QPushButton {\n"
"    color: rgb(333, 333, 333); /* Color del texto */\n"
"    font: 14pt \"Segoe UI\";\n"
"    background: transparent; /* Fondo transparente */\n"
"    border: none; /* Sin borde */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    color: #FF6704; /* Color del texto al pasar el cursor sobre el botón */\n"
"    background: transparent; /* Fondo transparente */\n"
"    border: none; /* Sin borde */\n"
"}\n"
"QPushButton:focus {\n"
"  color: #FF6704; /* Color del texto al pasar el cursor sobre el botón */\n"
"    background: transparent; /* Fondo transparente */\n"
"    border: none; /* Sin borde */\n"
"}")
        self.bt_cerrar.setObjectName("bt_cerrar")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(550, 210, 60, 60))
        self.frame.setMinimumSize(QtCore.QSize(60, 60))
        self.frame.setMaximumSize(QtCore.QSize(50, 50))
        self.frame.setAutoFillBackground(False)
        self.frame.setStyleSheet("image: url(:/icons/usuario.png);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(550, 330, 60, 60))
        self.frame_2.setMinimumSize(QtCore.QSize(60, 60))
        self.frame_2.setMaximumSize(QtCore.QSize(60, 60))
        self.frame_2.setStyleSheet("image: url(:/icons/bloquear.png);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.bt_ingresar_login = QtWidgets.QPushButton(self.centralwidget)
        self.bt_ingresar_login.setGeometry(QtCore.QRect(640, 430, 211, 51))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.bt_ingresar_login.setFont(font)
        self.bt_ingresar_login.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bt_ingresar_login.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.bt_ingresar_login.setStyleSheet("QPushButton {\n"
"    background-color: #FF6704;  /* Color de fondo */\n"
"    color: rgb(255, 255, 255);\n"
"    border: 1px solid #FF6704;  /* Borde del botón */\n"
"    padding: 5px 10px;  /* Relleno interno */\n"
"    border-radius: 15px;  /* Bordes redondeados */\n"
"    font: 14pt \"Segoe UI\";\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"  font: 14pt \"Segoe UI\";\n"
"  background-color: #000000; \n"
"  border: 1px solid #000000;\n"
"}")
        self.bt_ingresar_login.setObjectName("bt_ingresar_login")
        self.txt_input_contrasea = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_input_contrasea.setGeometry(QtCore.QRect(620, 340, 301, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.txt_input_contrasea.setFont(font)
        self.txt_input_contrasea.setStyleSheet("border-radius: 8px;\n"
"padding-left: 10px;\n"
"padding-top: 5px;    /* Espaciado arriba del texto (opcional) */\n"
"padding-bottom: 5px;/* Espaciado abajo del texto (opcional) */")
        self.txt_input_contrasea.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txt_input_contrasea.setObjectName("txt_input_contrasea")
        self.txt_input_usuario = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_input_usuario.setGeometry(QtCore.QRect(620, 220, 301, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.txt_input_usuario.setFont(font)
        self.txt_input_usuario.setStyleSheet("border-radius: 8px;\n"
"padding-left: 10px;\n"
"padding-top: 5px;    /* Espaciado arriba del texto (opcional) */\n"
"padding-bottom: 5px;/* Espaciado abajo del texto (opcional) */")
        self.txt_input_usuario.setObjectName("txt_input_usuario")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(620, 80, 270, 57))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(25)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.label.setFont(font)
        self.label.setStyleSheet("font: 75 25pt \"Segoe UI\";\n"
"color: #FF6704")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.bt_ver = QtWidgets.QPushButton(self.centralwidget)
        self.bt_ver.setGeometry(QtCore.QRect(930, 350, 30, 30))
        self.bt_ver.setMinimumSize(QtCore.QSize(30, 30))
        self.bt_ver.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.bt_ver.setFont(font)
        self.bt_ver.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bt_ver.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.bt_ver.setStyleSheet("\n"
"\n"
"")
        self.bt_ver.setText("")
        self.bt_ver.setObjectName("bt_ver")
        self.frame_logo = QtWidgets.QFrame(self.centralwidget)
        self.frame_logo.setGeometry(QtCore.QRect(0, 0, 500, 600))
        self.frame_logo.setMinimumSize(QtCore.QSize(500, 600))
        self.frame_logo.setMaximumSize(QtCore.QSize(500, 600))
        self.frame_logo.setSizeIncrement(QtCore.QSize(150, 150))
        self.frame_logo.setBaseSize(QtCore.QSize(150, 150))
        self.frame_logo.setStyleSheet("\n"
"background-color: #000000\n"
"")
        self.frame_logo.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_logo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_logo.setObjectName("frame_logo")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.frame_logo)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 130, 391, 341))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_3 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.frame_3.setStyleSheet("image: url(:/icons/logo.jpeg);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout.addWidget(self.frame_3)
        login.setCentralWidget(self.centralwidget)

        self.retranslateUi(login)
        QtCore.QMetaObject.connectSlotsByName(login)
        login.setTabOrder(self.txt_input_usuario, self.txt_input_contrasea)
        login.setTabOrder(self.txt_input_contrasea, self.bt_cerrar)

    def retranslateUi(self, login):
        _translate = QtCore.QCoreApplication.translate
        login.setWindowTitle(_translate("login", "Sport Center Gym"))
        self.bt_cerrar.setText(_translate("login", "Cerrar"))
        self.bt_ingresar_login.setText(_translate("login", "Iniciar sesión"))
        self.txt_input_contrasea.setPlaceholderText(_translate("login", "   Contraseña"))
        self.txt_input_usuario.setPlaceholderText(_translate("login", "   Usuario"))
        self.label.setText(_translate("login", "Inicio de sesión"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    login = QtWidgets.QMainWindow()
    ui = Ui_login()
    ui.setupUi(login)
    login.show()
    sys.exit(app.exec_())
