from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox


def aplicar_estilo_mensaje(mensaje, agregar_boton_aceptar=True):
    # Estilo CSS para QMessageBox
    estilo_css = '''
    QMessageBox {
        background-color: #F0F0F0;
        border: 1px solid #ffffff;
    }
    QLabel, QMessageBox QLabel {
        color: #000000;
        font-size: 19px;
    }
    QPushButton, QMessageBox QPushButton {
        background-color: #FF6704;
        color: #F0F0F0;
        border: 1px solid #ffffff;
        padding: 5px 10px;
        border-radius: 7px;
        font-size: 20px;
    }
    QPushButton:hover, QMessageBox QPushButton:hover {
        background-color: #000000;
    }
    '''
    mensaje.setStyleSheet(estilo_css)
    mensaje.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # Aplicar sin bordes (opcional)

    # Agregar botón personalizado "Aceptar" solo si se especifica
    if agregar_boton_aceptar:
        botonAceptar = mensaje.addButton(QMessageBox.Ok)
        botonAceptar.setText("Aceptar")

    return mensaje

def aplicar_estilo_spin_activo ():
    return """
    QSpinBox {
        color: rgb(0, 0, 0); /* Texto negro */
        font: 15pt "Segoe UI"; /* Fuente */
        background-color: rgb(255, 255, 255); /* Fondo blanco */
        border-radius: 5px; /* Bordes redondeados */
        padding: 5px; /* Espacio interno para que el texto no esté pegado al borde */
        padding-left: 10px; /* Espacio a la izquierda para que el texto no quede pegado */
    }

    QSpinBox::up-button {
        subcontrol-origin: border;
        subcontrol-position: top right;
        width: 16px;  /* Ancho del botón superior */
        border-left: 1px solid black;  /* Borde en el lado izquierdo del botón */
        border-bottom: 1px solid black;  /* Borde en la parte inferior del botón */
        border-top: none;  /* Sin borde superior */
        border-right: none;  /* Sin borde derecho */
        border-radius: 0px;  /* Sin bordes redondeados */
    }

    QSpinBox::down-button {
        subcontrol-origin: border;
        subcontrol-position: bottom right;
        width: 16px;  /* Ancho del botón inferior */
        border-left: 1px solid black;  /* Borde en el lado izquierdo del botón */
        border-top: 1px solid black;  /* Borde en la parte superior del botón */
        border-bottom: none;  /* Sin borde inferior */
        border-right: none;  /* Sin borde derecho */
        border-radius: 0px;  /* Sin bordes redondeados */
    }

    QSpinBox::up-arrow, QSpinBox::down-arrow {
        width: 10px;
        height: 10px;
    }

    QSpinBox::up-arrow {
        image: url(:/iconos_principal/iconos/punta-de-flecha (1).png);
    }

    QSpinBox::down-arrow {
        image: url(:/iconos_principal/iconos/punta-de-flecha.png);
    }
    """


def aplicar_estilo_spin_inactivo():
    return """
    QSpinBox {
        color: rgb(0, 0, 0); /* Texto negro */
        font: 15pt "Segoe UI"; /* Fuente */
        background-color: #F5F5F5;
        border-radius: 5px; /* Bordes redondeados */
        padding: 5px; /* Espacio interno para que el texto no esté pegado al borde */
        padding-left: 10px; /* Espacio a la izquierda para que el texto no quede pegado */
    }

    QSpinBox::up-button {
        subcontrol-origin: border;
        subcontrol-position: top right;
        width: 16px;  /* Ancho del botón superior */
        border-left: 1px solid black;  /* Borde en el lado izquierdo del botón */
        border-bottom: 1px solid black;  /* Borde en la parte inferior del botón */
        border-top: none;  /* Sin borde superior */
        border-right: none;  /* Sin borde derecho */
        border-radius: 0px;  /* Sin bordes redondeados */
    }

    QSpinBox::down-button {
        subcontrol-origin: border;
        subcontrol-position: bottom right;
        width: 16px;  /* Ancho del botón inferior */
        border-left: 1px solid black;  /* Borde en el lado izquierdo del botón */
        border-top: 1px solid black;  /* Borde en la parte superior del botón */
        border-bottom: none;  /* Sin borde inferior */
        border-right: none;  /* Sin borde derecho */
        border-radius: 0px;  /* Sin bordes redondeados */
    }

    QSpinBox::up-arrow, QSpinBox::down-arrow {
        width: 10px;
        height: 10px;
    }

    QSpinBox::up-arrow {
        image: url(:/iconos_principal/iconos/punta-de-flecha (1).png);
    }

    QSpinBox::down-arrow {
        image: url(:/iconos_principal/iconos/punta-de-flecha.png);
    }
    """

