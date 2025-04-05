from PyQt5 import QtWidgets, QtCore
from datetime import datetime, timedelta
from plyer import notification
from CapaDatos.ConexionPyodbc import conexion
from Recursos.Estilos import aplicar_estilo_notificacion
import time

class Notificaciones:
    def __init__(self, ui, parent ):
        self.ui = ui
        self.parent = parent  # Guarda una referencia al widget principal
        

    #*Plyer (notificaciones de escritorio)
    def enviar_notificacion_plyer(self, titulo, mensaje):
        """
        Enviar una notificación automática al sistema usando Plyer.
        """
        try:
            print(f"Enviando notificación: {titulo} - {mensaje}")  # Mensaje de depuración
            notification.notify(
                title=titulo,
                message=mensaje,
                app_name="Gestor de Membresías",
                timeout=8  # Duración de la notificación (segundos)
            )

        except Exception as e:
            print(f"Error al enviar la notificación: {e}")


    #*Notificaciones
    def actualizar_icono_notificacion(self, estado):
        # Estado puede ser "sin_noti", "con_noti" o "noti_vista"
        self.ui.bt_sin_noti.setVisible(estado == "sin_noti")
        self.ui.bt_con_noti.setVisible(estado == "con_noti")
        self.ui.bt_noti_vista.setVisible(estado == "noti_vista")


    def verificar_notificaciones(self):
        """
        Verifica si hay notificaciones pendientes de membresías expiradas o próximas a expirar
        al iniciar el sistema y ajusta los íconos de notificación en consecuencia.
        Además, envía notificaciones automáticas con Plyer.
        """
        # Obtener listas de clientes expirados y próximos a expirar
        clientes_expirados, clientes_proximos = self.obtener_notificaciones_membresias()

     
        

        # Notificación automática con Plyer para miembros expirados
        if clientes_expirados:
            nombres_expirados = ", ".join([f"{cliente[0]} {cliente[1]}" for cliente in clientes_expirados])
            mensaje_expirados = f"Las membresías de {nombres_expirados} han expirado."
            self.enviar_notificacion_plyer(
                titulo="Membresías Expiradas",
                mensaje=mensaje_expirados
            )
            time.sleep(0.2)  # Añadir un retraso 

        # Notificación automática con Plyer para miembros próximos a expirar
        if clientes_proximos:
            nombres_proximos = ", ".join([f"{cliente[0]} {cliente[1]}" for cliente in clientes_proximos])
            mensaje_proximos = f"Las membresías de {nombres_proximos} están por expirar."
            self.enviar_notificacion_plyer(
                titulo="Membresías Próximas a Expirar",
                mensaje=mensaje_proximos
            )


        # Actualizar iconos en la interfaz manual
        if clientes_expirados or clientes_proximos:
            self.ui.bt_con_noti.show()
            self.ui.bt_sin_noti.hide()
            self.ui.bt_noti_vista.hide()
        else:
            self.ui.bt_sin_noti.show()
            self.ui.bt_con_noti.hide()
            self.ui.bt_noti_vista.hide()


    

    def obtener_notificaciones_membresias(self):
        hoy = datetime.today()
        proximos_a_expirar = hoy + timedelta(days=3)
        
        try:
            with conexion.cursor() as cursor:
                # Membresías expiradas
                sql_expiradas = """
                    SELECT nombres, apellidos, fecha_fin
                    FROM clientes
                    JOIN pagos ON clientes.id = pagos.id_cliente
                    WHERE fecha_fin < %s
                """
                cursor.execute(sql_expiradas, (hoy,))
                clientes_expirados = cursor.fetchall()
                
                # Membresías próximas a expirar
                sql_proximas = """
                    SELECT nombres, apellidos, fecha_fin
                    FROM clientes
                    JOIN pagos ON clientes.id = pagos.id_cliente
                    WHERE fecha_fin >= %s AND fecha_fin <= %s
                """
                cursor.execute(sql_proximas, (hoy, proximos_a_expirar))
                clientes_proximos = cursor.fetchall()
                
                return clientes_expirados, clientes_proximos

        except Exception as e:
            print("Error al obtener notificaciones:", e)




    #ventana superior
    def mostrar_ventana_notificaciones(self):
        # Obtener los clientes con membresías expiradas y próximas a expirar
        clientes_expirados, clientes_proximos = self.obtener_notificaciones_membresias()

        # Crear la ventana de notificación sin bordes
        ventana = QtWidgets.QDialog(self.parent)  

        ventana.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Popup)
        ventana.setMinimumSize(300, 400)  # Tamaño mínimo para la ventana de notificación
        ventana.move(1500, 100)

        # Layout principal de la ventana
        layout_principal = QtWidgets.QVBoxLayout(ventana)
        layout_principal.setContentsMargins(0, 0, 0, 0)  # Sin márgenes para ajustarse a la ventana

        # Crear barra superior personalizada
        barra_superior = QtWidgets.QWidget()
        barra_superior.setObjectName("barraSuperior")
        layout_barra = QtWidgets.QHBoxLayout(barra_superior)
        barra_superior.setFixedHeight(40)
        layout_barra.setContentsMargins(10, 5, 10, 5)

        # Título en la barra superior
        titulo_label = QtWidgets.QLabel("Notificaciones de Membresías")
        titulo_label.setObjectName("tituloNotificacion")
        layout_barra.addWidget(titulo_label)

        # Botón de cierre
        boton_cerrar = QtWidgets.QPushButton("X")
        boton_cerrar.setObjectName("botonCerrar")
        boton_cerrar.setFixedSize(20, 20)
        boton_cerrar.clicked.connect(ventana.close)
        layout_barra.addWidget(boton_cerrar, alignment=QtCore.Qt.AlignRight)

        layout_principal.addWidget(barra_superior)

        # Crear el contenedor de notificaciones dentro de una QScrollArea
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none;")  # Quitar borde de la QScrollArea

        contenido_scroll = QtWidgets.QWidget()
        layout_contenido = QtWidgets.QVBoxLayout(contenido_scroll)
        layout_contenido.setContentsMargins(10, 10, 10, 10)

        # Agregar notificaciones de expirados
        if clientes_expirados:
            titulo_expirados = QtWidgets.QLabel("Membresías Expiradas")
            titulo_expirados.setObjectName("tituloExpirados")
            layout_contenido.addWidget(titulo_expirados)
            for cliente in clientes_expirados:
                label_cliente = QtWidgets.QLabel(f" 🟠  {cliente[0]} {cliente[1]}\n        Expirado el {cliente[2].strftime('%Y-%m-%d')}")
                label_cliente.setObjectName("clienteExpirado")
                layout_contenido.addWidget(label_cliente)

        # Agregar una línea divisoria
        linea_divisoria = QtWidgets.QFrame()
        linea_divisoria.setFrameShape(QtWidgets.QFrame.HLine)
        linea_divisoria.setFrameShadow(QtWidgets.QFrame.Sunken)
        linea_divisoria.setStyleSheet("color: orange;")
        layout_contenido.addWidget(linea_divisoria)

        # Agregar notificaciones de próximos a expirar
        if clientes_proximos:
            titulo_proximos = QtWidgets.QLabel("Membresías Próximas a Expirar")
            titulo_proximos.setObjectName("tituloProximos")
            layout_contenido.addWidget(titulo_proximos)
            for cliente in clientes_proximos:
                label_cliente = QtWidgets.QLabel(f" 🟠  {cliente[0]} {cliente[1]}\n        Expira el {cliente[2].strftime('%Y-%m-%d')}")
                label_cliente.setObjectName("clienteProximo")
                layout_contenido.addWidget(label_cliente)

        # Agregar mensaje si no hay notificaciones
        if not clientes_expirados and not clientes_proximos:
            mensaje_vacio = QtWidgets.QLabel("No hay notificaciones.")
            mensaje_vacio.setObjectName("mensajeVacio")
            layout_contenido.addWidget(mensaje_vacio)

        # Añadir el contenido al área de scroll
        scroll_area.setWidget(contenido_scroll)
        layout_principal.addWidget(scroll_area)

        # Aplicar estilo CSS
        ventana.setStyleSheet(aplicar_estilo_notificacion())

        ventana.exec_()
        self.actualizar_icono_notificacion("noti_vista")  # Cambia el estado de la campana