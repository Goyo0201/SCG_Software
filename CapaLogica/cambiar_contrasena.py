# dialogo_cambiar_contrasena.py

from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtWidgets as qtw
import bcrypt
from CapaDatos.ConexionPyodbc import conexion  # Asegúrate de tener esta conexión bien configurada
from Recursos.Estilos import aplicar_estilo_mensaje, aplicar_estilo_dialogo 

class CambiarContrasena(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(CambiarContrasena, self).__init__(parent)
        self.setWindowTitle("Cambiar Contraseña")

        # Layout y widgets
        layout = QtWidgets.QVBoxLayout(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Popup)
        self.move(1500, 100)

        # Establecer un tamaño mínimo para el diálogo
        self.setMinimumSize(200, 120)  # Cambia este tamaño según sea necesario

        self.etiqueta_actual = QtWidgets.QLabel("Contraseña Actual:")
        self.contrasena_actual = QtWidgets.QLineEdit()
        self.contrasena_actual.setEchoMode(QtWidgets.QLineEdit.Password)

        self.etiqueta_nueva = QtWidgets.QLabel("Nueva Contraseña:")
        self.nueva_contrasena = QtWidgets.QLineEdit()
        self.nueva_contrasena.setEchoMode(QtWidgets.QLineEdit.Password)

        # Botones
        self.boton_aceptar = QtWidgets.QPushButton("Aceptar")
        self.boton_cancelar = QtWidgets.QPushButton("Cancelar")

        # Conectar botones a acciones
        self.boton_aceptar.clicked.connect(self.cambiar_contrasena)
        self.boton_cancelar.clicked.connect(self.reject)

        # Añadir widgets al layout
        layout.addWidget(self.etiqueta_actual)
        layout.addWidget(self.contrasena_actual)
        layout.addWidget(self.etiqueta_nueva)
        layout.addWidget(self.nueva_contrasena)
        layout.addWidget(self.boton_aceptar)
        layout.addWidget(self.boton_cancelar)

        # Aplicar estilo
        self.setStyleSheet(aplicar_estilo_dialogo())

        self.setLayout(layout)
        
    

    def cambiar_contrasena(self):
        contrasena_actual = self.contrasena_actual.text()
        nueva_contrasena = self.nueva_contrasena.text()

        if self.validar_contrasena(contrasena_actual):
            # Si la contraseña actual es válida, proceder a cambiarla
            hashed_new_password = self.hash_password(nueva_contrasena)
            self.actualizar_contrasena_en_db(hashed_new_password)
            mensaje = qtw.QMessageBox(self)
            mensaje.setText("La contraseña ha sido cambiada con éxito.")
            mensaje.setIcon(qtw.QMessageBox.Information)
            aplicar_estilo_mensaje(mensaje) 
            mensaje.exec_()
            
            self.accept()
        else:
            mensaje = qtw.QMessageBox(self)
            mensaje.setText("La contraseña actual es incorrecta.")
            mensaje.setIcon(qtw.QMessageBox.Warning)
            aplicar_estilo_mensaje(mensaje) 
            mensaje.exec_()

    def validar_contrasena(self, contrasena):
        # Conectar a la base de datos y obtener la contraseña hasheada del administrador
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT contrasena FROM administrador WHERE usuario = 1")
                result = cursor.fetchone()

            if result:
                stored_hashed_password = result[0]
                return bcrypt.checkpw(contrasena.encode('utf-8'), stored_hashed_password.encode('utf-8'))
            return False
        except Exception as ex:
            print(ex)
            return False

    def hash_password(self, contrasena):
        # Generar un hash y salt para la nueva contraseña
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(contrasena.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def actualizar_contrasena_en_db(self, hashed_password):
        # Actualizar la contraseña en la base de datos
        try:
            with conexion.cursor() as cursor:
                cursor.execute("UPDATE administrador SET contrasena = %s WHERE usuario = 1", (hashed_password,))
                conexion.commit()
        except Exception as ex:
            print(ex)

    # Implementación de la función de validación de campos obligatorios
    def validar_campos_obligatorios(campos, dialogo):
        for campo in campos:
            if not campo.text():  # Verifica si el campo está vacío
                return False
        return True