def aplicar_estilo_spin_double_activo():
    return """
    QDoubleSpinBox {
    color: rgb(0, 0, 0); /* Texto negro */
    font: 15pt "Segoe UI"; /* Fuente */
	background-color: rgb(255, 255, 255);
    border-radius: 5px; /* Bordes redondeados */
    padding: 5px; /* Espacio interno para que el texto no esté pegado al borde */
	padding-left: 10px; /* Espacio a la izquierda para que el texto no quede pegado */
    }

    QDoubleSpinBox::up-button {
        subcontrol-origin: border;
        subcontrol-position: top right;
        width: 16px;  /* Ancho del botón superior */
        border-left: 1px solid black;  /* Borde en el lado izquierdo del botón */
        border-bottom: 1px solid black;  /* Borde en la parte inferior del botón */
        border-top: none;  /* Sin borde superior */
        border-right: none;  /* Sin borde derecho */
        border-radius: 0px;  /* Sin bordes redondeados */
    }

    QDoubleSpinBox::down-button {
        subcontrol-origin: border;
        subcontrol-position: bottom right;
        width: 16px;  /* Ancho del botón inferior */
        border-left: 1px solid black;  /* Borde en el lado izquierdo del botón */
        border-top: 1px solid black;  /* Borde en la parte superior del botón */
        border-bottom: none;  /* Sin borde inferior */
        border-right: none;  /* Sin borde derecho */
        border-radius: 0px;  /* Sin bordes redondeados */
    }

    QDoubleSpinBox::up-arrow, QDoubleSpinBox::down-arrow {
        width: 10px;
        height: 10px;
    }

    QDoubleSpinBox::up-arrow {
        
        image: url(:/iconos_principal/iconos/punta-de-flecha (1).png);
    }

    QDoubleSpinBox::down-arrow {
        
        image: url(:/iconos_principal/iconos/punta-de-flecha.png);
    }
    """

def aplicar_estilo_spin_double_inactivo():
    return """
    QDoubleSpinBox {
        color: rgb(0, 0, 0); /* Texto negro */
        font: 15pt "Segoe UI"; /* Fuente */
        background-color: #F5F5F5;
        border-radius: 5px; /* Bordes redondeados */
        padding: 5px; /* Espacio interno para que el texto no esté pegado al borde */
        padding-left: 10px; /* Espacio a la izquierda para que el texto no quede pegado */
    }

    QDoubleSpinBox::up-button {
        subcontrol-origin: border;
        subcontrol-position: top right;
        width: 16px;  /* Ancho del botón superior */
        border-left: 1px solid black;  /* Borde en el lado izquierdo del botón */
        border-bottom: 1px solid black;  /* Borde en la parte inferior del botón */
        border-top: none;  /* Sin borde superior */
        border-right: none;  /* Sin borde derecho */
        border-radius: 0px;  /* Sin bordes redondeados */
    }

    QDoubleSpinBox::down-button {
        subcontrol-origin: border;
        subcontrol-position: bottom right;
        width: 16px;  /* Ancho del botón inferior */
        border-left: 1px solid black;  /* Borde en el lado izquierdo del botón */
        border-top: 1px solid black;  /* Borde en la parte superior del botón */
        border-bottom: none;  /* Sin borde inferior */
        border-right: none;  /* Sin borde derecho */
        border-radius: 0px;  /* Sin bordes redondeados */
    }

    QDoubleSpinBox::up-arrow, QDoubleSpinBox::down-arrow {
        width: 10px;
        height: 10px;
    }

    QDoubleSpinBox::up-arrow {
        
        image: url(:/iconos_principal/iconos/punta-de-flecha (1).png);
    }

    QDoubleSpinBox::down-arrow {
        
        image: url(:/iconos_principal/iconos/punta-de-flecha.png);
    }
    """

def aplicar_estilo_notificacion():
    return """
    QDialog {
        background-color: #f9f9f9;
        border: 2px solid #ccc;
        border-radius: 10px;
        padding: 0px;
        border-bottom-left-radius: 8px;
        border-bottom-right-radius: 8px;
    }
    QWidget#barraSuperior {
        background-color: black;
        padding: 0 10px;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
    }
    QLabel#tituloNotificacion {
        color: #ffffff;
        font-family: 'Segoe UI';
        font-size: 15px;
        font-weight: bold;
    }
    QPushButton#botonCerrar {
        background-color: transparent;
        color: #ffffff;
        border: none;
        font-weight: bold;
        font-size: 16px;
    }
    QPushButton#botonCerrar:hover {
        color: #FF6704; /* Cambia el color al pasar el cursor */
    }
    QLabel#mensajeVacio {
        font-style: italic;
        color: #999;
        font-size: 14px;
        padding: 8px;
    }
    QLabel {
        font-size: 14px;
        padding: 4px 0;
    }
    QLabel#tituloExpirados, QLabel#tituloProximos {
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 5px;
    }
    QLabel#tituloExpirados {
        color: #FF6704;
    }
    QLabel#tituloProximos {
        color: #FF6704;
        margin-top: 15px;
    }
    QLabel.clienteExpirado {
        color: #d9534f;
        margin-left: 10px;  /* Espacio para indentación */
    }
    QLabel.clienteProximo {
        color: #f0ad4e;
        margin-left: 10px;  /* Espacio para indentación */
    }

    /* Estilos para la barra de desplazamiento */
    QScrollBar:vertical {
        width: 12px;
        background-color: #f0f0f0; /* Fondo gris claro */
        border-radius: 6px;
    }
    QScrollBar::handle:vertical {
        background-color: #888888; /* Color de la barra de desplazamiento */
        min-height: 20px;
        border-radius: 6px;
    }
    QScrollBar::handle:vertical:hover {
        background-color: #555555; /* Color al pasar el ratón por encima */
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }

    QScrollBar:horizontal {
        height: 12px;
        background-color: #f0f0f0;
        border-radius: 6px;
    }
    QScrollBar::handle:horizontal {
        background-color: #888888;
        min-width: 20px;
        border-radius: 6px;
    }
    QScrollBar::handle:horizontal:hover {
        background-color: #555555;
    }
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        width: 0px;
    }
    """

