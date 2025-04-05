from PyQt5.QtCore import QDate, QTimer
import re
from PyQt5 import QtWidgets as qtw
from Recursos.Estilos import *


def validar_campos_obligatorios(campos, parent):
    error = False
    for campo, nombre_campo in campos:
        if not campo.text():  # Verifica si el campo está vacío
            campo.setStyleSheet("""
                QLineEdit {
                    height: 43px;
                    border: 2px solid red;
                    color: rgb(0, 0, 0);
                    font: 15pt "Segoe UI";
                    background-color: rgb(255, 255, 255);
                    border-radius: 5px;
                    padding-left: 10px;
                }
            """)
            # Crea un mensaje de advertencia
            mensaje = QMessageBox(parent)  # Asegúrate de que 'parent' sea un QWidget (como 'self.ui')
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"El campo '{nombre_campo}' es obligatorio")
            mensaje.setIcon(QMessageBox.Warning)
            aplicar_estilo_mensaje(mensaje)  # Aplica el estilo al mensaje
            mensaje.exec_()
            error = True

            # Restablece el estilo del campo después de 500 ms
            QTimer.singleShot(500, lambda campo=campo: campo.setStyleSheet("""
                QLineEdit {
                    color: rgb(0, 0, 0);
                    font: 15pt "Segoe UI";
                    background-color: rgb(255, 255, 255);
                    border-radius: 5px;
                    padding: 5px;
                    padding-left: 10px;
                }
            """))
    return not error  # Retorna True si no hay errores, False si hay campos vacíos

def validar_fecha_nacimiento(fecha_texto, parent):
    # Convertir el texto a un objeto QDate
    fecha_nacimiento = QDate.fromString(fecha_texto, "yyyy-MM-dd")

    # Verificar si la conversión fue exitosa
    if not fecha_nacimiento.isValid():
        mensaje = qtw.QMessageBox(parent)
        mensaje.setWindowTitle("Error")
        mensaje.setText("El formato de la fecha de nacimiento es incorrecto. Use el formato 'yyyy-MM-dd'")
        mensaje.setIcon(qtw.QMessageBox.Warning)
        mensaje.exec_()
        return False

    # Calcular la edad
    hoy = QDate.currentDate()
    edad = hoy.year() - fecha_nacimiento.year() - ((hoy.month(), hoy.day()) < (fecha_nacimiento.month(), fecha_nacimiento.day()))

    # Verificar la edad mínima de 16 años
    if edad < 16:
        mensaje = qtw.QMessageBox(parent)
        mensaje.setWindowTitle("Error")
        mensaje.setText("El cliente debe tener al menos 16 años de edad")
        mensaje.setIcon(qtw.QMessageBox.Warning)
        aplicar_estilo_mensaje(mensaje)
        mensaje.exec_()
        return False

    return True

def validar_correo(correo, parent):
    patron_correo = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(patron_correo, correo):
        mensaje = qtw.QMessageBox(parent)
        mensaje.setWindowTitle("Error")
        mensaje.setText("El correo electrónico no es válido. Ingrese un correo con el formato correcto.")
        mensaje.setIcon(qtw.QMessageBox.Warning)
        aplicar_estilo_mensaje(mensaje)
        mensaje.exec_()
        return False

    return True

def formatear_precio(campo_precio):
    texto = campo_precio.text().replace(",", "")
    if texto:
        try:
            # Convertir el texto en un número entero
            numero = int(texto)
            # Formatear el número con puntos para los miles
            texto_formateado = "{:,}".format(numero)
            campo_precio.blockSignals(True)
            campo_precio.setText(texto_formateado)
            campo_precio.blockSignals(False)
        except ValueError:
            pass

def formatear_precio_base_datos(campo_precio, precio):
    # Formatear el precio obtenido de la base de datos con separadores de miles y dos decimales
    precio_formateado = "{:,.2f}".format(precio)
    campo_precio.setText(precio_formateado)

