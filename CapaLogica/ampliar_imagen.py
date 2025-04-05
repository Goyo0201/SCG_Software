# Clase para mostrar la imagen ampliada

from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal


class ImageDialog(QDialog):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Vista ampliada")
        
        # Quitar bordes de la ventana
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        # Cambiar el color de fondo de la ventana a negro
        self.setStyleSheet("background-color: black; border: 2px solid black;")

        # Crear QLabel para mostrar la imagen
        self.label_imagen_ampliada = QLabel(self)
        self.label_imagen_ampliada.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # Crear botón de cierre "X" en la esquina superior derecha
        self.boton_cerrar = QPushButton("X", self)
        self.boton_cerrar.setStyleSheet("""
            QPushButton {
                image: url(:/iconos_principal/iconos/borrar.png);
                border: 1px solid #000000;
             }QPushButton:hover {
            image: url(:/iconos_principal/iconos/cerrar.png);
        }

        """)
        self.boton_cerrar.setFixedSize(30, 30)
        
        # Agregar la "X" en la parte superior derecha, dentro de un layout
        close_layout = QHBoxLayout()
        close_layout.addWidget(self.boton_cerrar, alignment=Qt.AlignRight)  # Alinear a la derecha

        # Conectar el botón para cerrar la ventana
        self.boton_cerrar.clicked.connect(self.close)

        # Layout principal para la imagen y el botón de cierre
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(close_layout)  # Añadir la "X" al layout principal
        main_layout.addWidget(self.label_imagen_ampliada)  # Añadir la imagen

        self.setLayout(main_layout)

        # Ajustar el tamaño de la ventana para que se ajuste a la imagen
        self.label_imagen_ampliada.adjustSize()
        self.adjustSize()
    
    
#Clase para ver imagen en las tablas
class ClickableLabel(QLabel):
    clicked = pyqtSignal()  # Definir una señal que será emitida cuando se haga clic

    def __init__(self, parent=None):
        super(ClickableLabel, self).__init__(parent)

    def mousePressEvent(self, event):
        self.clicked.emit()  # Emitir la señal cuando se presione el mouse
        super(ClickableLabel, self).mousePressEvent(event)