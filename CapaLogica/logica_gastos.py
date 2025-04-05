
# PyQt5 Core y Widgets
from datetime import date
from functools import partial
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import *
from CapaLogica.Validaciones import  formatear_precio, validar_campos_obligatorios
from CapaDatos.ConexionPyodbc import conexion
from Recursos.Estilos import aplicar_estilo_mensaje
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtWidgets, QtCore



class LogicaGastos:
    def __init__(self, ui, main_logic):
        """
        Constructor que inicializa la lógica de gastos con acceso a la interfaz de usuario.
        """
        self.ui = ui  # Recibe la interfaz como argumento para acceder a los elementos de la UI
        self.main_logic = main_logic
        # Restaurar el estilo de los otros botones
        self.main_logic.reset_button_styles(except_button=self.ui.bt_gastos)


        # Navegación a la página de gastos
        self.ui.bt_gastos.clicked.connect(self.pagina_gastos)

        # Formateo en tiempo real del monto de gasto
        self.ui.txt_monto_gasto.textChanged.connect(lambda: formatear_precio(self.ui.txt_monto_gasto))

        # Guardar un nuevo gasto
        self.ui.bt_guardar_gasto.clicked.connect(self.crear_gasto)

        # Guardar cambios al editar un gasto existente
        self.ui.bt_editar_gasto.clicked.connect(self.editar_gasto)

        # Configurar botón para regresar de la página de gastos con confirmación
        self.ui.bt_regresar_gastos.clicked.connect(lambda: self.main_logic.confirmar_salida(self.ui.pagina_gastos))



    def pagina_gastos(self):
        # Cambiar a la página de 
        self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_gastos)

        self.ui.bt_gastos.setStyleSheet("""
            QPushButton {
                font: 14pt "Segoe UI";
                background-color: #000000; 
                border: 1px solid #000000;
                image: url(:/iconos_principal/iconos/depreciacion (1).png);
                image-position: left center;
                color: white;
                padding-left: 30px;
                qproperty-iconSize: 24px 24px; 
                padding-left: 40px;
                color: #FF6704;
                text-align: left; 
            }
        """)

        
        self.ui.bt_agregar_gasto.clicked.connect(self.abrir_pantalla_crear_gasto)

        # Conectar los radio buttons a la función que actualiza el ComboBox
        self.ui.radio_gasto_maquinas.toggled.connect(self.actualizar_combo_maquinas)
        self.ui.radio_gasto_entrenadores.toggled.connect(self.actualizar_combo_entrenadores)

        self.llenar_tabla_gastos()
        self.mostrar_advertencia_maquinas = True
        self.mostrar_advertencia_entrenadores = True
        


    #!Método para manejar la acción de crear gasto
    def abrir_pantalla_crear_gasto(self):
        # Cambiar a modo de creación
        self.modo_edicion = False
        # Llama al método que configura el modo de creación
        self.main_logic.mostrar_modo_crear()
        # Cambia a la pantalla de creación de cliente
        self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_crear_gasto)
        #Guarda el estado inicial de los campos de texto
        self.main_logic.guardar_estado_inicial()

        self.ui.combo_gasto_maquina.setVisible(False)


    def crear_gasto(self):
        
        # Validación de campos obligatorios
        campos_obligatorios = [
        (self.ui.txt_monto_gasto, "Monto"),
        ]
         # usamos la funcion de validaciones
        if not validar_campos_obligatorios(campos_obligatorios, self.main_logic):
            return  # Detener la ejecución si hay campos vacíos

        # Obtener los valores de los campos
        fecha = self.ui.txt_fecha_gasto.date().toString('yyyy-MM-dd')
        descripcion = self.ui.txt_descripcion_gasto.toPlainText()
        monto = float(self.ui.txt_monto_gasto.text().replace(",", ""))


        # Asegurarse de que la descripción no esté vacía
        if not descripcion:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setText("La descripción no puede estar vacía.")
            mensaje.setIcon(qtw.QMessageBox.Warning)
            aplicar_estilo_mensaje(mensaje) 
            mensaje.exec_()
            return

        # Obtener la selección de radio button y el ID correspondiente
        if self.ui.radio_gasto_maquinas.isChecked():
            self.ui.combo_gasto_maquina.setVisible(True)
            self.ui.combo_gasto_entrenador.setVisible(False)
            destino = "maquina"
            id_destino = self.ui.combo_gasto_maquina.currentData()  # Obtener el ID de la máquina
        elif self.ui.radio_gasto_entrenadores.isChecked():
            self.ui.combo_gasto_maquina.setVisible(False)
            self.ui.combo_gasto_entrenador.setVisible(True)
            destino = "entrenador"
            id_destino = self.ui.combo_gasto_entrenador.currentData()  # Obtener el ID del entrenador
        else:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setText("Debe seleccionar si el gasto es para una máquina o un entrenador.")
            mensaje.setIcon(qtw.QMessageBox.Warning)
            aplicar_estilo_mensaje(mensaje) 
            mensaje.exec_()
            return

        # Obtener el tipo de gasto
        tipo_gasto = self.ui.combo_tipo_gasto.currentText()

        # Verificar que haya seleccionado un tipo de gasto
        if not tipo_gasto:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setText("Debes seleccionar un tipo de gasto.")
            mensaje.setIcon(qtw.QMessageBox.Warning)
            aplicar_estilo_mensaje(mensaje) 
            mensaje.exec_()
            return

        try:
            with conexion.cursor() as cursor:
                # Guardar en la tabla gastos
                sql = "INSERT INTO gastos (fecha, monto, tipo_gasto, descripcion) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (fecha, monto, tipo_gasto, descripcion))
                gasto_id = cursor.lastrowid  # Obtener el ID del gasto insertado

                # Guardar en la tabla correspondiente según el tipo de gasto (máquina o entrenador)
                if destino == "maquina":
                    sql = "INSERT INTO maquinas_gastos (id_gasto, id_maquina) VALUES (%s, %s)"
                    cursor.execute(sql, (gasto_id, id_destino))
                elif destino == "entrenador":
                    sql_entrenador_gasto = "INSERT INTO entrenadores_gastos (id_gasto, id_entrenador) VALUES (%s, %s)"
                    cursor.execute(sql_entrenador_gasto, (gasto_id, id_destino))
                
                # Confirmar los cambios
                conexion.commit()

                # Limpiar los campos y actualizar la tabla de gastos
                self.main_logic.limpiar_campos()
                self.llenar_tabla_gastos()

                # Mostrar mensaje de éxito
                mensaje = qtw.QMessageBox(self.main_logic)
                mensaje.setWindowTitle("Éxito")
                mensaje.setText("Datos almacenados correctamente")
                mensaje.setIcon(qtw.QMessageBox.Information)
                aplicar_estilo_mensaje(mensaje)
                mensaje.exec_()

        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al guardar el gasto, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()


    #arreglar detalles 
    def llenar_tabla_gastos(self):
        tabla = self.ui.tabla_gastos
        self.ui.tabla_gastos.verticalHeader().setVisible(False)

        try:
            with conexion.cursor() as cursor:
                # Consulta unificada para obtener los gastos de entrenadores y máquinas
                sql = """
                    SELECT gastos.id, entrenadores.nombres AS asociado, 'Entrenador' AS tipo_asociado, gastos.tipo_gasto, gastos.descripcion, gastos.monto, gastos.fecha
                    FROM gastos
                    INNER JOIN entrenadores_gastos ON gastos.id = entrenadores_gastos.id_gasto
                    INNER JOIN entrenadores ON entrenadores.id = entrenadores_gastos.id_entrenador

                    UNION

                    SELECT gastos.id, maquinas.nombre AS asociado, 'Máquina' AS tipo_asociado, gastos.tipo_gasto, gastos.descripcion, gastos.monto, gastos.fecha
                    FROM gastos
                    INNER JOIN maquinas_gastos ON gastos.id = maquinas_gastos.id_gasto
                    INNER JOIN maquinas ON maquinas.id = maquinas_gastos.id_maquina;
                """
                cursor.execute(sql)
                gastos = cursor.fetchall()
            
            # Ocultamos la columna 0
            self.ui.tabla_gastos.hideColumn(0)

            # Validar la existencia de la tabla antes de configurar el número de filas
            if tabla is not None:
                # Medimos la cantidad de datos de la tabla        
                i = len(gastos)
                tabla.setRowCount(i)

                # Validamos si hay por lo menos un dato para que nos muestre los mismos en la tabla
                if i > 0:
                    tablerow = 0
                    for gasto in gastos:
                        tabla.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(gasto[0])))
                        tabla.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(gasto[1])))
                        tabla.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(gasto[2])))
                        tabla.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(gasto[3])))
                        tabla.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(gasto[4])))
                        


                        if gasto[5] is not None:
                                total = "$ {:,.2f}".format(gasto[5])  # Formateo del valor numérico
                        else:
                            total = "No Aplica"
                        tabla.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(total))


                        tabla.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(gasto[6])))
                        
                        for col in range(0, 7):
                            tabla.item(tablerow, col).setFlags(QtCore.Qt.ItemIsEnabled)

                        # Crear los botones de "Editar" y "Eliminar"
                        boton_editar = QPushButton()
                        boton_editar.clicked.connect(partial(self.llenar_campos_editar_gasto, tablerow))
                        boton_editar.setStyleSheet("""
                            QPushButton {
                                image: url(:/iconos_principal/iconos/editar_tabla.png);
                                width: 35px;
                                height: 35px 
                            }""")    

                        boton_eliminar = QPushButton()
                        boton_eliminar.clicked.connect(partial(self.eliminar_gasto, tablerow))
                        boton_eliminar.setStyleSheet("""
                            QPushButton {
                                image: url(:/iconos_principal/iconos/borrar_tabla.png);
                                width: 35px;
                                height: 35px 
                            }""")    


                        # Crear un layout horizontal para contener los botones
                        widget_opciones = QWidget()
                        layout_opciones = QHBoxLayout()
                        layout_opciones.addWidget(boton_editar)
                        layout_opciones.addWidget(boton_eliminar)
                        layout_opciones.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes
                        widget_opciones.setLayout(layout_opciones)

                        # Insertar el widget con los botones en la columna "Opciones"
                        self.ui.tabla_gastos.setCellWidget(tablerow, 7, widget_opciones)

                        tablerow += 1
                else:
                    mensaje = qtw.QMessageBox(self.main_logic)
                    mensaje.setText("No existen gastos en el sistema.")
                    mensaje.setIcon(qtw.QMessageBox.Warning)
                    aplicar_estilo_mensaje(mensaje) 
                    mensaje.exec_()
                    
        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al cargar los gastos, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()



    # FUNCION PARA ELIMINAR GASTO
    def eliminar_gasto(self, tablerow):
        
         # Obtener el ID y el nombre del entrenador de la fila seleccionada
        id_gasto = self.ui.tabla_gastos.item(tablerow, 0).text()  # Suponiendo que el ID está en la columna 0
        tipo_asociado = self.ui.tabla_gastos.item(tablerow, 2).text()  # Suponiendo que el nombre está en la columna 1
        tipo_gasto = self.ui.tabla_gastos.item(tablerow, 3).text()

        mensaje = QMessageBox(self.main_logic)
        mensaje.setIcon(QMessageBox.Question)
        mensaje.setWindowTitle("Eliminar gasto")
        mensaje.setText(
            f"¿Estás seguro de que deseas eliminar el gasto '{tipo_asociado} {tipo_gasto}'?"
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
                    # Determinar si el gasto corresponde a una máquina o a un entrenador
                    # Buscamos en 'entrenadores_gastos' primero
                    sql = "SELECT id_entrenador FROM entrenadores_gastos WHERE id_gasto = %s"
                    cursor.execute(sql, (id_gasto,))
                    entrenador_resultado = cursor.fetchone()

                    if entrenador_resultado:
                        # Si el gasto pertenece a un entrenador, eliminamos de 'entrenadores_gastos'
                        sql = "DELETE FROM entrenadores_gastos WHERE id_gasto = %s"
                        cursor.execute(sql, (id_gasto,))
                    else:
                        # Si el gasto no pertenece a un entrenador, buscamos en 'maquinas_gastos'
                        sql = "SELECT id_maquina FROM maquinas_gastos WHERE id_gasto = %s"
                        cursor.execute(sql, (id_gasto,))
                        maquina_resultado = cursor.fetchone()

                        if maquina_resultado:
                            # Si el gasto pertenece a una máquina, eliminamos de 'maquinas_gastos'
                            sql = "DELETE FROM maquinas_gastos WHERE id_gasto = %s"
                            cursor.execute(sql, (id_gasto,))
                        else:
                            # Si no se encontró en ninguna de las dos, mostramos un error
                            mensaje = qtw.QMessageBox(self.main_logic)
                            mensaje.setWindowTitle("Error")
                            mensaje.setText(f"No se encontró el gasto especificado, revise que la conexión a la base de datos esté disponible")
                            mensaje.setIcon(qtw.QMessageBox.Critical)
                            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
                            mensaje.exec_()
                            return

                    # Finalmente, eliminar el gasto de la tabla 'gastos'
                    sql = "DELETE FROM gastos WHERE id = %s"
                    cursor.execute(sql, (id_gasto,))
                    
                    # Confirmar los cambios en la base de datos
                    conexion.commit()

                # Mensaje de éxito
                mensaje = qtw.QMessageBox(self.main_logic)
                mensaje.setText("El gasto ha sido eliminado correctamente.")
                mensaje.setIcon(qtw.QMessageBox.Information)
                aplicar_estilo_mensaje(mensaje) 
                mensaje.exec_()

                self.llenar_tabla_gastos()

            except Exception as e:
                mensaje = qtw.QMessageBox(self.main_logic)
                mensaje.setWindowTitle("Error")
                mensaje.setText(f"Error al eliminar el gasto, revise que la conexión a la base de datos esté disponible")
                mensaje.setIcon(qtw.QMessageBox.Critical)
                aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
                mensaje.exec_()



    # Función para llenar el ComboBox con máquinas
    def llenar_combo_maquinas_gastos(self):  
        try:
            with conexion.cursor() as cursor:
                # Consulta para obtener los nombres de las máquinas
                sql = "SELECT id, nombre FROM maquinas"
                cursor.execute(sql)
                resultados = cursor.fetchall()

                # Limpiar el ComboBox antes de agregar los nuevos datos
                self.ui.combo_gasto_maquina.clear()

                # Llenar el ComboBox si hay resultados
                if resultados:
                    for fila in resultados:
                        self.ui.combo_gasto_maquina.addItem(fila[1], fila[0])  # fila[1] es el nombre, fila[0] es el ID

        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al cargar las máquinas, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()

    # Función para llenar el ComboBox con entrenadores
    def llenar_combo_entrenadores_gastos(self):
        try:
            with conexion.cursor() as cursor:
                # Consulta para obtener los nombres de los entrenadores
                sql = "SELECT id, nombres FROM entrenadores"
                cursor.execute(sql)
                resultados = cursor.fetchall()

                # Limpiar el ComboBox antes de agregar los nuevos datos
                self.ui.combo_gasto_entrenador.clear()

                # Llenar el ComboBox si hay resultados
                if resultados:
                    for fila in resultados:
                        self.ui.combo_gasto_entrenador.addItem(fila[1], fila[0])  # fila[1] es el nombre, fila[0] es el ID

        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al cargar los entrenadores, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()


    def actualizar_combo_maquinas(self):
        """Actualiza el ComboBox de máquinas y muestra advertencia si está vacío."""
        # Ocultar el ComboBox de entrenadores y mostrar el de máquinas
        self.ui.combo_gasto_entrenador.hide()
        self.ui.combo_gasto_maquina.show()

        # Llenar el ComboBox de máquinas
        self.llenar_combo_maquinas_gastos()

        # Mostrar advertencia solo si el ComboBox de máquinas está vacío y la advertencia no se ha mostrado
        if self.ui.combo_gasto_maquina.count() == 0 and self.mostrar_advertencia_maquinas:
            self.mostrar_mensaje_advertencia("No se encontraron máquinas en el sistema.")
            self.mostrar_advertencia_maquinas = False  # Desactivar la advertencia después de mostrarla

        # Reactivar la advertencia de entrenadores para el siguiente cambio
        self.mostrar_advertencia_entrenadores = True

        # Actualizar los tipos de gasto para máquinas
        self.actualizar_tipo_gasto_maquinas()

    def actualizar_combo_entrenadores(self):
        """Actualiza el ComboBox de entrenadores y muestra advertencia si está vacío."""
        # Ocultar el ComboBox de máquinas y mostrar el de entrenadores
        self.ui.combo_gasto_maquina.hide()
        self.ui.combo_gasto_entrenador.show()

        # Llenar el ComboBox de entrenadores
        self.llenar_combo_entrenadores_gastos()

        # Mostrar advertencia solo si el ComboBox de entrenadores está vacío y la advertencia no se ha mostrado
        if self.ui.combo_gasto_entrenador.count() == 0 and self.mostrar_advertencia_entrenadores:
            self.mostrar_mensaje_advertencia("No se encontraron entrenadores en el sistema.")
            self.mostrar_advertencia_entrenadores = False  # Desactivar la advertencia después de mostrarla

        # Reactivar la advertencia de máquinas para el siguiente cambio
        self.mostrar_advertencia_maquinas = True

        # Actualizar los tipos de gasto para entrenadores
        self.actualizar_tipo_gasto_entrenadores()

    # Función para mostrar el mensaje de advertencia
    def mostrar_mensaje_advertencia(self, texto):
        mensaje = qtw.QMessageBox(self.main_logic)
        mensaje.setWindowTitle("Advertencia")
        mensaje.setText(texto)
        mensaje.setIcon(qtw.QMessageBox.Warning)
        aplicar_estilo_mensaje(mensaje)
        mensaje.exec_()



    def actualizar_tipo_gasto_maquinas(self):
        """Actualiza los tipos de gasto para máquinas en el ComboBox de tipos de gasto."""
        self.ui.combo_tipo_gasto.clear()  # Limpiar el ComboBox antes de agregar nuevos valores
        tipos_gasto_maquinas = ["Mantenimiento", "Reparación", "Reemplazo de piezas", "Limpieza", "Instalación"]
        self.ui.combo_tipo_gasto.addItems(tipos_gasto_maquinas)

    def actualizar_tipo_gasto_entrenadores(self):
        """Actualiza los tipos de gasto para entrenadores en el ComboBox de tipos de gasto."""
        self.ui.combo_tipo_gasto.clear()  # Limpiar el ComboBox antes de agregar nuevos valores
        tipos_gasto_entrenadores = ["Salario", "Uniforme", "Viáticos", "Bonificaciones"]
        self.ui.combo_tipo_gasto.addItems(tipos_gasto_entrenadores)



    def llenar_campos_editar_gasto(self, tablerow):
        # Activar el modo de edición
        self.modo_edicion = True

        # Obtener el ID del gasto desde la primera columna de la tabla
        id_gasto = self.ui.tabla_gastos.item(tablerow, 0).text()

        # Cambiar a la página de edición
        self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_crear_gasto)

        try:
            with conexion.cursor() as cursor:
                # Consulta para obtener los datos del gasto que vamos a editar
                sql = """
                SELECT descripcion, monto, fecha, tipo_gasto, 
                (SELECT id_entrenador FROM entrenadores_gastos WHERE id_gasto = g.id) as id_entrenador, 
                (SELECT id_maquina FROM maquinas_gastos WHERE id_gasto = g.id) as id_maquina 
                FROM gastos g 
                WHERE g.id = %s
                """
                cursor.execute(sql, (id_gasto,))
                resultado = cursor.fetchone()

                if resultado:
                    descripcion, monto, fecha, tipo_gasto, id_entrenador, id_maquina = resultado

                    # Convertir la fecha a QDate utilizando sus componentes
                    fecha_qdate = date(fecha.year, fecha.month, fecha.day)

                    # Cargar los datos en el formulario de edición
                    self.ui.txt_descripcion_gasto.setText(descripcion)
                    self.ui.txt_monto_gasto.setText(str(monto))
                    self.ui.txt_fecha_gasto.setDate(fecha_qdate)
                    self.ui.combo_tipo_gasto.setCurrentText(tipo_gasto)

                    # Si es un gasto de entrenador, seleccionar el entrenador actual en el ComboBox
                    if id_entrenador:
                        self.ui.radio_gasto_entrenadores.setChecked(True)
                        self.llenar_combo_entrenadores_gastos()  # Llenar ComboBox con entrenadores
                        index = self.ui.combo_gasto_entrenador.findData(id_entrenador)
                        if index != -1:
                            self.ui.combo_gasto_entrenador.setCurrentIndex(index)
                        self.actualizar_tipo_gasto_entrenadores()  # Cargar tipos de gasto para entrenadores

                    # Si es un gasto de máquina, seleccionar la máquina actual en el ComboBox
                    elif id_maquina:
                        self.ui.radio_gasto_maquinas.setChecked(True)
                        self.llenar_combo_maquinas_gastos()  # Llenar ComboBox con máquinas
                        index = self.ui.combo_gasto_maquina.findData(id_maquina)
                        if index != -1:
                            self.ui.combo_gasto_maquina.setCurrentIndex(index)
                        self.actualizar_tipo_gasto_maquinas()  # Cargar tipos de gasto para máquinas

                    # Guardar el estado inicial de los campos de texto
                    self.main_logic.guardar_estado_inicial()

                    # Mostrar modo editar
                    self.main_logic.mostrar_modo_editar()

                    # Guardar el ID del gasto que estamos editando
                    self.gasto_id_actual = id_gasto

        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al cargar los datos del gasto, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()


    def editar_gasto(self):
        # Obtener los valores editados desde los campos
        fecha = self.ui.txt_fecha_gasto.date().toString('yyyy-MM-dd')
        descripcion = self.ui.txt_descripcion_gasto.toPlainText()
        monto = self.ui.txt_monto_gasto.text()
        tipo_gasto = self.ui.combo_tipo_gasto.currentText()


        # Obtener el nuevo entrenador o máquina
        if self.ui.radio_gasto_entrenadores.isChecked():
            id_entrenador = self.ui.combo_gasto_entrenador.currentData()  # Obtener el ID del entrenador
            id_maquina = None  # Ninguna máquina seleccionada
        elif self.ui.radio_gasto_maquinas.isChecked():
            id_maquina = self.ui.combo_gasto_maquina.currentData()  # Obtener el ID de la máquina
            id_entrenador = None  # Ningún entrenador seleccionado
        else:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setText("Debe seleccionar si el gasto es para una máquina o un entrenador.")
            mensaje.setIcon(qtw.QMessageBox.Warning)
            aplicar_estilo_mensaje(mensaje) 
            mensaje.exec_()
            return

        # Ejecutar la actualización en la base de datos
        try:
            with conexion.cursor() as cursor:
                # Actualizar los datos en la tabla gastos
                sql_gasto = """
                    UPDATE gastos
                    SET descripcion = %s, monto = %s, fecha = %s, tipo_gasto = %s
                    WHERE id = %s
                """
                cursor.execute(sql_gasto, (descripcion, monto, fecha, tipo_gasto, self.gasto_id_actual))

                # Actualizar la referencia en la tabla de relación correspondiente (entrenadores_gastos o maquinas_gastos)
                if id_entrenador:
                    sql_actualizar_relacion = """
                        UPDATE entrenadores_gastos
                        SET id_entrenador = %s
                        WHERE id_gasto = %s
                    """
                    cursor.execute(sql_actualizar_relacion, (id_entrenador, self.gasto_id_actual))
                elif id_maquina:
                    sql_actualizar_relacion = """
                        UPDATE maquinas_gastos
                        SET id_maquina = %s
                        WHERE id_gasto = %s
                    """
                    cursor.execute(sql_actualizar_relacion, (id_maquina, self.gasto_id_actual))

                # Confirmar los cambios
                conexion.commit()
                mensaje = qtw.QMessageBox(self.main_logic)
                mensaje.setText("El gasto ha sido actualizado correctamente.")
                mensaje.setIcon(qtw.QMessageBox.Information)
                aplicar_estilo_mensaje(mensaje) 
                mensaje.exec_()

                # Recargar los datos en la tabla 
                self.llenar_tabla_gastos()
                # Regresar a la vista de la tabla de gastos
                self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_gastos)

        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al actualizar el gasto, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()
            
    def activar_boton_gastos(self):
        self.main_logic.reset_button_styles(self.ui.bt_gastos)
        # Otra lógica específica para el botón de gastos