from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog
from CapaLogica.ampliar_imagen import ImageDialog
from Recursos.Estilos import *
from PyQt5.QtCore import Qt

 
        
def mousePressEvent(self, event):
    self.click_posicion = event.globalPos()

def mover_ventana(self, event):
    if not self.isMaximized():         
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.click_posicion)
            self.click_posicion = event.globalPos()
            event.accept()
		
    if event.globalPos().y() <= 5 or event.globalPos().x() <= 5:
        self.showMaximized()

    else:
        self.showNormal()
      

def calcular_imc(self):
    try:
        peso = float(self.ui.txt_peso.text())  # Convertir a float para asegurarse de que acepta decimales
        altura_cm = float(self.ui.txt_altura.text())
        altura_m = altura_cm / 100  # Convertir altura a metros

        if altura_m > 0:
            imc = peso / (altura_m ** 2)
            imc_formateado = "{:.2f}".format(imc)  # Formatear con dos decimales
            self.ui.txt_indice_masa.setText(imc_formateado)  # Asegurarse de que se establece como texto
            return imc
        else:
            self.ui.txt_indice_masa.clear()
            return None
    except ValueError:
        self.ui.txt_indice_masa.clear()



def mover_cursor_inicio(campo):
    campo.setCursorPosition(0)

def limpiar_entrada(campo):
    texto = campo.text()
    texto_limpio = ''.join(filter(str.isdigit, texto))
    campo.setText(texto_limpio)

def subir_foto(parent, label, tipo_foto):
    """
    Abre un cuadro de diálogo para seleccionar una imagen desde el PC, la muestra en el QLabel,
    la convierte a binario y actualiza referencias para la base de datos y ampliación.
    """
    try:
        # Abrir el cuadro de diálogo para seleccionar la imagen
        file_name, _ = QFileDialog.getOpenFileName(None, "Seleccionar Imagen", "", "Imágenes (*.png *.jpg *.jpeg)")
        
        if file_name:
            # Cargar la imagen en el QLabel proporcionado
            pixmap = QPixmap(file_name)
            label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            label.setScaledContents(True)

            # Convertir la imagen a binario para almacenarla en la base de datos
            with open(file_name, 'rb') as file:
                if tipo_foto == 'cliente':
                    parent.foto_cliente = file.read()  # Almacenar la imagen en binario en un atributo de la clase
                    print(f"Foto del cliente cargada y almacenada en binario ({len(parent.foto_cliente)} bytes).")
                elif tipo_foto == 'maquina':
                    parent.foto_maquina = file.read()  # Almacenar la imagen en binario en un atributo de la clase
                    print(f"Foto de la máquina cargada y almacenada en binario ({len(parent.foto_maquina)} bytes).")

            # Guardar el pixmap de la imagen en un atributo para ampliarla más tarde
            parent.pixmap_actual = pixmap
            print("pixmap_actual actualizado correctamente.")

            # Reconectar el evento de clic en el QLabel para ampliación
            label.mousePressEvent = lambda event: ampliar_imagen_utl(parent.pixmap_actual)
            print("Evento de clic reconectado al QLabel para ampliación desde archivo.")

        else:
            # Si no se seleccionó una imagen, asignar None
            print("No se seleccionó ninguna imagen. Restableciendo referencias.")
            if tipo_foto == 'cliente':
                parent.foto_cliente = None
            elif tipo_foto == 'maquina':
                parent.foto_maquina = None

            parent.pixmap_actual = None
            label.clear()  # Limpiar el QLabel de la imagen

    except Exception as e:
        print(f"Error en subir_foto: {e}")


def ampliar_imagen_utl(pixmap_actual):
    if pixmap_actual is not None:
        dialog = ImageDialog(pixmap_actual)
        dialog.exec_()
    else:
        print("No hay imagen para ampliar.")
