# CapaLogica/Login.py
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut, QMessageBox
from CapaDatos.ConexionPyodbc import conexion  # Importar la conexión de la base de datos
import bcrypt  # Usamos bcrypt para verificar contraseñas encriptadas
from CapaPresentacion import Login_interfaz  # Asumiendo que la interfaz generada desde QtDesigner se llama Ui_login
from Recursos.Estilos import aplicar_estilo_mensaje  # Asumiendo que existe una función para aplicar estilo
from CapaLogica.logica_menu_principal import MenuPrincipal


class Login(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Login_interfaz.Ui_login()
        self.ui.setupUi(self)

        # Instancia de la conexión
        self.conexion = conexion

        # Configuraciones de la ventana de inicio de sesión
        self.ui.bt_cerrar.clicked.connect(self.close)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        
        # Conectar el botón de iniciar sesión
        shortcut = QShortcut(QKeySequence("Return"), self)
        shortcut.activated.connect(self.iniciar_sesion)
        self.ui.bt_ingresar_login.clicked.connect(self.iniciar_sesion)

        # Botón para mostrar/ocultar contraseña
        self.ui.bt_ver.clicked.connect(self.toggle_password_visibility)
        self.ui.bt_ver.setStyleSheet("""
            QPushButton {
                image: url(:/icons/ojo1.png);
                border: none;
                background: transparent;
            }""")

    def toggle_password_visibility(self):
        """Alternar visibilidad de la contraseña."""
        if self.ui.txt_input_contrasea.echoMode() == QtWidgets.QLineEdit.Password:
            self.ui.txt_input_contrasea.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.ui.bt_ver.setStyleSheet("QPushButton { image: url(:/icons/ojo3.png); border: none; background: transparent; }")
        else:
            self.ui.txt_input_contrasea.setEchoMode(QtWidgets.QLineEdit.Password)
            self.ui.bt_ver.setStyleSheet("QPushButton { image: url(:/icons/ojo1.png); border: none; background: transparent; }")

    def iniciar_sesion(self):
        """
        Esta función pide al usuario los datos de ingreso y valida la autenticación.
        """
        # Strip remueve los espacios al principio o al final
        usuario = self.ui.txt_input_usuario.text().strip()
        contraseña = self.ui.txt_input_contrasea.text().strip()

        # Validación de campos vacíos
        if not usuario or not contraseña:
            mensaje = qtw.QMessageBox(self)
            mensaje.setWindowTitle("Error")
            mensaje.setText("Todos los campos son obligatorios")
            mensaje.setIcon(qtw.QMessageBox.Warning)
            aplicar_estilo_mensaje(mensaje)
            mensaje.exec_()
            return False

        try:
            with conexion.cursor() as cursor:
                # Consultar la contraseña en la base de datos para el usuario especificado
                cursor.execute("SELECT contrasena FROM administrador WHERE usuario = %s", (usuario,))
                result = cursor.fetchone()
                
                if result:
                    # Contraseña almacenada en la base de datos
                    contraseña_correcta = result[0]
                    
                    # Comparar la contraseña ingresada con la almacenada (usando bcrypt si está encriptada)
                    if bcrypt.checkpw(contraseña.encode('utf-8'), contraseña_correcta.encode('utf-8')):
                        # Si la autenticación es correcta, cerrar la ventana de login y abrir la principal
                        self.close()
                        self.ventana = MenuPrincipal()
                        self.ventana.show()
                        return True
                    else:
                        # Contraseña incorrecta
                        mensaje = qtw.QMessageBox(self)
                        mensaje.setWindowTitle("Error")
                        mensaje.setText("El usuario o la contraseña son incorrectos")
                        mensaje.setIcon(qtw.QMessageBox.Warning)
                        aplicar_estilo_mensaje(mensaje)
                        mensaje.exec_()
                        return False
                else:
                    # Usuario no encontrado
                    mensaje = qtw.QMessageBox(self)
                    mensaje.setWindowTitle("Error")
                    mensaje.setText("El usuario o la contraseña son incorrectos")
                    mensaje.setIcon(qtw.QMessageBox.Warning)
                    aplicar_estilo_mensaje(mensaje)
                    mensaje.exec_()
                    return False

        except Exception as ex:
            print("Error de conexión:", ex)
            mensaje = qtw.QMessageBox(self)
            mensaje.setWindowTitle("Error")
            mensaje.setText("Ocurrió un error al intentar iniciar sesión.  Por favor, siga los siguientes pasos para solucionar el problema:\n\n"
            "1. Abra WampServer desde el acceso directo de su escritorio o barra de tareas.\n\n"
                "2. Verifique el color del ícono de WampServer en la barra de tareas:\n"
                "   - **Rojo**: Indica que ninguno de los servicios está funcionando. Haga clic izquierdo en el ícono y seleccione 'Iniciar todos los servicios'.\n"
                "   - **Naranja**: Indica que algunos servicios no están funcionando. Haga clic izquierdo en el ícono y seleccione 'Iniciar todos los servicios' para intentar solucionarlo.\n"
                "   - **Verde**: Indica que todos los servicios están funcionando correctamente.\n\n"
                "3. Una vez que el ícono esté en verde, intente acceder nuevamente a la aplicación.\n\n"
                "Si el problema persiste, asegúrese de que la configuración del usuario y la contraseña de MySQL sea correcta.")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)
            mensaje.exec_()
            return False
