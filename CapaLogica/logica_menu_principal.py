
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5 import QtCore
from CapaLogica.logica_gastos import LogicaGastos
from CapaLogica.logica_horarios import LogicaHorarios
from CapaLogica.logica_maquinas import LogicaMaquinas
from CapaLogica.logica_membresias import LogicaMembresias
from CapaLogica.logica_pagos import LogicaPagos
from CapaLogica.notificaciones import Notificaciones
from CapaPresentacion.Menú_principal import Ui_menu_principal
from CapaLogica.Utilidades import *
from CapaLogica.Validaciones import *
from CapaLogica.cambiar_contrasena import CambiarContrasena
from CapaPresentacion.Menú_principal import *
from PyQt5 import QtWidgets as qtw
from PyQt5.QtWidgets import *
from Recursos.Estilos import aplicar_estilo_mensaje
from CapaLogica.logica_usuarios import LogicaUsuarios  # Importa LogicaUsuarios


#menu principal
# Clase `MenuPrincipal` que envuelve `Ui_menu_principal` en una ventana QMainWindow
class MenuPrincipal(QMainWindow):
    def __init__(self):
        super(MenuPrincipal, self).__init__()
        self.ui = Ui_menu_principal()  # Instancia la interfaz generada
        self.ui.setupUi(self)  # Configura la UI en esta ventana

        # Configuraciones de la ventana
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Inicializar bandera para saber si ya se ha generado el número de factura
        self.numero_factura_generado = False
        # Conectar los botones de restaurar y maximizar a las funciones de utilidades
        self.ui.bt_minimizar.clicked.connect(lambda: self.showMinimized())

        # Inicializar pixmap_actual para evitar errores si no se sube una foto
        self.pixmap_actual = None

        # Conectar los botones en logica_menu_principal.py para poner en naranja uno y los demas no
        self.ui.bt_usuarios.clicked.connect(lambda: self.logica_usuarios.activar_boton_usuarios())
        self.ui.bt_membresias.clicked.connect(lambda: self.logica_membresias.activar_boton_membresias())
        self.ui.bt_horarios.clicked.connect(lambda: self.logica_horarios.activar_boton_horarios())
        self.ui.bt_maquinas.clicked.connect(lambda: self.logica_maquinas.activar_boton_maquinas())
        self.ui.bt_pagos.clicked.connect(lambda: self.logica_pagos.activar_boton_pagos())
        self.ui.bt_gastos.clicked.connect(lambda: self.logica_gastos.activar_boton_gastos())


        #*Notificaciones
        #? Instancia de Notificaciones
        self.notificaciones = Notificaciones(self.ui, self)  # o self si es el QWidget principal
        self.notificaciones.verificar_notificaciones()
        

        # Ejemplo de conexión de botón para mostrar notificaciones
        self.ui.bt_sin_noti.clicked.connect(self.notificaciones.mostrar_ventana_notificaciones)
        self.ui.bt_con_noti.clicked.connect(self.notificaciones.mostrar_ventana_notificaciones)
        self.ui.bt_noti_vista.clicked.connect(self.notificaciones.mostrar_ventana_notificaciones)


        # * USUARIOS (CLIENTES-ENTRENADORES)
        # ? Instancia de LogicaUsuarios
        self.logica_usuarios = LogicaUsuarios(self.ui, self)

        # * MEMBRESÍAS
        # ? Instancia de LogicaMembresias
        self.logica_membresias = LogicaMembresias(self.ui, self)

        #* HORARIOS
        #? Instancia de LogicaHorarios
        self.logica_horarios = LogicaHorarios(self.ui, self)

        #* MÁQUINAS
        #? Instancia de LogicaMaquinas
        self.logica_maquinas = LogicaMaquinas(self.ui, self)

        #* PAGOS
        #? Instancia de LogicaPagos
        self.logica_pagos = LogicaPagos(self.ui, self)

        #* GASTOS
        #? Instancia de LogicaGastos
        self.logica_gastos = LogicaGastos(self.ui, self)


     # Definir actualizando_combo para controlar los eventos de cambio en el ComboBox
        self.actualizando_combo = False

        #Conectar el cambio de pestaña a la función
        self.ui.tabWidget.currentChanged.connect(self.cambiar_pestana1)
        #Conectar el otro
        self.ui.tabWidget_2.currentChanged.connect(self.cambiar_pestana2)

        self.modo_edicion = False
             
        self.ui.bt_cambiar_contra.clicked.connect(self.abrir_dialogo_cambiar_contrasena)

        # Botón para salir con confirmación
        self.ui.bt_cerrar.clicked.connect(self.boton_cerrar_sesion)
        self.mensaje = QMessageBox(self)



    def abrir_dialogo_cambiar_contrasena(self):
        """ Abre el diálogo para cambiar la contraseña. """
        dialogo = CambiarContrasena()
        if dialogo.exec_() == qtw.QDialog.Accepted:
            # Aquí puedes manejar la confirmación si es necesario
            pass
    
    def mostrar_imagen_ampliada(self, pixmap):
        """ Abre el diálogo para mostrar la imagen ampliada. """
        dialogo_imagen = ImageDialog(pixmap)
        dialogo_imagen.exec_()

    


    #!Manejo de llamado a TABS
    def cambiar_pestana1(self):
        # Verifica si el índice corresponde a la pestaña de "Buscar Medidas Antropométricas"
        if self.ui.tabWidget.currentIndex() == 1:  # Suponiendo que la pestaña de "Buscar Medidas" es la segunda
            self.logica_usuarios.pagina_buscar_medidas()
        
        # Verifica si el índice corresponde a la pestaña de "Filtros Clientes"
        elif self.ui.tabWidget.currentIndex() == 2:  # Índice 2 para "Filtros Clientes"
            self.logica_usuarios.pagina_buscar_estado()
        
        elif self.ui.tabWidget.currentIndex() == 3:  # Índice 2 para "Filtros Clientes"
            self.logica_usuarios.pagina_buscar_membresia()
        
        elif self.ui.tabWidget.currentIndex() == 4:  # Índice 2 para "Filtros Clientes"
            self.logica_usuarios.pagina_buscar_filtro()


    def cambiar_pestana2(self):
        #Consultas de pagos
        if self.ui.tabWidget_2.currentIndex() == 1:  # Suponiendo que la pestaña de "Buscar Medidas" es la segunda
            self.logica_pagos.pagina_buscar_historial()
        
        # Verifica si el índice corresponde a la pestaña de "Filtros Clientes"
        elif self.ui.tabWidget_2.currentIndex() == 2:  # Índice 2 para "Filtros Clientes"
            self.logica_pagos.pagina_buscar_expirados()
        
        elif self.ui.tabWidget_2.currentIndex() == 3:  # Índice 2 para "Filtros Clientes"
            self.logica_pagos.pagina_buscar_por_mes()
        
        elif self.ui.tabWidget_2.currentIndex() == 4:  # Índice 2 para "Filtros Clientes"
            self.logica_pagos.pagina_buscar_ultimos_pagos()


    def mousePressEvent(self, event):
        # Utilizar la función de utilidades para manejar el evento de presión del ratón
        mousePressEvent(self, event)

    def mover_ventana(self, event):
        # Utilizar la función de utilidades para mover la ventana
        mover_ventana(self, event)
        
    #*función limpiar campos
    def limpiar_campos(self):
            
        #* Limpiar los campos al entrar a crear (clientes)
            self.ui.txt_cedula_cliente.clear()
            self.ui.txt_nombres_cliente.clear()
            self.ui.txt_apellido_cliente.clear()
            self.ui.txt_direccion_cliente.clear()
            self.ui.txt_telefono_cliente.clear()
            self.ui.txt_correo_cliente.clear()
            self.ui.txt_fecha_nacimiento_cliente.setDate(QDate(2000, 1, 1))
            self.ui.txt_fecha_registro_cliente.setDate(QDate.currentDate())
            self.ui.combo_estado_cliente.setCurrentIndex(0) 
            # Limpiar la imagen del cliente
            self.ui.label_foto_cliente.clear()  # Eliminar cualquier imagen visible
            self.foto_cliente = None  # Restablecer la referencia binaria
            self.pixmap_actual = None  # Restablecer el pixmap actual

            # Desconectar cualquier evento de clic asociado al QLabel
            self.ui.label_foto_cliente.mousePressEvent = None

            self.ui.txt_peso.clear()
            self.ui.txt_altura.clear()
            self.ui.txt_medida_pecho.clear()
            self.ui.txt_medida_brazos.clear()
            self.ui.txt_medida_muslos.clear()
            self.ui.txt_medida_gluteos.clear()
            self.ui.txt_medida_pantorrillas.clear()
            self.ui.txt_medida_hombros.clear()

        #* Limpiar los campos al entrar a crear (entrenadores)
            self.ui.txt_cedula_entrenador.clear()
            self.ui.txt_nombres_entrenador.clear()
            self.ui.txt_apellido_entrenador.clear()
            self.ui.txt_direccion_entrenador.clear()
            self.ui.txt_telefono_entrenador.clear()
            self.ui.txt_correo_entrenador.clear()
            self.ui.txt_fecha_contrato_entrenador.setDate(QDate.currentDate())
            self.ui.combo_especialidad_entrenador.setCurrentIndex(0) 

        #* Limpiar los campos al entrar a crear (membresías)
            self.ui.txt_nombre_membresia.clear()
            self.ui.txt_descripcion_membresia.clear()
            self.ui.txt_precio_membresia.clear()
            self.ui.spin_cantidad.clear()
            self.ui.spin_descuento.setValue(0.00) 
            self.ui.spin_duracion_membresia.setValue(1)
            self.ui.precio_descuento.clear()
            self.ui.combo_tipo_membresia.setCurrentIndex(0)
            self.ui.combo_estado_membresia.setCurrentIndex(0)
        
        #* Limpiar los campos al entrar a crear horario
        
            self.ui.txt_nombre_horario.clear() 
            self.ui.combo_entrenador_horario.setCurrentIndex(0)
            self.ui.combo_hora_inicio.setCurrentIndex(0)
            self.ui.combo_hora_fin.setCurrentIndex(0)
            self.ui.check_lunes.setChecked(False)
            self.ui.check_martes.setChecked(False)
            self.ui.check_miercoles.setChecked(False)
            self.ui.check_jueves.setChecked(False)
            self.ui.check_viernes.setChecked(False)
            self.ui.check_sabado.setChecked(False)
            self.ui.tabla_crear_horario.clearContents()

        #* Limpiar los campos al entrar a crear (máquinas)
            self.ui.txt_nombre_maquina.clear()
            self.ui.txt_descripcion_maquina.clear()
            self.ui.txt_fecha_ingreso_maquina.setDate(QDate.currentDate())
            self.ui.label_foto_maquina.clear()
            self.foto_maquina = None

        #* Limpiar los campos al entrar a crear (pagos)
            self.ui.txt_observaciones.clear()
            self.ui.spin_cantidad.setValue(1)
            self.ui.txt_fecha_inicio_factura.setDate(QDate.currentDate())
            self.ui.combo_clientes_pagos.setCurrentIndex(0)
            self.ui.combo_membresia.setCurrentIndex(0)

        #* Limpiar los campos al entrar a crear (gastos)
            self.ui.txt_fecha_gasto.setDate(QDate.currentDate())
            self.ui.txt_descripcion_gasto.clear()
            self.ui.txt_monto_gasto.clear()
            self.ui.radio_gasto_maquinas.setAutoExclusive(False)
            self.ui.radio_gasto_maquinas.setChecked(False)
            self.ui.radio_gasto_entrenadores.setAutoExclusive(False)
            self.ui.radio_gasto_entrenadores.setChecked(False)
            self.ui.radio_gasto_maquinas.setAutoExclusive(True)
            self.ui.radio_gasto_entrenadores.setAutoExclusive(True)
            self.ui.combo_gasto_maquina.clear()
            self.ui.combo_gasto_entrenador.clear()
            self.ui.combo_tipo_gasto.clear()

        

    #* función Ocultar elementos de editar y mostrar los de crear
    def mostrar_modo_crear(self):
        #* Mostrar u ocultar botones y label de editar (cliente)
        self.ui.bt_guardar_nuevo_cliente.setVisible(True)
        self.ui.bt_editar_cliente.setVisible(False)
        self.ui.label_crear_cliente.setVisible(True)
        self.ui.label_editar_cliente.setVisible(False)

        #* Mostrar u ocultar botones y label de editar (entrenador)
        self.ui.bt_guardar_nuevo_entrenador.setVisible(True)
        self.ui.bt_editar_entrenador.setVisible(False)
        self.ui.label_crear_entrenador.setVisible(True)
        self.ui.label_editar_entrenador.setVisible(False)

        #* Mostrar u ocultar botones y label de editar (membresía)
        self.ui.bt_guardar_membresia.setVisible(True)
        self.ui.bt_editar_membresia.setVisible(False)
        self.ui.label_crear_membresia.setVisible(True)
        self.ui.label_editar_membresia.setVisible(False)

        #* Mostrar u ocultar botones y label de editar (máquina)
        self.ui.bt_guardar_nueva_maquina.setVisible(True)
        self.ui.bt_editar_maquina.setVisible(False)
        self.ui.label_crear_maquina.setVisible(True)
        self.ui.label_editar_maquina.setVisible(False)

        #* Mostrar u ocultar botones y label de editar (pago)
        self.ui.label_43.setVisible(True)
        self.ui.combo_clientes_pagos.setVisible(True)
        self.ui.bt_guardar_pago.setVisible(True)
        self.ui.bt_editar_pago.setVisible(False)
        self.ui.bt_imprimir.setEnabled(False)
        self.ui.bt_enviar_correo.setEnabled(False)
        self.ui.label_crear_pago.setVisible(True)
        self.ui.label_editar_pago.setVisible(False)

        #* Mostrar u ocultar botones y label de editar (gasto)
        self.ui.bt_guardar_gasto.setVisible(True)
        self.ui.bt_editar_gasto.setVisible(False)
        self.ui.label_crear_gasto.setVisible(True)
        self.ui.label_editar_gasto.setVisible(False)
        
        self.limpiar_campos()


    #* función Ocultar elementos de crear y mostrar los de editar
    def mostrar_modo_editar(self):
        #* Mostrar u ocultar botones y label de crear (cliente)
        self.ui.bt_guardar_nuevo_cliente.setVisible(False)
        self.ui.bt_editar_cliente.setVisible(True)
        self.ui.label_crear_cliente.setVisible(False)
        self.ui.label_editar_cliente.setVisible(True)

        #* Mostrar u ocultar botones y label de crear (entrenador)
        self.ui.bt_guardar_nuevo_entrenador.setVisible(False)
        self.ui.bt_editar_entrenador.setVisible(True)
        self.ui.label_crear_entrenador.setVisible(False)
        self.ui.label_editar_entrenador.setVisible(True)

        #* Mostrar u ocultar botones y label de crear (membresía)
        self.ui.bt_guardar_membresia.setVisible(False)
        self.ui.bt_editar_membresia.setVisible(True)
        self.ui.label_crear_membresia.setVisible(False)
        self.ui.label_editar_membresia.setVisible(True)

        #* Mostrar u ocultar botones y label de crear (máquina)
        self.ui.bt_guardar_nueva_maquina.setVisible(False)
        self.ui.bt_editar_maquina.setVisible(True)
        self.ui.label_crear_maquina.setVisible(False)
        self.ui.label_editar_maquina.setVisible(True)

        #* Mostrar u ocultar botones y label de crear (pago)
        self.ui.label_43.setVisible(False)
        self.ui.combo_clientes_pagos.setVisible(False)
        self.ui.bt_guardar_pago.setVisible(False)
        self.ui.bt_editar_pago.setVisible(True)
        self.ui.bt_imprimir.setEnabled(True)
        self.ui.bt_enviar_correo.setEnabled(True)
        self.ui.label_crear_pago.setVisible(False)
        self.ui.label_editar_pago.setVisible(True)

        #* Mostrar u ocultar botones y label de crear (gasto)
        self.ui.bt_guardar_gasto.setVisible(False)
        self.ui.bt_editar_gasto.setVisible(True)
        self.ui.label_crear_gasto.setVisible(False)
        self.ui.label_editar_gasto.setVisible(True)


    def guardar_estado_inicial(self):
        # Diccionario para almacenar el estado inicial de cada campo
        self.estado_inicial = {}

        # Guardar el estado inicial de QLineEdit y QTextEdit
        for widget in self.findChildren((QLineEdit, QTextEdit)):
            if isinstance(widget, QLineEdit):
                self.estado_inicial[widget.objectName()] = widget.text()
            elif isinstance(widget, QTextEdit):
                self.estado_inicial[widget.objectName()] = widget.toPlainText()
        
        # Guardar el estado inicial de QComboBox
        for combo in self.findChildren(QComboBox):
            self.estado_inicial[combo.objectName()] = combo.currentIndex()
        
        # Guardar el estado inicial de QDateEdit (como texto para fácil comparación)
        for date_edit in self.findChildren(QDateEdit):
            self.estado_inicial[date_edit.objectName()] = date_edit.date().toString("yyyy-MM-dd")


    def confirmar_salida(self, pagina_destino):
        # Verificar si algún campo ha cambiado respecto a su estado inicial
        campos_con_cambios = False

        # Comparar el estado actual de QLineEdit y QTextEdit con el estado inicial
        for widget in self.findChildren((QLineEdit, QTextEdit)):
            nombre_widget = widget.objectName()
            if nombre_widget == "qt_spinbox_lineedit":
                continue
            valor_actual = widget.text() if isinstance(widget, QLineEdit) else widget.toPlainText()
            if valor_actual != self.estado_inicial.get(nombre_widget, ""):
                campos_con_cambios = True
                break

        # Comparar el estado actual de QComboBox con el estado inicial
        if not campos_con_cambios:
            for combo in self.findChildren(QComboBox):
                if combo.currentIndex() != self.estado_inicial.get(combo.objectName(), -1):
                    campos_con_cambios = True
                    break

        # Comparar el estado actual de QDateEdit con el estado inicial
        if not campos_con_cambios:
            for date_edit in self.findChildren(QDateEdit):
                if date_edit.date().toString("yyyy-MM-dd") != self.estado_inicial.get(date_edit.objectName(), ""):
                    campos_con_cambios = True
                    break

        # Mostrar mensaje de confirmación solo si algún campo ha cambiado
        if campos_con_cambios:
            # Crear el cuadro de diálogo de confirmación
            mensaje = QMessageBox(self)
            mensaje.setIcon(QMessageBox.Question)
            mensaje.setWindowTitle("Confirmación de salida")
            mensaje.setText("Hay cambios sin guardar. ¿Está seguro de que quiere salir? Los cambios no se guardarán.")

            # Añadir botones "Sí" y "No"
            boton_si = mensaje.addButton("Sí", QMessageBox.YesRole)
            boton_no = mensaje.addButton("No", QMessageBox.NoRole)

            # Aplicar el estilo del mensaje sin agregar el botón "Aceptar"
            aplicar_estilo_mensaje(mensaje, agregar_boton_aceptar=False)

            # Mostrar el cuadro de diálogo y obtener la respuesta
            respuesta = mensaje.exec_()

            # Comprobar la respuesta
            if mensaje.clickedButton() != boton_si:
                return

        # Cambiar a la página de destino si no hay cambios o si el usuario confirmó
        self.ui.stackedWidget.setCurrentWidget(pagina_destino)




    def reset_button_styles(self, except_button):
        """
        Restaurar el estilo original de todos los botones excepto el que está activo.
        """
        if except_button != self.ui.bt_usuarios:
            self.ui.bt_usuarios.setStyleSheet("""
                QPushButton {
                    font: 14pt "Segoe UI";
                    background-color: #000000; 
                    border: 1px solid #000000;
                    image: url(:/iconos_principal/iconos/usuarios (1).png);
                    image-position: left center; 
                    color: white;
                    padding-left: 30px;
                    qproperty-iconSize: 24px 24px; 
                    padding-left: 40px;
                    color: white;
                    text-align: left; 
                }
                QPushButton:hover {
                image: url(:/iconos_principal/iconos/usuarios.png);
                image-position: left center; /* Mantiene el icono a la izquierda */
                color: rgb(255, 103, 4); /* Cambia el color del texto al pasar el mouse */
            }
            """)
        
        if except_button != self.ui.bt_membresias:
            self.ui.bt_membresias.setStyleSheet("""
                QPushButton {
                    font: 14pt "Segoe UI";
                    background-color: #000000; 
                    border: 1px solid #000000;
                    image: url(:/iconos_principal/iconos/plan-de-estudios.png);
                    image-position: left center; 
                    color: white;
                    padding-left: 30px;
                    qproperty-iconSize: 24px 24px; 
                    padding-left: 40px;
                    color: white;
                    text-align: left; 
                }
                QPushButton:hover {
                image: url(:/iconos_principal/iconos/plan-de-estudios (1).png);
                image-position: left center; /* Mantiene el icono a la izquierda */
                color: rgb(255, 103, 4); /* Cambia el color del texto al pasar el mouse */
            }
            """)


        if except_button != self.ui.bt_horarios:
            self.ui.bt_horarios.setStyleSheet("""
               QPushButton {
                    font: 14pt "Segoe UI";
                    background-color: #000000; 
                    border: 1px solid #000000;
                    image: url(:/iconos_principal/iconos/calendario.png);
                    image-position: left center; 
                    color: white;
                    padding-left: 30px;
                    qproperty-iconSize: 24px 24px; 
                    padding-left: 40px;
                    color: white;
                    text-align: left; 
                }
                QPushButton:hover {
                image: url(:/iconos_principal/iconos/calendario (1).png);
                image-position: left center; /* Mantiene el icono a la izquierda */
                color: rgb(255, 103, 4); /* Cambia el color del texto al pasar el mouse */
            }
            """)

        if except_button != self.ui.bt_maquinas:
            self.ui.bt_maquinas.setStyleSheet("""
               QPushButton {
                    font: 14pt "Segoe UI";
                    background-color: #000000; 
                    border: 1px solid #000000;
                    image: url(:/iconos_principal/iconos/maquina.png);
                    image-position: left center; 
                    color: white;
                    padding-left: 30px;
                    qproperty-iconSize: 24px 24px; 
                    padding-left: 40px;
                    color: white;
                    text-align: left; 
                }
                QPushButton:hover {
                image: url(:/iconos_principal/iconos/maquina1.png);
                image-position: left center; /* Mantiene el icono a la izquierda */
                color: rgb(255, 103, 4); /* Cambia el color del texto al pasar el mouse */
            }
            """)

        if except_button != self.ui.bt_pagos:
            self.ui.bt_pagos.setStyleSheet("""
               QPushButton {
                    font: 14pt "Segoe UI";
                    background-color: #000000; 
                    border: 1px solid #000000;
                    image: url(:/iconos_principal/iconos/metodo-de-pago.png);
                    image-position: left center; 
                    color: white;
                    padding-left: 30px;
                    qproperty-iconSize: 24px 24px; 
                    padding-left: 40px;
                    color: white;
                    text-align: left; 
                }
                QPushButton:hover {
                image: url(:/iconos_principal/iconos/metodo-de-pago (1).png);
                image-position: left center; /* Mantiene el icono a la izquierda */
                color: rgb(255, 103, 4); /* Cambia el color del texto al pasar el mouse */
            }
            """)
        
        if except_button != self.ui.bt_gastos:
            self.ui.bt_gastos.setStyleSheet("""
               QPushButton {
                    font: 14pt "Segoe UI";
                    background-color: #000000; 
                    border: 1px solid #000000;
                   image: url(:/iconos_principal/iconos/depreciacion.png);
                    image-position: left center; 
                    color: white;
                    padding-left: 30px;
                    qproperty-iconSize: 24px 24px; 
                    padding-left: 40px;
                    color: white;
                    text-align: left; 
                }
                QPushButton:hover {
                image: url(:/iconos_principal/iconos/depreciacion (1).png);
                image-position: left center; /* Mantiene el icono a la izquierda */
                color: rgb(255, 103, 4); /* Cambia el color del texto al pasar el mouse */
            }
            """)


    def boton_cerrar_sesion(self):
        """
        Función para cerrar sesión con confirmación.
        """
     # Crear el cuadro de diálogo de confirmación
        mensaje = QMessageBox(self)
        mensaje.setIcon(QMessageBox.Question)
        mensaje.setWindowTitle("Confirmar cierre de sesión")
        mensaje.setText("¿Está seguro(a) de que desea cerrar sesión?")

        # Añadir botones "Sí" y "No"
        boton_si = mensaje.addButton("Sí", QMessageBox.YesRole)
        boton_no = mensaje.addButton("No", QMessageBox.NoRole)

        # Aplicar el estilo del mensaje sin agregar el botón "Aceptar"
        aplicar_estilo_mensaje(mensaje, agregar_boton_aceptar=False)

        # Mostrar el cuadro de diálogo
        respuesta = mensaje.exec_()

        # Si el usuario elige "Sí", cerrar sesión
        if mensaje.clickedButton() == boton_si:
            # Cerrar la ventana actual
            self.close()

            from CapaLogica.logica_login import Login
            
            # Mostrar la ventana de inicio de sesión
            login = Login()
            login.show()