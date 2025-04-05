
from PyQt5 import QtCore
from CapaPresentacion.Menú_principal import *
from PyQt5.QtWidgets import *
from Recursos.Estilos import aplicar_estilo_dialogo


class DialogoEstado(QtWidgets.QDialog):
    def __init__(self, nombre_maquina, opciones_estado, parent=None):
        super(DialogoEstado, self).__init__(parent)
        self.setWindowTitle("Cambiar estado de la máquina")
        
        # Quitar la barra de título
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        # Establecer un tamaño mínimo para el diálogo
        self.setMinimumSize(450, 170)  # Cambia este tamaño según sea necesario

        # Layout y widgets
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)  # Ajustar márgenes

        etiqueta = QtWidgets.QLabel(f"Seleccione el nuevo estado para la máquina '{nombre_maquina}':")
        layout.addWidget(etiqueta)
        
        self.combo_estado = QtWidgets.QComboBox()
        self.combo_estado.addItems(opciones_estado)
        layout.addWidget(self.combo_estado)

        # Layout horizontal para los botones
        button_layout = QtWidgets.QHBoxLayout()

        # Botones personalizados
        boton_aceptar = QtWidgets.QPushButton("Aceptar")
        boton_cancelar = QtWidgets.QPushButton("Cancelar")

        # Establecer tamaño de los botones
        boton_aceptar.setFixedSize(100, 40)  # Aumentar tamaño
        boton_cancelar.setFixedSize(100, 40)  # Aumentar tamaño
        
        # Conectar botones a acciones
        boton_aceptar.clicked.connect(self.accept)
        boton_cancelar.clicked.connect(self.reject)

        # Añadir botones al layout horizontal
        button_layout.addStretch()  # Para centrar los botones
        button_layout.addWidget(boton_aceptar)
        button_layout.addWidget(boton_cancelar)
        button_layout.addStretch()  # Para centrar los botones

        # Añadir layout de botones al layout principal
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Aplicar estilo
        self.setStyleSheet(aplicar_estilo_dialogo())

    def obtener_estado_seleccionado(self):
        return self.combo_estado.currentText()
