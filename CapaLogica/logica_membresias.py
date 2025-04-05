
# PyQt5 Core y Widgets

from functools import partial
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import *
from CapaLogica.Validaciones import validar_campos_obligatorios, formatear_precio
from CapaDatos.ConexionPyodbc import conexion
from Recursos.Estilos import aplicar_estilo_mensaje, aplicar_estilo_spin_activo, aplicar_estilo_spin_double_activo, aplicar_estilo_spin_double_inactivo, aplicar_estilo_spin_inactivo  
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui, QtCore


class LogicaMembresias:
    def __init__(self, ui, main_logic):
        """
        Constructor que inicializa la lógica de membresías con acceso a la interfaz de usuario.
        """
        self.ui = ui  # Recibe la interfaz como argumento para acceder a los elementos de la UI
        self.main_logic = main_logic
        # Restaurar el estilo de los otros botones
        self.main_logic.reset_button_styles(except_button=self.ui.bt_membresias)



        # Formatear el precio mientras se escribe en el campo de membresías
        self.ui.txt_precio_membresia.textChanged.connect(lambda: formatear_precio(self.ui.txt_precio_membresia))

        # Navegación a la página de membresías
        self.ui.bt_membresias.clicked.connect(self.pagina_membresias)

        # Guardar y editar membresía
        self.ui.bt_editar_membresia.clicked.connect(self.editar_membresia)
        self.ui.bt_guardar_membresia.clicked.connect(self.crear_membresia)

        # Regresar desde la página de membresías
        self.ui.bt_regresar_membresia.clicked.connect(lambda: self.main_logic.confirmar_salida(self.ui.pagina_membresias))





    def pagina_membresias(self):
        # Cambiar a la página de membresias
        self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_membresias)

        self.ui.bt_membresias.setStyleSheet("""
            QPushButton {
                font: 14pt "Segoe UI";
                background-color: #000000; 
                border: 1px solid #000000;
                image: url(:/iconos_principal/iconos/plan-de-estudios (1).png);
                image-position: left center;
                color: white;
                padding-left: 30px;
                qproperty-iconSize: 24px 24px; 
                padding-left: 40px;
                color: #FF6704;
                text-align: left; 
            }
        """)
        

        
        
        self.ui.combo_tipo_membresia.currentIndexChanged.connect(self.actualizar_campos_grupales)
        
        self.ui.spin_numero_personas.setEnabled(False)
        self.ui.spin_descuento.setSuffix(" %")
        self.ui.spin_descuento.setEnabled(False)
        self.ui.precio_descuento.setReadOnly(True)

        self.ui.spin_descuento.valueChanged.connect(self.calcular_precio_con_descuento)

        self.llenar_tabla_membresia()

        self.ui.bt_nueva_membresia.clicked.connect(self.abrir_pantalla_crear_membresia)

         # Configuraciones iniciales para que los campos estén deshabilitados y en gris membresias
        if self.ui.combo_tipo_membresia.currentText() == "Individual":
            self.ui.spin_numero_personas.setEnabled(False)
            self.ui.spin_descuento.setEnabled(False)

            # Aplicar estilo gris para que se vean inactivos
            estilo_gris_spin = aplicar_estilo_spin_inactivo()
            estilo_gris_spin_double = aplicar_estilo_spin_double_inactivo()
            self.ui.spin_numero_personas.setStyleSheet(estilo_gris_spin)
            self.ui.spin_descuento.setStyleSheet(estilo_gris_spin_double)

        # Conectar el evento del combo para actualizar los campos según el tipo de membresía seleccionado
        self.ui.combo_tipo_membresia.currentIndexChanged.connect(self.actualizar_campos_grupales)

    
    #!Método para manejar la acción de crear membresía
    def abrir_pantalla_crear_membresia(self):
        
        # Cambiar a modo de creación
        self.modo_edicion = False
    
        # Llama al método que configura el modo de creación
        self.main_logic.mostrar_modo_crear()
        # Cambia a la pantalla de creación de cliente
        self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_crear_membresias)

        #Guarda el estado inicial de los campos de texto
        self.main_logic.guardar_estado_inicial()

    def crear_membresia(self):
        # Validación de campos obligatorios
        campos_obligatorios = [
            (self.ui.txt_nombre_membresia, "Nombre membresia"),
            (self.ui.txt_precio_membresia, "Precio"),
        ]

        # usamos la funcion de validaciones
        if not validar_campos_obligatorios(campos_obligatorios, self.main_logic):
            return  # Detener la ejecución si hay campos vacíos
        
        # Tabla membresia
        nombre = self.ui.txt_nombre_membresia.text()
        descripcion = self.ui.txt_descripcion_membresia.toPlainText()
        tipo_membresia = self.ui.combo_tipo_membresia.currentText()
        duracion = self.ui.spin_duracion_membresia.value()
        precio = float(self.ui.txt_precio_membresia.text().replace(",", ""))
        cantidad_personas = self.ui.spin_numero_personas.value() if self.ui.spin_numero_personas.text() != "" else None
        descuento = self.ui.spin_descuento.value() if self.ui.spin_descuento.text() != "" else None
        precio_descuento = float(self.ui.precio_descuento.text().replace(",", "")) if self.ui.precio_descuento.text() != "" else None
        estado = self.ui.combo_estado_membresia.currentText()


        try:
            with conexion.cursor() as cursor:
                if tipo_membresia == "Individual":
                    sql = "INSERT INTO membresias (nombre, descripcion, tipo_membresia, duracion, precio_regular, estado) VALUES (%s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (nombre, descripcion, tipo_membresia, duracion, precio, estado))
                else:
                    sql = "INSERT INTO membresias (nombre, descripcion, tipo_membresia, duracion, precio_regular, cantidad_personas, descuento_porcentaje, precio_descuento, estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (nombre, descripcion, tipo_membresia, duracion, precio, cantidad_personas, descuento, precio_descuento, estado))

            # Confirmar los cambios en la base de datos
            conexion.commit()

            self.main_logic.limpiar_campos()

            # Aplicar el estilo solo a este cuadro de mensaje
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Éxito")
            mensaje.setText("La nueva membresía se ha creado correctamente")
            mensaje.setIcon(qtw.QMessageBox.Information)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()

            self.llenar_tabla_membresia()

        except Exception as ex:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Fallo al almacenar los datos, revise que la conexión a la base de datos esté disponible.")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()


    def llenar_tabla_membresia(self):
        tabla = self.ui.tabla_membresias  # Asegúrate de que este sea el nombre correcto de tu tabla
        self.ui.tabla_membresias.verticalHeader().setVisible(False)

        try:
            with conexion.cursor() as cursor:
                # Se realiza la consulta a la base de datos
                sql = """SELECT id, nombre, descripcion, tipo_membresia, duracion, precio_regular, cantidad_personas, descuento_porcentaje, precio_descuento, estado 
                         FROM membresias;"""
                
                # Se ejecuta la consulta sql con el cursor y se obtienen todas las filas 
                cursor.execute(sql)
                membresias = cursor.fetchall()

            # Ocultamos la columna 0
            self.ui.tabla_membresias.hideColumn(0)

            # Validar la existencia de la tabla antes de configurar el número de filas
            if tabla is not None:
                # Medimos la cantidad de datos de la tabla        
                i = len(membresias)
                tabla.setRowCount(i)

                # Validamos si hay por lo menos un dato para que nos muestre los mismos en la tabla
                if i > 0:
                    tablerow = 0
                    for membresia in membresias:
                        tabla.setItem(tablerow, 0, qtw.QTableWidgetItem(str(membresia[0])))
                        tabla.setItem(tablerow, 1, qtw.QTableWidgetItem(str(membresia[1])))
                        tabla.setItem(tablerow, 2, qtw.QTableWidgetItem(str(membresia[2])))
                        tabla.setItem(tablerow, 3, qtw.QTableWidgetItem(str(membresia[3])))
                        tabla.setItem(tablerow, 4, qtw.QTableWidgetItem(str(membresia[4])))

                        # Formatear el precio en la columna 5
                        if membresia[5] is not None:
                            precio_regular = "$ {:,.2f}".format(membresia[5])  # Formateo del valor numérico
                        else:
                            precio_regular = "No Aplica"
                        tabla.setItem(tablerow, 5, qtw.QTableWidgetItem(precio_regular))

                        # Formatear el número de personas, si es `None` asignar "N/A"
                        num_personas = membresia[6] if membresia[6] is not None else "N/A"
                        tabla.setItem(tablerow, 6, qtw.QTableWidgetItem(str(num_personas)))

                        # Formatear el descuento, si es `None` asignar "N/A"
                        descuento = membresia[7] if membresia[7] is not None else "N/A"
                        tabla.setItem(tablerow, 7, qtw.QTableWidgetItem(str(descuento)))

                        
                        if membresia[8] is not None:
                            precio_descuento = "{:,.2f}".format(membresia[8])  # Formateo del valor numérico
                        else:
                            precio_descuento = "No Aplica"
                        tabla.setItem(tablerow, 8, qtw.QTableWidgetItem(precio_descuento))

                    


                        # Configurar la celda de estado y cambiar el color 
                        estado_item = qtw.QTableWidgetItem(str(membresia[9]))
                        if membresia[9].lower() == "inactivo":
                            estado_item.setForeground(QtGui.QColor("red"))  # Cambiar color de texto a rojo
                            boton_estado = QPushButton()
                            boton_estado.setStyleSheet("""
                                QPushButton {
                                    image: url(:/iconos_principal/iconos/cliente_off.png);
                                    width: 35px;
                                    height: 35px 
                                }""")
                        
                        else:
                            estado_item.setForeground(QtGui.QColor("green"))  # Cambiar color de texto a rojo
                            boton_estado = QPushButton()
                            boton_estado.setStyleSheet("""
                                QPushButton {
                                    image: url(:/iconos_principal/iconos/cliente_on.png);
                                    width: 35px;
                                    height: 35px 
                                }""")


                        tabla.setItem(tablerow, 9, estado_item)

               
                        for col in range(1, 10):  
                            tabla.item(tablerow, col).setFlags(QtCore.Qt.ItemIsEnabled)

                        
                        # Crear botón Editar y usar partial para pasar la fila correcta
                        boton_editar = QPushButton()
                        boton_editar.clicked.connect(partial(self.llenar_campos_editar_membresia, tablerow))
                        boton_editar.setStyleSheet("""
                                QPushButton {
                                    image: url(:/iconos_principal/iconos/editar_tabla.png);
                                    width: 35px;
                                    height: 35px 
                                }""")
                        
                        # Crear botón Eliminar y usar partial
                        boton_eliminar = QPushButton()
                        boton_eliminar.clicked.connect(partial(self.eliminar_membresia, tablerow))
                        boton_eliminar.setStyleSheet("""
                            QPushButton {
                                image: url(:/iconos_principal/iconos/borrar_tabla.png);
                                width: 35px;
                                height: 35px 
                            }""")
                      
                        boton_estado.clicked.connect(partial(self.editar_estado_membresia, tablerow))

                        # Crear un layout horizontal para contener los botones
                        widget_opciones = QWidget()
                        layout_opciones = QHBoxLayout()
                        layout_opciones.addWidget(boton_editar)
                        layout_opciones.addWidget(boton_eliminar)
                        layout_opciones.addWidget(boton_estado)
                        layout_opciones.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes
                        widget_opciones.setLayout(layout_opciones)

                        # Insertar el widget con los botones en la columna "Opciones"
                        self.ui.tabla_membresias.setCellWidget(tablerow, 10, widget_opciones)

                        tablerow += 1
                else:
                    mensaje = qtw.QMessageBox(self.main_logic)
                    mensaje.setText("No existen membresías en el sistema")
                    mensaje.setIcon(qtw.QMessageBox.Warning)
                    aplicar_estilo_mensaje(mensaje) 
                    mensaje.exec_()

        except Exception as ex:
            print(ex)


    def eliminar_membresia(self, tablerow):

        # Obtener el ID y el nombre del cliente de la fila seleccionada
        id_membresia = self.ui.tabla_membresias.item(tablerow, 0).text()  # Suponiendo que el ID está en la columna 0
        nombre_membresia = self.ui.tabla_membresias.item(tablerow, 1).text()  # Suponiendo que el nombre está en la columna 1

        mensaje = QMessageBox(self.main_logic)
        mensaje.setIcon(QMessageBox.Question)
        mensaje.setWindowTitle("Eliminar Membresía")
        mensaje.setText(
            f"¿Estás seguro de que deseas eliminar la membresía '{nombre_membresia}'?\n\n"
            "Esta acción es irreversible y eliminará todos los datos relacionados con esta membresía en el sistema, "
            "incluyendo:\n"
            "- Pagos asociados a la membresía\n"
            "- Registros de clientes que hayan contratado esta membresía\n\n"
            "¿Deseas continuar con la eliminación?"
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

                    sql_pagos = "DELETE FROM pagos WHERE id_membresia = %s"
                    cursor.execute(sql_pagos, (id_membresia,))

                    sql_membresia = "DELETE FROM membresias WHERE id = %s"
                    cursor.execute(sql_membresia, (id_membresia,))

                    conexion.commit()

                mensaje = qtw.QMessageBox(self.main_logic)
                mensaje.setText(f"La membresía '{nombre_membresia}' ha sido eliminada correctamente.")
                mensaje.setIcon(qtw.QMessageBox.Information)
                aplicar_estilo_mensaje(mensaje) 
                mensaje.exec_()

                self.llenar_tabla_membresia()

            except Exception as e:
                mensaje = qtw.QMessageBox(self.main_logic)
                mensaje.setWindowTitle("Error")
                mensaje.setText(f"Error al eliminar la membresía, revise que la conexión a la base de datos esté disponible")
                mensaje.setIcon(qtw.QMessageBox.Critical)
                aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
                mensaje.exec_()

    def editar_estado_membresia(self, tablerow):
        # Obtener el ID y los nombres del cliente desde la tabla
        id_membresia = self.ui.tabla_membresias.item(tablerow, 0).text() 
        nombre_membresia = self.ui.tabla_membresias.item(tablerow, 1).text()
        estado_actual = self.ui.tabla_membresias.item(tablerow, 9).text()  # Columna de estado (verifica que sea la columna correcta)

 
        # Determinar el nuevo estado
        nuevo_estado = "Inactivo" if estado_actual == "Activo" else "Activo"
        accion = "desactivada" if estado_actual == "Activo" else "activada"

        try:
            # Cambiar el estado en la base de datos
            with conexion.cursor() as cursor:
                sql_cambiar_estado = "UPDATE membresias SET estado = %s WHERE id = %s"
                cursor.execute(sql_cambiar_estado, (nuevo_estado, id_membresia))
                conexion.commit()

            # Recargar la tabla para actualizarla
            self.llenar_tabla_membresia()

            # Mostrar mensaje de éxito con el nombre del cliente
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Éxito")
            mensaje.setText(f"La membresía '{nombre_membresia}' ha sido {accion} correctamente.")
            mensaje.setIcon(qtw.QMessageBox.Information)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()

        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al cambiar el estado de la membresía, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()



    def llenar_campos_editar_membresia(self, tablerow):

        # Activar el modo de edición
        self.modo_edicion = True

        self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_crear_membresias)

        id_membresia = self.ui.tabla_membresias.item(tablerow, 0).text()
        
        # Guardar el ID de la máquina para usarlo más tarde en la actualización
        self.membresia_id_actual = id_membresia

        # Obtener los demás datos desde la tabla
        nombre = self.ui.tabla_membresias.item(tablerow, 1).text()
        descripcion = self.ui.tabla_membresias.item(tablerow, 2).text()
        tipo_membresia = self.ui.tabla_membresias.item(tablerow, 3).text()
        duracion = self.ui.tabla_membresias.item(tablerow, 4).text()
        precio_regular = self.ui.tabla_membresias.item(tablerow, 5).text()
        cant_personas = self.ui.tabla_membresias.item(tablerow, 6).text()
        descuento = self.ui.tabla_membresias.item(tablerow, 7).text()
        precio_descuento = self.ui.tabla_membresias.item(tablerow, 8).text()
        estado = self.ui.tabla_membresias.item(tablerow, 9).text()


        # Cargar los datos actuales en los campos de edición de la máquina
        self.ui.txt_nombre_membresia.setText(nombre)
        self.ui.txt_descripcion_membresia.setText(descripcion)
        self.ui.combo_tipo_membresia.setCurrentText(tipo_membresia)

        # Verificar si duracion es numérico antes de convertirlo a int
        if duracion.isdigit():
            self.ui.spin_duracion_membresia.setValue(int(duracion))
        else:
            self.ui.spin_duracion_membresia.setValue(0)

        self.ui.txt_precio_membresia.setText(str(precio_regular))

        # Verificar si cant_personas es numérico antes de convertirlo a int
        if cant_personas.isdigit():
            self.ui.spin_numero_personas.setValue(int(cant_personas))
        else:
            self.ui.spin_numero_personas.setValue(0)

        # Verificar si descuento es numérico antes de convertirlo a float
        try:
            self.ui.spin_descuento.setValue(float(descuento))
        except ValueError:
            self.ui.spin_descuento.setValue(0.0)

        self.ui.precio_descuento.setText(str(precio_descuento))
        self.ui.combo_estado_membresia.setCurrentText(estado)

        # Ocultar el botón de guardar y mostrar el de editar
        self.ui.bt_guardar_membresia.setVisible(False)
        self.ui.bt_editar_membresia.setVisible(True)

        # Ocultar el label de crear y mostrar el label de editar
        self.ui.label_crear_membresia.setVisible(False)
        self.ui.label_editar_membresia.setVisible(True)
    
        #Guarda el estado inicial de los campos de texto
        self.main_logic.guardar_estado_inicial()

        #*mostrar modo editar
        self.main_logic.mostrar_modo_editar()

    def editar_membresia(self):
                # Validación de campos obligatorios
        campos_obligatorios = [
            (self.ui.txt_nombre_membresia, "Nombre membresia"),
            (self.ui.txt_precio_membresia, "Precio"),
        ]

          # usamos la funcion de validaciones
        if not validar_campos_obligatorios(campos_obligatorios, self.main_logic):
            return  # Detener la ejecución si hay campos vacíos

    
        # Tabla membresia
        nombre = self.ui.txt_nombre_membresia.text()
        descripcion = self.ui.txt_descripcion_membresia.toPlainText()
        tipo_membresia = self.ui.combo_tipo_membresia.currentText()
        duracion = self.ui.spin_duracion_membresia.value()
        precio = float(self.ui.txt_precio_membresia.text().replace(",", ""))
        cantidad_personas = self.ui.spin_numero_personas.value() if self.ui.spin_numero_personas.text() != "" else None
        descuento = self.ui.spin_descuento.value() if self.ui.spin_descuento.text() != "" else None
        precio_descuento_texto = self.ui.precio_descuento.text()
        precio_descuento = None if precio_descuento_texto == 'No Aplica' or precio_descuento_texto == "" else float(precio_descuento_texto.replace(",", ""))
        estado = self.ui.combo_estado_membresia.currentText()


        try:
            with conexion.cursor() as cursor:
                if tipo_membresia == "Individual":
                    sql = """UPDATE membresias
                        SET nombre = %s, descripcion = %s, tipo_membresia = %s, duracion = %s, precio_regular = %s, 
                        estado = %s WHERE id = %s"""
                    
                    cursor.execute(sql, (nombre, descripcion, tipo_membresia, duracion, precio, estado, self.membresia_id_actual))
                else:
                    sql = """UPDATE membresias
                        SET nombre = %s, descripcion = %s, tipo_membresia = %s, duracion = %s, precio_regular = %s, 
                        cantidad_personas = %s, descuento_porcentaje = %s, precio_descuento = %s, estado = %s WHERE id = %s"""

                    cursor.execute(sql, (nombre, descripcion, tipo_membresia, duracion, precio, cantidad_personas, descuento, precio_descuento, estado, self.membresia_id_actual))

                # Confirmar los cambios
                conexion.commit()

                mensaje = qtw.QMessageBox(self.main_logic)
                mensaje.setText("La membresía se ha editado correctamente.")
                mensaje.setIcon(qtw.QMessageBox.Information)
                aplicar_estilo_mensaje(mensaje) 
                mensaje.exec_()

                # Regresar a la vista de la tabla de clientes
                self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_membresias)

                # Recargar los datos en la tabla de clientes
                self.llenar_tabla_membresia()

        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al editar la membresía, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()    


    def actualizar_campos_grupales(self):
        # Habilitar o deshabilitar campos dependiendo del tipo de membresía seleccionado
        if self.ui.combo_tipo_membresia.currentText() == "Grupal":
            # Habilitar los campos y restaurar el estilo normal
            self.ui.spin_numero_personas.setEnabled(True)
            self.ui.spin_descuento.setEnabled(True)
            
            estilo_normal_spin = aplicar_estilo_spin_activo()
            estilo_normal_spin_double = aplicar_estilo_spin_double_activo()
            self.ui.spin_numero_personas.setStyleSheet(estilo_normal_spin)
            self.ui.spin_descuento.setStyleSheet(estilo_normal_spin_double)
        else:
            # Deshabilitar los campos y aplicar estilo gris
            self.ui.spin_numero_personas.setEnabled(False)
            self.ui.spin_descuento.setEnabled(False)
            self.ui.spin_numero_personas.setValue(2)
            self.ui.spin_descuento.setValue(0)
            self.ui.precio_descuento.clear()

            estilo_gris_spin = aplicar_estilo_spin_inactivo()
            estilo_gris_spin_double = aplicar_estilo_spin_double_inactivo()
            self.ui.spin_numero_personas.setStyleSheet(estilo_gris_spin)
            self.ui.spin_descuento.setStyleSheet(estilo_gris_spin_double)
        
    def calcular_precio_con_descuento(self):
        # Obtener el precio unitario
        precio_unitario_text = self.ui.txt_precio_membresia.text().replace(",", "")
        if precio_unitario_text:
            precio_unitario = float(precio_unitario_text)

            # Obtener la cantidad del QSpinBox
            cantidad = self.ui.spin_cantidad.value()

            # Obtener el porcentaje de descuento definido por el administrador (QDoubleSpinBox)
            descuento_porcentaje = self.ui.spin_descuento.value() / 100  # Convertir de porcentaje a decimal

            # Calcular el precio total con el descuento
            precio_total = precio_unitario * cantidad * (1 - descuento_porcentaje)

            # Formatear el precio total para mostrarlo con el formato adecuado
            precio_total_formateado = "{:,.2f}".format(precio_total)


            self.ui.precio_descuento.setText(precio_total_formateado)
        else:
            # Si no hay precio unitario, limpiar el campo de valor total
            self.ui.precio_descuento.clear()


    def activar_boton_membresias(self):
        self.main_logic.reset_button_styles(self.ui.bt_membresias)
        # Otra lógica específica para el botón de membresías