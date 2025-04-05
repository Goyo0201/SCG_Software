

# PyQt5 Core y Widgets
from datetime import date, datetime
from decimal import Decimal
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import partial
import os
import smtplib
import tempfile
import time
from PyQt5.QtCore import QDate, QPoint, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QRegion
from PyQt5.QtPrintSupport import QPrintPreviewDialog, QPrinter
from PyQt5.QtWidgets import *
from CapaLogica.Validaciones import formatear_precio_base_datos
from CapaDatos.ConexionPyodbc import conexion
from Recursos.Estilos import aplicar_estilo_mensaje, aplicar_estilo_progress_dialog
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from dotenv import load_dotenv



class LogicaPagos:
    def __init__(self, ui, main_logic):
        """
        Constructor que inicializa la lógica de pagos con acceso a la interfaz de usuario.
        """
        self.ui = ui  # Recibe la interfaz como argumento para acceder a los elementos de la UI
        self.main_logic = main_logic
        # Restaurar el estilo de los otros botones
        self.main_logic.reset_button_styles(except_button=self.ui.bt_pagos)

        # Inicializar bandera para saber si ya se ha generado el número de factura
        self.numero_factura_generado = False
               # Definir actualizando_combo para controlar los eventos de cambio en el ComboBox
        self.actualizando_combo = False

        # Navegación a la página de pagos
        self.ui.bt_pagos.clicked.connect(self.pagina_pagos)

        # Configuración del botón de regreso de la página de pagos con confirmación
        self.ui.bt_regresar_pago.clicked.connect(lambda: self.main_logic.confirmar_salida(self.ui.pagina_pagos))

        # Cambio en el ComboBox de pagos por mes
        self.ui.combo_buscar_pagos_mes.currentIndexChanged.connect(self.pagina_buscar_por_mes)

        # Configuración de botones para agregar, editar, imprimir, y enviar recibo
        # Agregar un nuevo recibo
        self.ui.bt_guardar_pago.clicked.connect(self.crear_recibo)

        # Editar un pago existente
        self.ui.bt_editar_pago.clicked.connect(self.editar_pago)

        # Imprimir el recibo
        self.ui.bt_imprimir.clicked.connect(self.imprimir_recibo)

        # Enviar el recibo por correo electrónico
        self.ui.bt_enviar_correo.clicked.connect(self.preparar_y_enviar_correo)




    def pagina_pagos(self):
        # Cambiar a la página de 
        self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_pagos)

        self.ui.bt_pagos.setStyleSheet("""
            QPushButton {
                font: 14pt "Segoe UI";
                background-color: #000000; 
                border: 1px solid #000000;
                image: url(:/iconos_principal/iconos/metodo-de-pago (1).png);
                image-position: left center;
                color: white;
                padding-left: 30px;
                qproperty-iconSize: 24px 24px; 
                padding-left: 40px;
                color: #FF6704;
                text-align: left; 
            }
        """)

        
        self.ui.bt_regresar_pagos_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_pagos))
        self.ui.bt_agregar_pago.clicked.connect(self.abrir_pantalla_crear_pago)


        self.ui.bt_buscar_pago.clicked.connect(self.pagina_buscar_pagos)

        self.llenar_tabla_pagos()
        
        # Cargar las medidas del primer cliente (dato 0) si está disponible
        self.llenar_combo_clientes_pagos()
        self.llenar_combo_membresias_pagos()
        



        # Acciones para pagos
        self.ui.txt_fecha_inicio_factura.setDate(QDate.currentDate())


        self.calcular_fecha_vencimiento()

        # Obtener el número de factura solo si no se ha generado previamente
        if not self.numero_factura_generado:
            self.obtener_numero_factura()
            self.numero_factura_generado = True
        
        # Generar el número de factura si no está definido
        if not self.ui.txt_numero_factura.text():  # Si no hay un número ya definido
            self.obtener_numero_factura()

        # Seleccionar el primer cliente si existen elementos
        if self.ui.combo_clientes_pagos.count() > 0:
            self.ui.combo_clientes_pagos.setCurrentIndex(0)
            self.llenar_recibo()  # Llenar recibo con el primer cliente seleccionado

        # Seleccionar la primera membresía si existen elementos
        if self.ui.combo_membresia.count() > 0:
            self.ui.combo_membresia.setCurrentIndex(0)
            self.actualizar_precio_y_total()  # Actualizar el valor unitario con la membresía seleccionada

        # Conectar el evento de cambio de selección del ComboBox (cambiando entre valores del combo)
        self.ui.combo_clientes_pagos.currentIndexChanged.connect(self.llenar_recibo)
        self.ui.combo_membresia.currentIndexChanged.connect(self.actualizar_precio_y_total)
        self.ui.spin_cantidad.valueChanged.connect(self.actualizar_precio_y_total)
        self.ui.combo_membresia.currentIndexChanged.connect(self.calcular_fecha_vencimiento)

    #!Método para manejar la acción de crear pago
    def abrir_pantalla_crear_pago(self):
        # Cambiar a modo de creación
        self.modo_edicion = False
        # Llama al método que configura el modo de creación
        self.main_logic.mostrar_modo_crear()
        # Cambia a la pantalla de creación de cliente
        self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_crear_pago)
        #Guarda el estado inicial de los campos de texto
        self.main_logic.guardar_estado_inicial()
        # Llenar los combos de clientes y membresías y seleccionar un valor inicial para asegurar que estén correctamente seleccionados (iniciando la página)
        #Mostrar alerta de campos vacios
        self.llenar_combo_clientes_pagos(mostrar_advertencia=True)
        self.llenar_combo_membresias_pagos(mostrar_advertencia=True)

        



    def crear_recibo(self):
        print("Iniciando la creación del recibo...")
        # Obtener datos del recibo desde los campos de la interfaz
        fecha_inicio = self.ui.txt_fecha_inicio_factura.text()
        fecha_fin = self.ui.txt_fecha_fin_factura.text()
        numero_factura = int(self.ui.txt_numero_factura.text())
        nombres = self.ui.txt_nombre_cliente_factura.text()
        cedula = int(self.ui.txt_cedula_factura.text())
        direccion = self.ui.txt_direccion_cliente_factura.text()
        telefono = self.ui.txt_telefono_factura.text()
        cantidad = self.ui.spin_cantidad.value()
        membresia = self.ui.combo_membresia.currentText()
        valor_unitario = float(self.ui.txt_valor_unitario.text().replace(",", ""))
        valor_total = float(self.ui.txt_valor_total.text().replace(",", ""))
        observaciones = self.ui.txt_observaciones.toPlainText()
        subtotal = float(self.ui.txt_subtotal.text().replace(",", ""))
        descuento = float(self.ui.txt_porcentaje_recibo.text().replace("%", "").strip())
        total_full = float(self.ui.txt_total_full.text().replace(",", ""))

        # Obtener IDs desde los ComboBox
        id_cliente = self.ui.combo_clientes_pagos.currentData()
        id_membresia = self.ui.combo_membresia.currentData()

        if isinstance(id_cliente, tuple):
            id_cliente = id_cliente[0]

        if isinstance(id_membresia, tuple):
            id_membresia = id_membresia[0]

        # Validar si los IDs fueron seleccionados
        if id_cliente is None or id_membresia is None:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText("Debe seleccionar un cliente y una membresía antes de continuar.")
            mensaje.setIcon(qtw.QMessageBox.Warning)
            aplicar_estilo_mensaje(mensaje)
            mensaje.exec_()
            return

        try:
            with conexion.cursor() as cursor:
                print("Ejecutando consulta SQL para insertar el recibo...")
                # Verificar si el cliente tiene una membresía en pagos y si está expirada
                cursor.execute("""
                    SELECT id_cliente, membresia, fecha_inicio, fecha_fin
                    FROM pagos
                    WHERE id_cliente = %s
                """, (id_cliente,))
                membresia_actual = cursor.fetchone()

                if membresia_actual:
                    fecha_fin_actual = membresia_actual[3]  # Cambiamos 'fecha_fin' por el índice numérico correspondiente
                    dias_restantes = (fecha_fin_actual - datetime.now().date()).days


                    if dias_restantes <= 0:
                        # Si la membresía está expirada, moverla al historial y eliminarla de pagos sin preguntar
                        cursor.execute("""
                            INSERT INTO historial_pagos (id_cliente, membresia, fecha_inicio, fecha_fin)
                            SELECT id_cliente, membresia, fecha_inicio, fecha_fin
                            FROM pagos
                            WHERE id_cliente = %s
                        """, (id_cliente,))
                        
                        cursor.execute("DELETE FROM pagos WHERE id_cliente = %s", (id_cliente,))
 
                        # cambiar el estado a "Activo"
                        cursor.execute("UPDATE clientes SET estado = 'Activo' WHERE id = %s", (id_cliente,))
                        conexion.commit()
                    else:
                        
                        mensaje = QMessageBox(self.main_logic)
                        mensaje.setIcon(QMessageBox.Question)
                        mensaje.setWindowTitle("Eliminar Membresía")
                        mensaje.setText("El cliente ya tiene una membresía activa. ¿Desea reemplazarla?")

                        # Añadir botones "Sí" y "No"
                        boton_si = mensaje.addButton("Sí", QMessageBox.YesRole)
                        boton_no = mensaje.addButton("No", QMessageBox.NoRole)

                        # Aplicar el estilo del mensaje
                        aplicar_estilo_mensaje(mensaje, agregar_boton_aceptar=False)

                        # Mostrar el cuadro de diálogo y obtener la respuesta
                        respuesta = mensaje.exec_()

                        # Comprobar la respuesta
                        if mensaje.clickedButton() == boton_no:
                            return  # Si el usuario selecciona "No", cancelamos la operación
                        else:
                            # Mover la membresía activa al historial y eliminarla de pagos
                            cursor.execute("""
                                INSERT INTO historial_pagos (id_cliente, membresia, fecha_inicio, fecha_fin)
                                SELECT id_cliente, membresia, fecha_inicio, fecha_fin
                                FROM pagos
                                WHERE id_cliente = %s
                            """, (id_cliente,))
                            cursor.execute("DELETE FROM pagos WHERE id_cliente = %s", (id_cliente,))

                # Insertar los datos del nuevo recibo en la tabla pagos
                sql = """INSERT INTO pagos (num_factura, fecha_inicio, fecha_fin, nombre_cliente, direccion_cliente, 
                        cedula_cliente, telefono_cliente, cantidad, membresia, valor_unitario, valor_total, observaciones, 
                        subtotal, descuento, total_completo, id_cliente, id_membresia) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (numero_factura, fecha_inicio, fecha_fin, nombres, direccion, cedula, telefono,
                                    cantidad, membresia, valor_unitario, valor_total, observaciones, subtotal, 
                                    descuento, total_full, id_cliente, id_membresia))
                
                conexion.commit()
                

                # Verificar si el pago fue realmente insertado
                cursor.execute("SELECT COUNT(*) FROM pagos WHERE num_factura = %s AND id_cliente = %s", (numero_factura, id_cliente))
                resultado = cursor.fetchone()
                
                # Habilitar y mostrar los botones si se guardó el pago correctamente
                if resultado and resultado[0] > 0:
                    
                    self.ui.bt_imprimir.setEnabled(True)
                    self.ui.bt_enviar_correo.setEnabled(True)
    

            self.main_logic.limpiar_campos()

            
            # Mostrar mensaje de éxito
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Éxito")
            mensaje.setText("Datos almacenados correctamente")
            mensaje.setIcon(qtw.QMessageBox.Information)
            aplicar_estilo_mensaje(mensaje)
            mensaje.exec_()

            # Después de guardar, se genera un nuevo número de factura
            self.numero_factura_generado = False
            self.obtener_numero_factura()

            self.llenar_tabla_pagos()

            print("Creación exitosa, retornando True")
            return True  

        except Exception as ex:
            # Revertir cambios si ocurre una excepción
            conexion.rollback()
            # Mostrar mensaje de error si ocurre una excepción
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Fallo al almacenar los datos, revise que la conexión a la base de datos esté disponible.")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)
            mensaje.exec_()

            return False


    def llenar_tabla_pagos(self):
        tabla = self.ui.tabla_pagos
        self.ui.tabla_pagos.verticalHeader().setVisible(False)
     
        try:
            with conexion.cursor() as cursor:
                # Consulta SQL para obtener los datos
                sql = """SELECT num_factura, nombre_cliente, membresia, fecha_inicio, fecha_fin, valor_total FROM pagos"""
                cursor.execute(sql)
                pagos = cursor.fetchall()
                print(pagos)  # Verificar que se obtienen resultados

            if tabla is not None:
                i = len(pagos)
                tabla.setRowCount(i)

                if i > 0:
                    tablerow = 0
                    
                    for pago in pagos:
                        try:

                            fecha_fin = pago[4]
                            hoy = datetime.now().date()  # Obtenemos solo la fecha actual

                            # Cálculo de días restantes
                            dias_restantes = (fecha_fin - hoy).days if fecha_fin >= hoy else 0

                            # Añadir los elementos a la tabla
                            tabla.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(pago[0])))
                            tabla.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(pago[1])))
                            tabla.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(pago[2])))
                            tabla.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(pago[3])))
                            tabla.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(pago[4])))
                            tabla.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(dias_restantes)))  # Días restantes

                            if pago[5] is not None:
                                total = "$ {:,.2f}".format(pago[5])  # Formateo del valor numérico
                            else:
                                total = "No Aplica"
                            tabla.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(total))

                            # Desactivar la edición de las celdas agregadas (excepto la primera columna ID)
                            for col in range(0, 7):
                                tabla.item(tablerow, col).setFlags(QtCore.Qt.ItemIsEnabled)

                            # Crear botón Editar y usar partial para pasar la fila correcta
                            boton_editar = QtWidgets.QPushButton()
                            boton_editar.clicked.connect(partial(self.llenar_campos_editar_pago, tablerow))
                            boton_editar.setStyleSheet("""
                                QPushButton {
                                    image: url(:/iconos_principal/iconos/editar_tabla.png);
                                    width: 35px;
                                    height: 35px 
                                }""")    

                            # Crear botón Eliminar y usar partial
                            boton_eliminar = QtWidgets.QPushButton()
                            boton_eliminar.clicked.connect(partial(self.eliminar_pago, tablerow))
                            boton_eliminar.setStyleSheet("""
                                QPushButton {
                                    image: url(:/iconos_principal/iconos/borrar_tabla.png);
                                    width: 35px;
                                    height: 35px 
                                }""")    

                            # Crear un layout horizontal para contener los botones
                            widget_opciones = QtWidgets.QWidget()
                            layout_opciones = QtWidgets.QHBoxLayout()
                            layout_opciones.addWidget(boton_editar)
                            layout_opciones.addWidget(boton_eliminar)
                            layout_opciones.setContentsMargins(0, 0, 0, 0)
                            widget_opciones.setLayout(layout_opciones)

                            # Insertar el widget con los botones en la columna "Opciones"
                            self.ui.tabla_pagos.setCellWidget(tablerow, 7, widget_opciones)

                            tablerow += 1

                        except Exception as e:
                            print(f"Error al procesar el pago: {e}")

                else:

                    mensaje = qtw.QMessageBox(self.main_logic)
                    mensaje.setText("No existen pagos en el sistema.")
                    mensaje.setIcon(qtw.QMessageBox.Warning)
                    aplicar_estilo_mensaje(mensaje) 
                    mensaje.exec_()

        except Exception as ex:
            print(ex)
     

    def eliminar_pago(self, tablerow):
       
        num_factura = self.ui.tabla_pagos.item(tablerow, 0).text()  
        nombre_cliente = self.ui.tabla_pagos.item(tablerow, 1).text()  

        mensaje = QMessageBox(self.main_logic)
        mensaje.setIcon(QMessageBox.Question)
        mensaje.setWindowTitle("Eliminar pago")
        mensaje.setText(
            f"¿Estás seguro de que deseas eliminar el pago asociado al cliente '{nombre_cliente}'?"
        )

        # Añadir botones "Sí" y "No"
        boton_si = mensaje.addButton("Sí", QMessageBox.YesRole)
        boton_no = mensaje.addButton("No", QMessageBox.NoRole)

        # Aplicar el estilo del mensaje
        aplicar_estilo_mensaje(mensaje, agregar_boton_aceptar=False)

        # Mostrar el cuadro de diálogo y obtener la respuesta
        respuesta = mensaje.exec_()

        # Comprobar la respuesta
        if mensaje.clickedButton() == boton_si:
            try:
                
                with conexion.cursor() as cursor:
                   
                    sql = "DELETE FROM pagos WHERE num_factura = %s"
                    cursor.execute(sql, (num_factura,))
                    
                    conexion.commit()

                mensaje = qtw.QMessageBox(self.main_logic)
                mensaje.setText(f"El pago del cliente '{nombre_cliente}' ha sido eliminado correctamente.")
                mensaje.setIcon(qtw.QMessageBox.Information)
                aplicar_estilo_mensaje(mensaje) 
                mensaje.exec_()

                self.llenar_tabla_pagos()

            except Exception as e:
                mensaje = qtw.QMessageBox(self.main_logic)
                mensaje.setWindowTitle("Error")
                mensaje.setText(f"Error al eliminar el pago, revise que la conexión a la base de datos esté disponible")
                mensaje.setIcon(qtw.QMessageBox.Critical)
                aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
                mensaje.exec_()


    def llenar_campos_editar_pago(self, tablerow):

        # Activar el modo de edición
        self.modo_edicion = True


        self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_crear_pago)
 
        num_factura = self.ui.tabla_pagos.item(tablerow, 0).text() 

                # Hacer la consulta para obtener los datos completos del cliente
        try:
            with conexion.cursor() as cursor:
                # Consulta para obtener todos los datos del cliente
                sql = """SELECT num_factura, fecha_inicio, fecha_fin, nombre_cliente, direccion_cliente, cedula_cliente, 
                telefono_cliente, cantidad, membresia, valor_unitario, valor_total, observaciones, subtotal, descuento, total_completo FROM pagos WHERE num_factura = %s"""
                cursor.execute(sql, (num_factura,))
                resultado = cursor.fetchone()

                if resultado:
                    (num_factura, fecha_inicio, fecha_fin, nombre_cliente, direccion_cliente, cedula_cliente, 
                     telefono_cliente, cantidad, membresia, valor_unitario, valor_total, observaciones, subtotal, descuento, total_completo) = resultado

                    # Convertir las fechas a QDate
                    formato_fecha = "yyyy-MM-dd"
                    fecha_inicio_qdate = QDate.fromString(str(fecha_inicio), formato_fecha)
                    fecha_fin_qdate = QDate.fromString(str(fecha_fin), formato_fecha)

                    # Cargar los datos del cliente en los campos de edición
                    self.ui.txt_numero_factura.setText(str(num_factura))
                    self.ui.txt_fecha_inicio_factura.setDate(fecha_inicio_qdate)
                    self.ui.txt_fecha_fin_factura.setDate(fecha_fin_qdate)
                    self.ui.txt_nombre_cliente_factura.setText(nombre_cliente)
                    self.ui.txt_direccion_cliente_factura.setText(direccion_cliente)
                    self.ui.txt_cedula_factura.setText(str(cedula_cliente))
                    self.ui.txt_telefono_cliente.setText(str(telefono_cliente))
                    self.ui.spin_cantidad.setValue(int(cantidad))
                    self.ui.combo_membresia.setCurrentText(membresia)
                    self.ui.txt_valor_unitario.setText(str(valor_unitario))
                    self.ui.txt_valor_total.setText(str(valor_total))
                    self.ui.txt_observaciones.setText(observaciones)
                    self.ui.txt_subtotal.setText(str(subtotal))
                    self.ui.txt_porcentaje_recibo.setText(str(descuento))
                    self.ui.txt_total_full.setText(str(total_completo))

                    #Guarda el estado inicial de los campos de texto
                    self.main_logic.guardar_estado_inicial()

                    #*mostrar modo editar
                    self.main_logic.mostrar_modo_editar()

                # Guardar el ID del cliente que estamos editando
                self.factura_num_actual = num_factura

        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al cargar los datos del cliente, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()

    def editar_pago(self):
        
        # Obtener los valores editados desde los campos    

        fecha_inicio = self.ui.txt_fecha_inicio_factura.text()
        fecha_fin = self.ui.txt_fecha_fin_factura.text()   
        cantidad = self.ui.spin_cantidad.value()
        membresia = self.ui.combo_membresia.currentText()
        valor_unitario = float(self.ui.txt_valor_unitario.text().replace(",", ""))
        valor_total = float(self.ui.txt_valor_total.text().replace(",", ""))
        observaciones = self.ui.txt_observaciones.toPlainText()
        subtotal = float(self.ui.txt_subtotal.text().replace(",", ""))
        descuento = float(self.ui.txt_porcentaje_recibo.text().replace("%", "").strip())
        total_full = float(self.ui.txt_total_full.text().replace(",", ""))


        try:
            with conexion.cursor() as cursor:
                # Actualizar los datos del cliente en la base de datos
                sql_cliente = """
                    UPDATE pagos SET fecha_inicio = %s, fecha_fin = %s, cantidad = %s, membresia = %s, 
                    valor_unitario = %s, valor_total = %s, observaciones = %s, subtotal = %s, descuento = %s, total_completo = %s WHERE num_factura = %s"""
                
                cursor.execute(sql_cliente, (fecha_inicio, fecha_fin, cantidad, membresia, valor_unitario, valor_total, observaciones, subtotal, descuento, total_full,
                                            self.factura_num_actual))

                # Confirmar los cambios
                conexion.commit()

                mensaje = qtw.QMessageBox(self.main_logic)
                mensaje.setWindowTitle("Éxito")
                mensaje.setText("El pago ha sido actualizado correctamente.")
                mensaje.setIcon(qtw.QMessageBox.Information)
                aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
                mensaje.exec_()

                # Regresar a la vista de la tabla de clientes
                self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_pagos)

                # Recargar los datos en la tabla de clientes
                self.llenar_tabla_pagos()

        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al actualizar el pago, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()


    def llenar_combo_clientes_pagos(self, mostrar_advertencia=False):
        try:
            with conexion.cursor() as cursor:
                # Obtener todos los clientes
                sql = "SELECT id, nombres, apellidos FROM clientes WHERE estado = 'Activo' OR estado = 'Expirado'"
                cursor.execute(sql)
                clientes = cursor.fetchall()

                # Desactivar las señales mientras se llena el ComboBox
                self.ui.combo_clientes_pagos.blockSignals(True)

                if not clientes:
                    if mostrar_advertencia:
                        # Si no hay clientes, agregar "Sin datos" y mostrar un mensaje de advertencia
                        mensaje = qtw.QMessageBox(self.main_logic)
                        mensaje.setText("No se encontraron clientes en el sistema.")
                        mensaje.setIcon(qtw.QMessageBox.Warning)
                        aplicar_estilo_mensaje(mensaje)
                        mensaje.exec_()

                # Llenar el ComboBox con los nombres, apellidos e ID de los clientes
                self.ui.combo_clientes_pagos.clear()
                for cliente in clientes:
                    id_cliente = cliente[0]
                    nombre_completo = f"{cliente[1]} {cliente[2]}"
                    # Agregar al ComboBox el nombre, pero guardar el ID único
                    self.ui.combo_clientes_pagos.addItem(nombre_completo, id_cliente)

                # Reactivar las señales después de llenar el ComboBox
                self.ui.combo_clientes_pagos.blockSignals(False)

        except Exception as ex:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"No se pudo cargar el listado de clientes, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()

    def llenar_combo_membresias_pagos(self, mostrar_advertencia=False):
        try:
            with conexion.cursor() as cursor:
                # Obtener las membresías
                sql = "SELECT id, nombre, precio_regular, descuento_porcentaje, precio_descuento, duracion FROM membresias WHERE estado = 'Activo'"
                cursor.execute(sql)
                membresias = cursor.fetchall()

                # Desactivar las señales mientras se llena el ComboBox
                self.ui.combo_membresia.blockSignals(True)

                if not membresias:
                    if mostrar_advertencia:
                        # Si no hay clientes, agregar "Sin datos" y mostrar un mensaje de advertencia
                        mensaje = qtw.QMessageBox(self.main_logic)
                        mensaje.setText("No se encontraron membresías en el sistema.")
                        mensaje.setIcon(qtw.QMessageBox.Warning)
                        aplicar_estilo_mensaje(mensaje)
                        mensaje.exec_()

                # Llenar el ComboBox de membresías
                self.ui.combo_membresia.clear()
                for membresia in membresias:
                    id = membresia[0]
                    nombre = membresia[1]
                    precio = membresia[2]
                    descuento = membresia[3]
                    precio_decuento = membresia[4]
                    duracion = membresia[5]
                    # Agregar al ComboBox el nombre
                    self.ui.combo_membresia.addItem(nombre, (id, precio, descuento, precio_decuento, duracion))

                # Reactivar las señales después de llenar el ComboBox
                self.ui.combo_membresia.blockSignals(False)

        except Exception as ex:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"No se pudo cargar el listado de membresías, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()


    def actualizar_precio_y_total(self):
        # Obtener la tupla con el precio del ComboBox (que es el dato asociado al elemento seleccionado)
        data = self.ui.combo_membresia.currentData()

        if data is not None:
            _, precio, descuento, _, _,  = data  # Desempaquetar la tupla

            # Convertir precio y descuento a float si son Decimal
            precio = float(precio) if isinstance(precio, Decimal) else precio
            descuento = float(descuento) if isinstance(descuento, Decimal) else descuento

            # Establecer valores predeterminados si alguno de los valores es None
            precio = precio or 0.0
            descuento = descuento or 0.0

            # Actualizar el campo del valor unitario con el precio formateado
            formatear_precio_base_datos(self.ui.txt_valor_unitario, precio)

            # Actualizar el campo de porcentaje de descuento con el valor obtenido
            self.ui.txt_porcentaje_recibo.setText(f"{descuento:.2f} %")

            # Obtener la cantidad del QSpinBox
            cantidad = self.ui.spin_cantidad.value()

            # Calcular el total sin descuento
            total = cantidad * precio

            # Calcular el total con descuento
            total_con_descuento = total * (1 - descuento / 100)

            # Formatear los totales con separadores de miles y dos decimales
            total_formateado = "{:,.2f}".format(total)
            total_con_descuento_formateado = "{:,.2f}".format(total_con_descuento)

            # Colocar el total en el campo de texto
            self.ui.txt_valor_total.setText(total_formateado)
            self.ui.txt_subtotal.setText(total_formateado)
            self.ui.txt_total_full.setText(total_con_descuento_formateado)

        else:
            # Limpiar los campos si no hay un precio válido seleccionado
            self.ui.txt_valor_unitario.clear()
            self.ui.txt_porcentaje_recibo.clear()
            self.ui.txt_total_full.clear()
            self.ui.txt_valor_total.clear()
            self.ui.txt_subtotal.clear()


    def llenar_recibo(self):       

        # Si la variable de control está activada, salir para evitar que la función se ejecute al llenar el ComboBox
        if self.actualizando_combo:
            return 
         
        # Obtiene el ID único del cliente
        id_cliente = self.ui.combo_clientes_pagos.currentData()

        
        try:
            with conexion.cursor() as cursor:
                # Obtener datos del cliente
                sql = """SELECT nombres, apellidos, num_cedula, direccion, telefono 
                        FROM clientes 
                        WHERE id = %s;"""
                cursor.execute(sql, (id_cliente,))
                cliente = cursor.fetchone()

                if cliente:
                    # Llenar los campos del recibo con los datos del cliente
                    self.ui.txt_nombre_cliente_factura.setText(f"{cliente[0]} {cliente[1]}")
                    self.ui.txt_cedula_factura.setText(str(cliente[2]))  # Convertir a cadena
                    self.ui.txt_direccion_cliente_factura.setText(cliente[3])
                    self.ui.txt_telefono_factura.setText(str(cliente[4]))  # Convertir a cadena

        except Exception as ex:
            # Mostrar un mensaje de error al usuario
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al obtener datos del cliente, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()



    def calcular_fecha_vencimiento(self):
        # Obtener la fecha de inicio de la factura
        fecha_inicio = self.ui.txt_fecha_inicio_factura.date()  # Obtener la fecha desde el QDateEdit
        
        # Obtener la duración de la membresía en días desde la base de datos
        data = self.ui.combo_membresia.currentData()
        if data is not None:
            _, _, _, _, duracion = data  # Extraer la duración de la membresía (en días)
            
            # Sumar la duración de días a la fecha de inicio para calcular la fecha de vencimiento
            fecha_vencimiento = fecha_inicio.addDays(duracion)
            
            # Establecer la fecha de vencimiento en el campo correspondiente
            self.ui.txt_fecha_fin_factura.setDate(fecha_vencimiento)

        else:
            # Limpiar el campo de fecha de vencimiento si no hay membresía seleccionada
            self.ui.txt_fecha_fin_factura.clear()

    def obtener_numero_factura(self):
        try:
            with conexion.cursor() as cursor:
                # Obtener el último número de factura y sumar 1
                sql = "SELECT MAX(num_factura) FROM pagos"
                cursor.execute(sql)
                resultado = cursor.fetchone()

                # Si hay facturas previas, sumar 1 al último número de factura
                if resultado[0] is not None:
                    nuevo_numero_factura = resultado[0] + 1
                else:
                    # Si no hay facturas previas, empezar con el número 1000
                    nuevo_numero_factura = 1000

                # Mostrar el nuevo número de factura en el campo de texto
                self.ui.txt_numero_factura.setText(str(nuevo_numero_factura))

        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"No se pudo obtener el número de factura, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()



    def imprimir_recibo(self):
        # Configurar la impresora con alta resolución y tamaño de página A4
        printer = QPrinter(QPrinter.HighResolution)
        printer.setResolution(600)  # Aumentar la resolución a 600 DPI
        printer.setPageSize(QPrinter.A4)  # Configura el tamaño de la página a A4
        printer.setOrientation(QPrinter.Portrait)  # Orientación vertical

        # Crear la vista previa de impresión
        vista_previa = QPrintPreviewDialog(printer, self)
        
        # Conectar el evento de renderizado y mostrar el diálogo de vista previa
        vista_previa.paintRequested.connect(self.renderizar_recibo_en_printer)

        # Configurar la vista previa para que ajuste al ancho
        vista_previa.setWindowFlags(vista_previa.windowFlags() | Qt.WindowMaximizeButtonHint)
        vista_previa.resize(900, 600)  # Ajusta el tamaño para visualizar mejor
        vista_previa.exec_()


    def renderizar_recibo_en_printer(self, printer):
        # Crear un pintor para dibujar en el contenido del frame con calidad mejorada
        painter = QPainter(printer)
        
        # Escalar el contenido para llenar la página
        frame_rect = self.ui.frame_6.rect()  # Obtiene el rectángulo del frame
        page_rect = printer.pageRect()  # Obtiene el rectángulo de la página
        
        # Calcular la escala para ajustar el frame al tamaño de la página
        scale_x = page_rect.width() / frame_rect.width()
        scale_y = page_rect.height() / frame_rect.height()
        scale = min(scale_x, scale_y)  # Escalar para que se ajuste en ambos ejes
        
        painter.scale(scale, scale)
        
        # Renderizar el frame en el área escalada
        self.ui.frame_6.render(painter, QPoint(0, 0), QRegion(frame_rect))

        # Finalizar el pintor
        painter.end()



    #*función para enviar por correo
    def capturar_frame_como_imagen(self):
        # Captura el contenido de frame_6 como una imagen QPixmap
        pixmap = self.ui.frame_6.grab()
        return pixmap


    def guardar_imagen_temporal(self, pixmap):
        # Define un nombre más claro para el archivo temporal
        temp_file_path = os.path.join(tempfile.gettempdir(), "recibo_pago.png")
        pixmap.save(temp_file_path, "PNG")
        return temp_file_path


    def preparar_y_enviar_correo(self):
        # Obtener el ID del cliente seleccionado en el combo box
        cliente_id = self.ui.combo_clientes_pagos.currentData()

        # Obtener el correo del cliente
        try:
            with conexion.cursor() as cursor:
                sql = "SELECT correo FROM clientes WHERE id = %s"
                cursor.execute(sql, (cliente_id,))
                resultado = cursor.fetchone()

                if resultado and resultado[0]:  # Verifica que haya un correo
                    correo_cliente = resultado[0]
                    asunto = "Recibo de Pago"
                    mensaje = "Adjuntamos el recibo de su pago. Gracias por su preferencia."

                    # Capturar el frame como imagen y guardarla temporalmente
                    pixmap = self.capturar_frame_como_imagen()
                    archivo_adjunto = self.guardar_imagen_temporal(pixmap)

                    # Enviar el correo con el archivo adjunto
                    self.enviar_correo(correo_cliente, asunto, mensaje, archivo_adjunto)
                else:
                    QMessageBox.warning(self, "Error", "No se encontró el correo del cliente seleccionado.")
        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al obtener el correo del cliente, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()


    def enviar_correo(self, destinatario, asunto, mensaje, archivo_adjunto):
        try:
            load_dotenv()
            password = os.getenv("password")
            remitente = "sportcentergym64@gmail.com"
            
            # Crear el mensaje de correo
            msg = MIMEMultipart()
            msg['From'] = remitente
            msg['To'] = destinatario
            msg['Subject'] = asunto
            
            # Agregar el mensaje de texto
            msg.attach(MIMEText(mensaje, 'plain'))
            
            # Adjuntar el archivo con un nombre más claro
            with open(archivo_adjunto, "rb") as adj:
                parte_adjunto = MIMEBase('application', 'octet-stream')
                parte_adjunto.set_payload(adj.read())
                encoders.encode_base64(parte_adjunto)
                parte_adjunto.add_header('Content-Disposition', f"attachment; filename=recibo_pago.png")
                msg.attach(parte_adjunto)
            
            # Configurar el progreso
            self.progress_dialog = QProgressDialog(f"Preparando para enviar correo a: {destinatario}", "Cancelar", 0, 100, self)
            self.progress_dialog = aplicar_estilo_progress_dialog(self.progress_dialog)
            self.progress_dialog.setWindowModality(Qt.WindowModal)
            self.progress_dialog.setMinimumDuration(0)
            self.progress_dialog.setValue(0)
            self.envio_cancelado = False

            # Establecer cancelación
            self.progress_dialog.canceled.connect(self.cancelar_envio)

            # Fase inicial de progreso
            for progress in range(0, 70, 5):
                if self.envio_cancelado:
                    raise Exception("Envío cancelado por el usuario.")
                self.progress_dialog.setValue(progress)
                time.sleep(0.3)

            # Desactivar el botón de cancelar y cambiar el texto
            self.progress_dialog.setCancelButtonText(None)
            self.progress_dialog.setLabelText(f"Enviando correo a: {destinatario}")
            
            # Enviar el correo en la fase final mientras la barra sigue progresando
            servidor = smtplib.SMTP('smtp.gmail.com', 587)
            servidor.starttls()
            servidor.login(remitente, password)
            servidor.sendmail(remitente, destinatario, msg.as_string())
            servidor.quit()

            # Fase final de progreso
            for progress in range(70, 101, 5):
                if self.envio_cancelado:
                    raise Exception("Envío cancelado por el usuario.")
                self.progress_dialog.setValue(progress)
                time.sleep(0.2)

            # Mensaje de confirmación
            if not self.envio_cancelado:
                mensaje = qtw.QMessageBox(self.main_logic)
                mensaje.setText(f"El recibo se ha enviado correctamente por correo a {destinatario}.")
                mensaje.setIcon(qtw.QMessageBox.Information)
                aplicar_estilo_mensaje(mensaje) 
                mensaje.exec_()

        except Exception as e:
            if self.envio_cancelado:
                mensaje = qtw.QMessageBox(self.main_logic)
                mensaje.setText("El envío del correo ha sido cancelado.")
                mensaje.setIcon(qtw.QMessageBox.Information)
                aplicar_estilo_mensaje(mensaje) 
                mensaje.exec_()
            else:
                mensaje = qtw.QMessageBox(self.main_logic)
                mensaje.setWindowTitle("Error")
                mensaje.setText(f"Error al enviar el correo.")
                mensaje.setIcon(qtw.QMessageBox.Critical)
                aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
                mensaje.exec_()
        finally:
            if hasattr(self, 'progress_dialog'):
                self.progress_dialog.close()

    def cancelar_envio(self):
        self.envio_cancelado = True




    #>Pagina buscar pagos 
 
    def pagina_buscar_pagos(self):
        # Cambiar a la página de pagos
        self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_buscar_pago)
        self.ui.tabWidget_2.setCurrentIndex(0)

        # Llamamos la función para buscar cliente por nombre
        self.ui.txt_buscar_pago_cliente_nombre.textChanged.connect(self.buscar_pago_por_cliente)
        self.ui.Lista_pagos_clientes_por_nombre.itemClicked.connect(self.mostrar_pago_en_tabla)

        # Para que cada vez que entre a buscar cliente por nombre se limpien los datos
        self.ui.bt_buscar_cliente.clicked.connect(self.limpiar_busqueda_pago)
    
        

    #!Manejo de tabs
    #*TAB - 0
    # Función para buscar clientes por nombre
    def buscar_pago_por_cliente(self):
        nombre_cliente = self.ui.txt_buscar_pago_cliente_nombre.text()

        # Limpiar la lista de clientes antes de cargar nuevos resultados
        self.ui.Lista_pagos_clientes_por_nombre.clear()

        try:
            with conexion.cursor() as cursor:
                # Consulta SQL para buscar clientes por nombre
                sql = "SELECT id, num_cedula, nombres, apellidos, telefono, correo, direccion FROM clientes WHERE nombres LIKE %s"
                cursor.execute(sql, ('%' + nombre_cliente + '%',))
                resultados = cursor.fetchall()

                # Cargar los resultados en el QListWidget
                for id_cliente, cedula, nombres, apellidos, telefono, correo, direccion in resultados:
                    item_texto = f"{nombres} {apellidos} - {cedula}"
                    item = QListWidgetItem(item_texto)
                    item.setData(Qt.UserRole, id_cliente)  # Guardar el ID del cliente en el ítem
                    self.ui.Lista_pagos_clientes_por_nombre.addItem(item)
                    
        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al buscar los clientes, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()


    # Función para mostrar los detalles del cliente en la QTableWidget
    def mostrar_pago_en_tabla(self, item):
        self.ui.tabla_pagos_clientes_nombre.verticalHeader().setVisible(False)
        id_cliente = item.data(Qt.UserRole)  # Obtener el ID del cliente del ítem seleccionado

        try:
            with conexion.cursor() as cursor:
                # Consulta SQL para obtener los detalles del pago y cliente
                sql = """
                    SELECT 
                        CONCAT(c.nombres, ' ', c.apellidos) AS nombre_completo,
                        m.nombre AS membresia,
                        p.fecha_inicio,
                        p.fecha_fin,
                        p.valor_total
                    FROM 
                        pagos p
                    JOIN 
                        clientes c ON p.id_cliente = c.id
                    JOIN 
                        membresias m ON p.id_membresia = m.id
                    WHERE 
                        c.id = %s;
                """
                cursor.execute(sql, (id_cliente,))
                resultado = cursor.fetchone()

                if resultado:
                    nombre_completo, membresia, fecha_inicio, fecha_fin, valor_total = resultado

                    # Calcular los días restantes hasta la fecha de vencimiento
                    if fecha_fin:
                        hoy = datetime.now().date()
                        fecha_fin_date = datetime.strptime(str(fecha_fin), "%Y-%m-%d").date()
                        dias_restantes = (fecha_fin_date - hoy).days if fecha_fin_date >= hoy else 0
                    else:
                        dias_restantes = "N/A"  # En caso de que no haya fecha de vencimiento

                    # Limpiar la tabla antes de cargar los datos
                    self.ui.tabla_pagos_clientes_nombre.setRowCount(0)
                    self.ui.tabla_pagos_clientes_nombre.insertRow(0)
                    self.ui.tabla_pagos_clientes_nombre.setItem(0, 0, QTableWidgetItem(nombre_completo))
                    self.ui.tabla_pagos_clientes_nombre.setItem(0, 1, QTableWidgetItem(membresia))
                    self.ui.tabla_pagos_clientes_nombre.setItem(0, 2, QTableWidgetItem(str(fecha_inicio)))
                    self.ui.tabla_pagos_clientes_nombre.setItem(0, 3, QTableWidgetItem(str(fecha_fin)))
                    # Formatear el precio en la columna 4
                    if valor_total is not None:
                        valor_total_formateado = "$ {:,.2f}".format(valor_total)  # Formateo del valor numérico
                    else:
                        valor_total_formateado = "No Aplica"
                    self.ui.tabla_pagos_clientes_nombre.setItem(0, 4, QTableWidgetItem(valor_total_formateado))

                    self.ui.tabla_pagos_clientes_nombre.setItem(0, 5, QTableWidgetItem(str(dias_restantes)))

                    

        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al cargar los detalles del cliente, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()

    # Función para limpiar la búsqueda de pagos
    def limpiar_busqueda_pago(self):
        # Limpiar el campo de texto del nombre del cliente
        self.ui.txt_buscar_pago_cliente_nombre.clear()

        # Limpiar el QListWidget donde aparecen los nombres filtrados
        self.ui.Lista_pagos_clientes_por_nombre.clear()

        # Limpiar la tabla donde se muestran los detalles del cliente
        self.ui.tabla_pagos_clientes_nombre.setRowCount(0)



    #*TAB - 1 ----------------------------------------------------
    # Página para buscar el historial de clientes
    def pagina_buscar_historial(self):
        # Cambiar a la página de historial de pagos
        self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_buscar_pagos_clientes)

        # Limpiar el ComboBox y la tabla de historial
        self.ui.combo_buscar_pagos_cliente.clear()  # Limpiar el ComboBox
        self.ui.tabla_pagos_clientes.setRowCount(0)  # Limpiar la tabla

        # Llenar el ComboBox con clientes únicos que tienen historial de pagos
        clientes_historial = self.cargar_clientes_con_historial_combobox(mostrar_advertencia=True)

         # Solo conectar el combobox y cargar el primer cliente si hay clientes cargados
        if clientes_historial:
            # Conectar el combobox al evento de selección
            self.ui.combo_buscar_pagos_cliente.currentIndexChanged.connect(self.cliente_seleccionado_historial)
            
            # Cargar las medidas del primer cliente (dato 0) si está disponible
            self.cliente_seleccionado_historial()

          
    # FUNCIONES BUSCAR HISTORIAL DE CLIENTES
    def cargar_clientes_con_historial_combobox(self, mostrar_advertencia=False):
        try:
            # Realizar la consulta para obtener solo los clientes únicos que tienen historial de pagos
            with conexion.cursor() as cursor:
                sql = """
                SELECT c.id, c.nombres, c.apellidos
                FROM clientes c
                JOIN historial_pagos h ON c.id = h.id_cliente
                GROUP BY c.id, c.nombres, c.apellidos
                """
                cursor.execute(sql)
                resultados = cursor.fetchall()

                # Verificar si no hay resultados
                if not resultados:
                    if mostrar_advertencia:
                        mensaje = qtw.QMessageBox(self.main_logic)
                        mensaje.setText("No se encontraron clientes con historial de pagos.")
                        mensaje.setIcon(qtw.QMessageBox.Warning)
                        aplicar_estilo_mensaje(mensaje)
                        mensaje.exec_()
                    return False  # Indicar que no hay clientes cargados

                # Cargar los resultados en el ComboBox
                for id_cliente, nombres, apellidos in resultados:
                    cliente_nombre = f"{nombres} {apellidos}"
                    self.ui.combo_buscar_pagos_cliente.addItem(cliente_nombre, id_cliente)

                    

                return True  # Indicar que se cargaron clientes exitosamente

        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al cargar el historial, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()
            return False

    def cliente_seleccionado_historial(self):
        # Limpiar la tabla antes de cargar nuevos datos
        self.ui.tabla_pagos_clientes.setRowCount(0)
        self.ui.tabla_pagos_clientes.verticalHeader().setVisible(False)

        # Obtener el ID del cliente seleccionado del ComboBox
        id_cliente = self.ui.combo_buscar_pagos_cliente.currentData()

        if id_cliente is None:
            return

        try:
            # Realizar la consulta para obtener el historial del cliente seleccionado
            with conexion.cursor() as cursor:
                sql = """
                SELECT c.num_cedula, c.nombres, c.apellidos, h.membresia, h.fecha_inicio, h.fecha_fin
                FROM clientes c
                INNER JOIN historial_pagos h ON c.id = h.id_cliente
                WHERE h.id_cliente = %s
                """
                cursor.execute(sql, (id_cliente,))
                resultados = cursor.fetchall()

                if resultados:
                    # Llenar la tabla con los resultados
                    for fila, (cedula, nombre, apellido, membresia, fecha_inicio, fecha_fin) in enumerate(resultados):
                        self.ui.tabla_pagos_clientes.insertRow(fila)
                        self.ui.tabla_pagos_clientes.setItem(fila, 0, QTableWidgetItem(str(cedula)))
                        self.ui.tabla_pagos_clientes.setItem(fila, 1, QTableWidgetItem(nombre))
                        self.ui.tabla_pagos_clientes.setItem(fila, 2, QTableWidgetItem(apellido))
                        self.ui.tabla_pagos_clientes.setItem(fila, 3, QTableWidgetItem(membresia))
                        self.ui.tabla_pagos_clientes.setItem(fila, 4, QTableWidgetItem(str(fecha_inicio)))
                        self.ui.tabla_pagos_clientes.setItem(fila, 5, QTableWidgetItem(str(fecha_fin)))

                        # Desactivar la edición de las celdas 
                        for col in range(6): 
                            for row in range(self.ui.tabla_pagos_clientes.rowCount()):
                                item = self.ui.tabla_pagos_clientes.item(row, col)
                                if item is not None:
                                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)  
                else:
                    # Mostrar un mensaje si no se encontraron datos de historial para el cliente
                    mensaje = qtw.QMessageBox(self.main_logic)
                    mensaje.setWindowTitle("Advertencia")
                    mensaje.setText("No se encontraron registros de pagos para el cliente seleccionado.")
                    mensaje.setIcon(qtw.QMessageBox.Warning)
                    aplicar_estilo_mensaje(mensaje)
                    mensaje.exec_()

        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al cargar el historial, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()


    #*TAB -2 -------------------------------------------------------------------------

    def pagina_buscar_expirados(self):
            tabla = self.ui.tabla_pagos_expirados  # Asegúrate de que este sea el nombre correcto de tu tabla
            self.ui.tabla_pagos_expirados.verticalHeader().setVisible(False)

            try:
                with conexion.cursor() as cursor:
                    # Se realiza la consulta a la base de datos (mostrar todos los clientes incluso aquellos que no tienen un pago asociado LEFT JOIN)
                    sql = """SELECT clientes.num_cedula, clientes.nombres, clientes.apellidos, pagos.membresia, pagos.fecha_inicio, pagos.fecha_fin
                        FROM clientes INNER JOIN pagos ON clientes.id = pagos.id_cliente WHERE estado = 'Expirado'"""

                    # Se ejecuta la consulta sql con el cursor y se obtienen todas las filas 
                    cursor.execute(sql)
                    clientes = cursor.fetchall()


                # Validar la existencia de la tabla antes de configurar el número de filas
                if tabla is not None:
                    # Medimos la cantidad de datos de la tabla        
                    i = len(clientes)
                    tabla.setRowCount(i)

                    # Validamos si hay por lo menos un dato para que nos muestre los mismos en la tabla
                    if i > 0:
                        tablerow = 0
                        for cliente in clientes:

                            # Añadir los elementos a la tabla
                            tabla.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(cliente[0])))
                            tabla.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(cliente[1])))
                            tabla.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(cliente[2])))
                            tabla.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(cliente[3])))
                            tabla.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(cliente[4])))
                            tabla.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(cliente[5])))

                            # Desactivar la edición de las celdas agregadas (excepto la primera columna ID)
                            for col in range(0, 6):
                                tabla.item(tablerow, col).setFlags(QtCore.Qt.ItemIsEnabled)

                            tablerow += 1
                    else:
                        # Mostrar mensaje de éxito
                        mensaje = qtw.QMessageBox(self.main_logic)
                        mensaje.setWindowTitle("Éxito")
                        mensaje.setText(f"No existen clientes con estado 'Expirado' en el sistema")
                        mensaje.setIcon(qtw.QMessageBox.Warning)
                        aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
                        mensaje.exec_()
                
            except Exception as ex:
                print(ex)



    #*TAB - 3 ------------------------------------------------------------------------
    #FUNCION BUSCAR PAGOS POR MES
    def pagina_buscar_por_mes(self):
        # Obtener el mes seleccionado en el ComboBox
        mes_seleccionado = self.ui.combo_buscar_pagos_mes.currentText()
        self.ui.tabla_pagos_mes.verticalHeader().setVisible(False)
        
        # Diccionario para mapear los nombres de los meses al número correspondiente
        meses = {
            "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4,
            "Mayo": 5, "Junio": 6, "Julio": 7, "Agosto": 8,
            "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12
        }
        
        # Convertir el mes seleccionado al número correspondiente
        mes_numero = meses.get(mes_seleccionado)
        anio_actual = date.today().year  # Usar el año actual para la consulta

        # Limpiar la tabla antes de cargar nuevos resultados
        self.ui.tabla_pagos_mes.setRowCount(0)
        
        try:
            with conexion.cursor() as cursor:
                # Consulta SQL para obtener pagos de un mes y año específicos
                sql = """
                SELECT nombre_cliente, fecha_inicio, fecha_fin, membresia, valor_total
                FROM pagos
                WHERE MONTH(fecha_inicio) = %s AND YEAR(fecha_inicio) = %s
                """
                cursor.execute(sql, (mes_numero, anio_actual))
                resultados = cursor.fetchall()

                # Verificar si no hay resultados
                if not resultados:
                    mensaje = qtw.QMessageBox(self.main_logic)
                    mensaje.setText(f"No hay pagos registrados en {mes_seleccionado} de {anio_actual}.")
                    mensaje.setIcon(qtw.QMessageBox.Warning)
                    aplicar_estilo_mensaje(mensaje) 
                    mensaje.exec_()
                    return

                # Calcular el total de ingresos y mostrar los resultados en la tabla
                total_ingresos = 0
                for fila_num, (nombre_cliente, fecha_inicio, fecha_fin, membresia, valor_total) in enumerate(resultados):
                    self.ui.tabla_pagos_mes.insertRow(fila_num)
                    
                    # Insertar los datos en cada columna de la fila
                    self.ui.tabla_pagos_mes.setItem(fila_num, 0, QTableWidgetItem(nombre_cliente))
                    self.ui.tabla_pagos_mes.setItem(fila_num, 1, QTableWidgetItem(str(fecha_inicio)))
                    self.ui.tabla_pagos_mes.setItem(fila_num, 2, QTableWidgetItem(str(fecha_fin)))
                    self.ui.tabla_pagos_mes.setItem(fila_num, 3, QTableWidgetItem(membresia))
                    # Formatear el valor_total con dos decimales y símbolo de $
                    valor_total_formateado = "$ {:,.2f}".format(valor_total)
                    self.ui.tabla_pagos_mes.setItem(fila_num, 4, QTableWidgetItem(valor_total_formateado))

                                       # Desactivar la edición de las celdas 
                    for col in range(5): 
                        for row in range(self.ui.tabla_pagos_mes.rowCount()):
                            item = self.ui.tabla_pagos_mes.item(row, col)
                            if item is not None:
                                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)  

                    # Sumar al total de ingresos
                    total_ingresos += valor_total

                #
                # Mostrar el total de ingresos en el label con formato
                self.ui.txt_total_ingresos.setText(f"$ {total_ingresos:,.2f}")

                                      
        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al obtener los pagos, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()

    #*TAB - 4 ------------------------------------------------------------------------
    def pagina_buscar_ultimos_pagos(self):
            tabla = self.ui.tabla_ultimos_pagos  # Asegúrate de que este sea el nombre correcto de tu tabla
            self.ui.tabla_ultimos_pagos.verticalHeader().setVisible(False)

            try:
                with conexion.cursor() as cursor:
                    # Se realiza la consulta a la base de datos (mostrar todos los clientes incluso aquellos que no tienen un pago asociado LEFT JOIN)
                    sql = """
                        SELECT clientes.num_cedula, clientes.nombres, clientes.apellidos, pagos.membresia, pagos.total_completo, pagos.fecha_inicio, pagos.fecha_fin
                        FROM clientes 
                        INNER JOIN pagos ON clientes.id = pagos.id_cliente 
                        WHERE pagos.fecha_fin >= CURDATE() - INTERVAL 7 DAY
                    """

                    # Se ejecuta la consulta sql con el cursor y se obtienen todas las filas 
                    cursor.execute(sql)
                    clientes = cursor.fetchall()


                # Validar la existencia de la tabla antes de configurar el número de filas
                if tabla is not None:
                    # Medimos la cantidad de datos de la tabla        
                    i = len(clientes)
                    tabla.setRowCount(i)

                    # Validamos si hay por lo menos un dato para que nos muestre los mismos en la tabla
                    if i > 0:
                        tablerow = 0
                        for cliente in clientes:

                            # Añadir los elementos a la tabla
                            tabla.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(cliente[0])))
                            tabla.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(cliente[1])))
                            tabla.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(cliente[2])))
                            tabla.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(cliente[3])))

                            valor_total_formateado = "$ {:,.2f}".format(cliente[4])
                            tabla.setItem(tablerow, 4, QTableWidgetItem(valor_total_formateado))

                            tabla.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(cliente[5])))
                            tabla.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(cliente[6])))

                            # Desactivar la edición de las celdas agregadas (excepto la primera columna ID)
                            for col in range(0, 7):
                                tabla.item(tablerow, col).setFlags(QtCore.Qt.ItemIsEnabled)

                            tablerow += 1
                    else:
                        # Mostrar mensaje de éxito
                        mensaje = qtw.QMessageBox(self.main_logic)
                        mensaje.setWindowTitle("Éxito")
                        mensaje.setText(f"No existen clientes con estado 'Expirado' en el sistema")
                        mensaje.setIcon(qtw.QMessageBox.Warning)
                        aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
                        mensaje.exec_()
                
            except Exception as ex:
                print(ex)

    def activar_boton_pagos(self):
        self.main_logic.reset_button_styles(self.ui.bt_pagos)
        # Otra lógica específica para el botón de pagos