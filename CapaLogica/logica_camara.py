import os
import cv2
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMessageBox

from CapaLogica.Utilidades import ampliar_imagen_utl

class LogicaCamara:
    def __init__(self, ui, parent=None):
        self.ui = ui
        self.parent = parent
        self.foto_cliente = None

    def abrir_camara(self):
        try:
            camara = cv2.VideoCapture(0)
            if not camara.isOpened():
                raise Exception("No se pudo acceder a la cámara. Verifica que esté conectada.")

            while True:
                ret, frame = camara.read()
                if not ret:
                    print("Error al capturar la imagen.")
                    break

                cv2.imshow("Captura de Foto (Presiona Espacio para tomar la foto)", frame)

                key = cv2.waitKey(1) & 0xFF
                if key == 32:  # Espacio para capturar la foto
                    ruta_foto = "foto_cliente.jpg"
                    cv2.imwrite(ruta_foto, frame)
                    print(f"Foto capturada y guardada en: {ruta_foto}")

                    # Convertir la imagen a binario
                    with open(ruta_foto, "rb") as file:
                        self.foto_cliente = file.read()  # Leer la foto como binario

                    # Mostrar la foto y conectar el evento dinámicamente
                    self.mostrar_foto_en_label(ruta_foto)

                    # Eliminar el archivo temporal después de procesarlo
                    if os.path.exists(ruta_foto):
                        os.remove(ruta_foto)

                    if hasattr(self.ui, 'logica_usuarios') and self.ui.logica_usuarios is not None:
                        self.ui.label_foto_cliente.mousePressEvent = lambda event: ampliar_imagen_utl(
                            self.ui.logica_usuarios.pixmap_actual
                        )
                    break


                elif key == 27:  # Esc
                    break

            camara.release()
            cv2.destroyAllWindows()

        except Exception as e:
            print("Error en abrir_camara:", str(e))


    def mostrar_foto_en_label(self, ruta_foto):
        try:
            pixmap = QPixmap(ruta_foto)
            self.ui.label_foto_cliente.setPixmap(pixmap)
            self.ui.label_foto_cliente.setScaledContents(True)

            # Actualizar pixmap_actual en LogicaUsuarios
            if hasattr(self.ui, 'logica_usuarios') and self.ui.logica_usuarios is not None:
                self.ui.logica_usuarios.pixmap_actual = pixmap


            # Reconectar el evento de clic en el QLabel
            self.ui.label_foto_cliente.mousePressEvent = lambda event: ampliar_imagen_utl(pixmap)

        except Exception as e:
            print("Error en mostrar_foto_en_label:", str(e))