def aplicar_estilo_dialogo():
    return """
    QDialog {
        background-color: #F0F0F0;           /* Fondo gris claro */
        border: 1px solid #ffffff;            /* Borde blanco */
        color: black;                          /* Color del texto */
        font-family: 'Segoe UI';               /* Fuente Segoe UI */
        border-radius: 5px;                  /* Bordes redondeados */
        padding: 20px;                        /* Espaciado interno */
    }
    QLabel {
        font-size: 20px;                       /* Tamaño de fuente de las etiquetas */
        color: #000000;                        /* Color negro */
        font-family: 'Segoe UI';               /* Fuente Segoe UI */
    }
    QComboBox {
        background-color: #F0F0F0;            /* Fondo gris claro para el combo */
        color: #000000;                        /* Color negro del texto */
        border: 1px solid #ffffff;            /* Borde blanco */
        padding: 5px;                         /* Espaciado interno */
        border-radius: 9px;                   /* Bordes redondeados */
        font-family: 'Segoe UI';               /* Fuente Segoe UI */
        font-size: 18px;
     }

    QComboBox::drop-down {
      
        background: #F0F0F0;                 /* Fondo gris claro */
        width: 20px;                         /* Ancho de la flecha */
        border-radius: 5px;                  /* Bordes redondeados para el drop-down */
    }
    
    QComboBox::down-arrow {
        image: url(:/iconos_principal/iconos/punta-de-flecha.png);
        width: 10px;                          /* Ancho de la flecha */
        height: 10px;                         /* Alto de la flecha */
    }

    QComboBox QAbstractItemView {
        background-color: #F0F0F0;            /* Fondo gris claro para el desplegable */
        color: #000000;                        /* Color negro */
        selection-background-color: #FF6704;  /* Color de fondo de selección naranja */
    }
    QPushButton {
        background-color: #FF6704;            /* Fondo naranja */
        color: #F0F0F0;                        /* Color de texto gris claro */
        border: 1px solid #ffffff;            /* Borde blanco */
        padding: 5px 10px;                    /* Espaciado interno */
        border-radius: 7px;                   /* Bordes redondeados */
        font-size: 17px;                       /* Tamaño de fuente de los botones */
        font-family: 'Segoe UI';               /* Fuente Segoe UI */
    }
    QPushButton:hover {
        background-color: #000000;            /* Fondo negro al pasar el mouse */
    }
    """

def aplicar_estilo_progress_dialog(dialogo):
    estilo_css = '''
    QProgressDialog {
        background-color: #F0F0F0;
        border: 1px solid #ffffff;
        border-radius: 8px;
        padding: 10px;
    }
    QLabel, QProgressDialog QLabel {
        color: #000000;
        font-size: 18px;
    }
    QProgressBar {
        background-color: #D3D3D3;
        border: 1px solid #ffffff;
        height: 25px;
        border-radius: 5px;
        text-align: center; /* Asegura que el texto esté centrado */
        color: #FFFFFF; /* Color blanco para el texto del porcentaje */
        font-family: 'Segoe UI';
        font-size: 20px;
      
    }
    QProgressBar::chunk {
        background-color: #FF6704;
        border-radius: 5px;
    }
    QPushButton, QProgressDialog QPushButton {
        background-color: #FF6704;
        color: #F0F0F0;
        border: 1px solid #ffffff;
        padding: 5px 10px;
        border-radius: 7px;
        font-size: 20px;
    }
    QPushButton:hover, QProgressDialog QPushButton:hover {
        background-color: #000000;
    }
    '''
    
    # Quitar la barra de título
    dialogo.setWindowFlag(QtCore.Qt.FramelessWindowHint)
    dialogo.setStyleSheet(estilo_css)
    return dialogo


