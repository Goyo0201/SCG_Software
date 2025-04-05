
# PyQt5 Core y Widgets
from datetime import datetime, timedelta
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from CapaLogica.Validaciones import validar_campos_obligatorios
from CapaDatos.ConexionPyodbc import conexion
from Recursos.Estilos import aplicar_estilo_mensaje
from PyQt5 import QtWidgets as qtw


class LogicaHorarios:
    def __init__(self, ui, main_logic):
        """
        Constructor que inicializa la lógica de horarios con acceso a la interfaz de usuario.
        """
        self.ui = ui  # Recibe la interfaz como argumento para acceder a los elementos de la UI
        self.main_logic = main_logic

        # Restaurar el estilo de los otros botones
        self.main_logic.reset_button_styles(except_button=self.ui.bt_horarios)
        # Navegación a la página de horarios
        self.ui.bt_horarios.clicked.connect(self.pagina_horarios)

        # Configuración de botones para manejar horarios
        self.ui.bt_eliminar_horario.clicked.connect(self.eliminar_horario)
        self.ui.bt_guardar_horario.clicked.connect(self.crear_horario)
        self.ui.bt_guardar_horario_limpiar.clicked.connect(self.limpiar_horario)
        self.ui.bt_agregar_horario.clicked.connect(self.abrir_pantalla_crear_horario)
        self.ui.bt_regresar_horarios.clicked.connect(self.regresar_horario)


    def pagina_horarios(self):
        # Cambiar a la página de 
        self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_horarios)

        self.ui.bt_horarios.setStyleSheet("""
            QPushButton {
                font: 14pt "Segoe UI";
                background-color: #000000; 
                border: 1px solid #000000;
                image: url(:/iconos_principal/iconos/calendario (1).png);
                image-position: left center;
                color: white;
                padding-left: 30px;
                qproperty-iconSize: 24px 24px; 
                padding-left: 40px;
                color: #FF6704;
                text-align: left; 
            }
        """)

        self.ui.combo_buscar_horario_nombre.currentIndexChanged.connect(self.mostrar_horario_por_nombre)
        self.cargar_nombres_horarios()
        

    #!Método para manejar la acción de crear horario
    def abrir_pantalla_crear_horario(self):
        # Cambiar a modo de creación
        self.modo_edicion = False

        # Cambia a la pantalla de creación de cliente
        self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_crear_horario)
        #Guarda el estado inicial de los campos de texto
        self.main_logic.guardar_estado_inicial()
        self.llenar_combo_entrenador_horario()

        self.mostrar_horario_por_nombre()
        
        self.main_logic.limpiar_campos()

    def regresar_horario(self):
        
        self.cargar_nombres_horarios()
        # Obtener el texto del campo de nombre de horario
        nombre_horario = self.ui.txt_nombre_horario.text().strip()

        # Verificar si el campo de nombre de horario tiene contenido
        if nombre_horario:
        # Crear el cuadro de diálogo de confirmación
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setIcon(qtw.QMessageBox.Question)
            mensaje.setWindowTitle("Confirmación de salida")
            mensaje.setText(
                "Tiene cambios sin guardar en el horario. ¿Está seguro de que desea salir? El horario no se guardará."
            )

            # Añadir botones "Sí" y "No"
            boton_si = mensaje.addButton("Sí", qtw.QMessageBox.YesRole)
            boton_no = mensaje.addButton("No", qtw.QMessageBox.NoRole)

            # Aplicar el estilo del mensaje
            aplicar_estilo_mensaje(mensaje, agregar_boton_aceptar=False)

            # Mostrar el cuadro de diálogo y obtener la respuesta
            respuesta = mensaje.exec_()

            # Comprobar la respuesta
            if mensaje.clickedButton() == boton_si:
                try:
                    with conexion.cursor() as cursor:
                        # Obtener todos los IDs de horarios con el nombre especificado
                        obtener_ids_sql = "SELECT id FROM horarios WHERE nombre = %s"
                        cursor.execute(obtener_ids_sql, (nombre_horario,))
                        resultados = cursor.fetchall()

                        # Verificar que existen registros para el nombre dado
                        if resultados:
                            # Limpiar el buffer de resultados pendientes
                            cursor.fetchall()  # Esto asegura que no haya resultados sin leer

                            # Eliminar las relaciones en horarios_entrenadores para cada horario encontrado
                            for resultado in resultados:
                                id_horario = resultado[0]
                                eliminar_relacion_sql = "DELETE FROM horarios_entrenadores WHERE id_horario = %s"
                                cursor.execute(eliminar_relacion_sql, (id_horario,))
                                print(f"Relación eliminada para el horario con ID {id_horario} en horarios_entrenadores.")

                            # Luego, eliminar todos los horarios en la tabla horarios que coincidan con el nombre
                            eliminar_horarios_sql = "DELETE FROM horarios WHERE nombre = %s"
                            cursor.execute(eliminar_horarios_sql, (nombre_horario,))
                            print(f"Todos los horarios con nombre '{nombre_horario}' eliminados de la base de datos.")  # Mensaje de confirmación

                            # Confirmar cambios en la base de datos
                            conexion.commit()

                        else:
                            print(f"No se encontraron horarios con el nombre '{nombre_horario}' en la base de datos.")

                    # Limpiar los campos de entrada para evitar confusión
                    self.ui.txt_nombre_horario.clear()
                    self.ui.combo_entrenador_horario.setCurrentIndex(0)
                    self.ui.combo_hora_inicio.setCurrentIndex(0)
                    self.ui.combo_hora_fin.setCurrentIndex(0)
                    
                    
                    self.cargar_nombres_horarios()


                    # Cambiar a la página de horarios
                    self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_horarios)

                except Exception as ex:
                    mensaje = qtw.QMessageBox(self.main_logic)
                    mensaje.setWindowTitle("Error")
                    mensaje.setText(f"No se pudo eliminar el horario, revise que la conexión a la base de datos esté disponible")
                    mensaje.setIcon(qtw.QMessageBox.Critical)
                    aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
                    mensaje.exec_()
            else:
                # Si el usuario presiona "No", no hacemos nada y se queda en la página actual
                pass
        else:
            # Si el campo de nombre de horario está vacío, simplemente regresa a la página de horarios
            self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_horarios)


    def llenar_combo_entrenador_horario(self):
        try:
            with conexion.cursor() as cursor:
                # Obtener todos los clientes
                sql = "SELECT id, nombres, apellidos FROM entrenadores"
                cursor.execute(sql)
                entrenadores = cursor.fetchall()

                # Desactivar las señales mientras se llena el ComboBox
                self.ui.combo_entrenador_horario.blockSignals(True)

                if not entrenadores:
                    # Si no hay clientes, agregar "Sin datos" y mostrar un mensaje de advertencia
                    mensaje = qtw.QMessageBox(self.main_logic)
                    mensaje.setText("No se encontraron entrenadores en el sistema.")
                    mensaje.setIcon(qtw.QMessageBox.Warning)
                    aplicar_estilo_mensaje(mensaje)
                    mensaje.exec_()
                

                # Llenar el ComboBox con los nombres, apellidos e ID de los clientes
                self.ui.combo_entrenador_horario.clear()
                

                for entrenador in entrenadores:
                    id_entrenador = entrenador[0]
                    nombre = entrenador[1]
                    primer_apellido = entrenador[2].split()[0]  # Tomar solo el primer apellido

                    # Crear la cadena que incluye el nombre completo y la especialidad
                    texto_combo = f"{nombre} {primer_apellido}"

                    # Agregar al ComboBox el nombre, pero guardar el ID único
                    self.ui.combo_entrenador_horario.addItem(texto_combo, id_entrenador)
                    

                # Reactivar las señales después de llenar el ComboBox
                self.ui.combo_entrenador_horario.blockSignals(False)

        except Exception as ex:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"No se pudo cargar el listado de entrenadores, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()



    def crear_horario(self):
        
        # Validación de campos obligatorios
        campos_obligatorios = [
            (self.ui.txt_nombre_horario, "Nombre horario"),
        ]

        # Validación de campos
        if not validar_campos_obligatorios(campos_obligatorios, self.main_logic):
            return  # Detener la ejecución si hay campos vacíos

        nombre = self.ui.txt_nombre_horario.text().strip()  # Elimina espacios en blanco al inicio y al final
        id_entrenador = self.ui.combo_entrenador_horario.currentData()
        nombre_entrenador = self.ui.combo_entrenador_horario.currentText()
        hora_inicio = self.ui.combo_hora_inicio.currentText()
        hora_fin = self.ui.combo_hora_fin.currentText()

        # Crear una lista para almacenar los días seleccionados
        dias_seleccionados = []
        if self.ui.check_lunes.isChecked():
            dias_seleccionados.append('Lunes')
        if self.ui.check_martes.isChecked():
            dias_seleccionados.append('Martes')
        if self.ui.check_miercoles.isChecked():
            dias_seleccionados.append('Miércoles')
        if self.ui.check_jueves.isChecked():
            dias_seleccionados.append('Jueves')
        if self.ui.check_viernes.isChecked():
            dias_seleccionados.append('Viernes')
        if self.ui.check_sabado.isChecked():
            dias_seleccionados.append('Sábado')

        # Verificar que se ha seleccionado al menos un día
        if not dias_seleccionados:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setText("Seleccione al menos un día de la semana.")
            mensaje.setIcon(qtw.QMessageBox.Warning)
            aplicar_estilo_mensaje(mensaje) 
            mensaje.exec_()
            return

        try:
            with conexion.cursor() as cursor:
                hora_inicio_24 = datetime.strptime(hora_inicio, "%I:%M %p").strftime("%H:%M:%S")
                hora_fin_24 = datetime.strptime(hora_fin, "%I:%M %p").strftime("%H:%M:%S")

                # Registrar los IDs de horarios ya actualizados para evitar duplicaciones
                horarios_actualizados = []

                for dia_semana in dias_seleccionados:
                    verificar_sql = """
                        SELECT h.id FROM horarios h
                        WHERE h.nombre = %s AND h.dia_semana = %s AND h.hora_inicio = %s AND h.hora_fin = %s
                    """
                    cursor.execute(verificar_sql, (nombre, dia_semana, hora_inicio_24, hora_fin_24))
                    resultado = cursor.fetchone()


                    if resultado and resultado[0] not in horarios_actualizados:
                        
                         # Crear el cuadro de diálogo de confirmación
                        mensaje = qtw.QMessageBox(self.main_logic)
                        mensaje.setIcon(qtw.QMessageBox.Question)
                        mensaje.setWindowTitle("Confirmación de salida")
                        mensaje.setText(f"Ya existe un horario para el nombre '{nombre}' el {dia_semana} de {hora_inicio} a {hora_fin}. ¿Desea actualizarlo?")

                        # Añadir botones "Sí" y "No"
                        boton_si = mensaje.addButton("Sí", qtw.QMessageBox.YesRole)
                        boton_no = mensaje.addButton("No", qtw.QMessageBox.NoRole)

                        # Aplicar el estilo del mensaje
                        aplicar_estilo_mensaje(mensaje, agregar_boton_aceptar=False)

                        # Mostrar el cuadro de diálogo y obtener la respuesta
                        respuesta = mensaje.exec_()

                        # Comprobar la respuesta
                        if mensaje.clickedButton() == boton_si:

                            actualizar_sql = """
                                UPDATE horarios
                                SET dia_semana = %s, hora_inicio = %s, hora_fin = %s
                                WHERE id = %s
                            """
                            cursor.execute(actualizar_sql, (dia_semana, hora_inicio_24, hora_fin_24, resultado[0]))
                            horarios_actualizados.append(resultado[0])

                            relacion_sql = """
                                UPDATE horarios_entrenadores
                                SET id_entrenador = %s
                                WHERE id_horario = %s
                            """
                            cursor.execute(relacion_sql, (id_entrenador, resultado[0]))
                    else:
                        # Insertar un nuevo horario si no existe uno igual
                        insertar_sql = """
                            INSERT INTO horarios (nombre, dia_semana, hora_inicio, hora_fin)
                            VALUES (%s, %s, %s, %s)
                        """
                        cursor.execute(insertar_sql, (nombre, dia_semana, hora_inicio_24, hora_fin_24))
                        id_horario = cursor.lastrowid

                        relacion_sql = """
                            INSERT INTO horarios_entrenadores (id_entrenador, id_horario)
                            VALUES (%s, %s)
                        """
                        cursor.execute(relacion_sql, (id_entrenador, id_horario))

                conexion.commit()
                self.actualizar_tabla_crear_horarios(nombre_entrenador, dias_seleccionados, hora_inicio, hora_fin)

        except Exception as ex:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Fallo al almacenar los datos, revise que la conexión a la base de datos esté disponible.")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            mensaje.exec_()



    def limpiar_horario(self):
        
        # Verificar que el campo de nombre de horario esté lleno
        nombre_horario = self.ui.txt_nombre_horario.text().strip()
        
        # Verificar que al menos un día esté seleccionado
        algun_dia_seleccionado = (
            self.ui.check_lunes.isChecked() or
            self.ui.check_martes.isChecked() or
            self.ui.check_miercoles.isChecked() or
            self.ui.check_jueves.isChecked() or
            self.ui.check_viernes.isChecked() or
            self.ui.check_sabado.isChecked()
        )
        
        # Verificar que la tabla de horarios tenga al menos una celda con datos
        filas_en_tabla = self.ui.tabla_crear_horario.rowCount()
        tabla_con_datos = False
        for row in range(filas_en_tabla):
            for col in range(self.ui.tabla_crear_horario.columnCount()):
                item = self.ui.tabla_crear_horario.item(row, col)
                if item and item.text().strip():  # Verificar si la celda tiene texto
                    tabla_con_datos = True
                    break
            if tabla_con_datos:
                break

        # Validación: Mostrar advertencia si alguna de las condiciones no se cumple
        if not (nombre_horario and algun_dia_seleccionado and tabla_con_datos):
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Advertencia")
            mensaje.setText("No hay horarios que guardar")
            mensaje.setIcon(qtw.QMessageBox.Warning)
            aplicar_estilo_mensaje(mensaje)
            mensaje.exec_()
            return  # Detener la ejecución de la función si las condiciones no se cumplen

        # Si todas las condiciones se cumplen, procede con la limpieza
        # Limpiar el campo de texto de nombre de horario
        self.ui.txt_nombre_horario.clear()

        # Resetear el combo de entrenadores al primer índice
        self.ui.combo_entrenador_horario.setCurrentIndex(0)

        # Resetear los combos de hora de inicio y fin al primer índice
        self.ui.combo_hora_inicio.setCurrentIndex(0)
        self.ui.combo_hora_fin.setCurrentIndex(0)

        # Desmarcar todos los checkboxes de los días de la semana
        self.ui.check_lunes.setChecked(False)
        self.ui.check_martes.setChecked(False)
        self.ui.check_miercoles.setChecked(False)
        self.ui.check_jueves.setChecked(False)
        self.ui.check_viernes.setChecked(False)
        self.ui.check_sabado.setChecked(False)

        # Limpiar la tabla de horarios
        self.ui.tabla_crear_horario.clearContents()

        # Mostrar mensaje de confirmación de limpieza
        mensaje = qtw.QMessageBox(self.main_logic)
        mensaje.setWindowTitle("Éxito")
        mensaje.setText("El horario ha sido guardado correctamente.")
        mensaje.setIcon(qtw.QMessageBox.Information)
        aplicar_estilo_mensaje(mensaje)
        mensaje.exec_()


    
    def actualizar_tabla_crear_horarios(self, nombre_entrenador, dias_seleccionados, hora_inicio, hora_fin):
        # Definir la lista de días en el mismo orden que las columnas de la tabla
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
        horarios_dia = [
            "5:00 am - 6:00 am", "6:00 am - 7:00 am", "7:00 am - 8:00 am",
            "8:00 am - 9:00 am", "9:00 am - 10:00 am", "10:00 am - 11:00 am",
            "11:00 am - 12:00 pm", "3:00 pm - 4:00 pm", "4:00 pm - 5:00 pm", 
            "5:00 pm - 6:00 pm", "6:00 pm - 7:00 pm", "8:00 pm - 9:00 pm"
        ]

        # Convertir las horas de inicio y fin a objetos datetime para comparar
        hora_inicio_dt = datetime.strptime(hora_inicio, "%I:%M %p")
        hora_fin_dt = datetime.strptime(hora_fin, "%I:%M %p")

        # Iterar sobre cada fila de horarios_dia para encontrar el rango de tiempo adecuado
        for row, horario_intervalo in enumerate(horarios_dia):
            # Extraer la hora de inicio y fin del intervalo de la fila
            intervalo_inicio_str, intervalo_fin_str = horario_intervalo.split(" - ")
            intervalo_inicio_dt = datetime.strptime(intervalo_inicio_str, "%I:%M %p")
            intervalo_fin_dt = datetime.strptime(intervalo_fin_str, "%I:%M %p")

            # Verificar si el intervalo de la fila está dentro del rango seleccionado
            if intervalo_inicio_dt >= hora_inicio_dt and intervalo_fin_dt <= hora_fin_dt:
                # Marcar las celdas para cada día seleccionado
                for dia in dias_seleccionados:
                    if dia in dias_semana:
                        col = dias_semana.index(dia)   # +1 porque la primera columna es de horas
                        item = QTableWidgetItem(nombre_entrenador)
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tabla_crear_horario.setItem(row, col, item)


    #muestra el nombre de los horarios en el combobox
    def cargar_nombres_horarios(self):
        try:
            with conexion.cursor() as cursor:
                sql = "SELECT DISTINCT nombre FROM horarios"
                cursor.execute(sql)
                horarios = cursor.fetchall()
                
                # Limpiar el ComboBox antes de llenarlo
                self.ui.combo_buscar_horario_nombre.clear()
                
                # Llenar el ComboBox con los nombres de horarios
                for horario in horarios:
                    self.ui.combo_buscar_horario_nombre.addItem(horario[0])
                            # Verificar si el ComboBox está vacío después de cargar datos

                if self.ui.combo_buscar_horario_nombre.count() == 0:
                    mensaje = qtw.QMessageBox(self.main_logic)
                    mensaje.setWindowTitle("Advertencia")
                    mensaje.setText("No existen horarios en el sistema.")
                    mensaje.setIcon(qtw.QMessageBox.Warning)
                    aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
                    mensaje.exec_()
        
        except Exception as ex:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"No se pudo cargar los horarios, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()


    def mostrar_horario_por_nombre(self):
        nombre_horario = self.ui.combo_buscar_horario_nombre.currentText()
        if not nombre_horario:  # Verifica que haya un horario seleccionado
            return

        try:
            # Ejecuta la consulta para obtener los datos del horario y entrenadores
            with conexion.cursor() as cursor:
                sql = """
                    SELECT h.dia_semana, h.hora_inicio, h.hora_fin, e.nombres, e.apellidos
                    FROM horarios h
                    JOIN horarios_entrenadores he ON h.id = he.id_horario
                    JOIN entrenadores e ON he.id_entrenador = e.id
                    WHERE h.nombre = %s
                """
                cursor.execute(sql, (nombre_horario,))
                resultados = cursor.fetchall()
                
                # Limpiar la tabla antes de llenarla con nuevos datos
                self.ui.tabla_horarios.clearContents()

                # Define los días de la semana y los intervalos horarios que usaremos para indexar filas y columnas en la tabla
                dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
                horarios_dia = [
                    "5:00 am - 6:00 am", "6:00 am - 7:00 am", "7:00 am - 8:00 am",
                    "8:00 am - 9:00 am", "9:00 am - 10:00 am", "10:00 am - 11:00 am",
                    "11:00 am - 12:00 pm", "3:00 pm - 4:00 pm", "4:00 pm - 5:00 pm", 
                    "5:00 pm - 6:00 pm", "6:00 pm - 7:00 pm", "8:00 pm - 9:00 pm"
                ]

                # Procesa cada resultado y lo ubica en la tabla en todas las celdas del rango de tiempo
                for dia_semana, hora_inicio, hora_fin, nombre, apellido in resultados:
                    hora_actual = (datetime.min + hora_inicio).time()
                    hora_fin_dt = (datetime.min + hora_fin).time()
                    
                    # Inserta el nombre en cada intervalo de tiempo dentro del rango
                    while hora_actual < hora_fin_dt:
                        hora_siguiente = (datetime.combine(datetime.min, hora_actual) + timedelta(hours=1)).time()
                        intervalo_horario = f"{hora_actual.strftime('%I:%M %p').lstrip('0').lower()} - {hora_siguiente.strftime('%I:%M %p').lstrip('0').lower()}"

                        # Buscar el índice de columna (día de la semana) y de fila (intervalo horario) en la tabla
                        if dia_semana in dias_semana and intervalo_horario in horarios_dia:
                            col = dias_semana.index(dia_semana)
                            row = horarios_dia.index(intervalo_horario)
                            
                            # Crea un ítem con el nombre completo del entrenador y lo agrega a la tabla
                            item = QTableWidgetItem(f"{nombre} {apellido}")
                            item.setTextAlignment(Qt.AlignCenter)
                            self.ui.tabla_horarios.setItem(row, col, item)
                        
                        # Avanza al siguiente intervalo de 1 hora
                        hora_actual = hora_siguiente

        except Exception as ex:
            # Muestra un mensaje de error si ocurre una excepción al cargar los datos
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"No se pudo cargar los entrenadores, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()


    # FUNCION ELIMINAR HORARIO
    def eliminar_horario(self):
        nombre_horario = self.ui.combo_buscar_horario_nombre.currentText()
        if not nombre_horario:
            return

        mensaje = qtw.QMessageBox(self.main_logic)
        mensaje.setIcon(qtw.QMessageBox.Question)
        mensaje.setWindowTitle("Confirmar eliminación")
        mensaje.setText(
            f"¿Está seguro de que desea eliminar el horario '{nombre_horario}'?"
        )

        # Añadir botones "Sí" y "No"
        boton_si = mensaje.addButton("Sí", qtw.QMessageBox.YesRole)
        boton_no = mensaje.addButton("No", qtw.QMessageBox.NoRole)

        # Aplicar el estilo del mensaje
        aplicar_estilo_mensaje(mensaje, agregar_boton_aceptar=False)

        # Mostrar el cuadro de diálogo y obtener la respuesta
        respuesta = mensaje.exec_()

        # Comprobar la respuesta
        if mensaje.clickedButton() == boton_si:
            try:
                with conexion.cursor() as cursor:
                    # Eliminar relaciones en la tabla de horarios_entrenadores
                    delete_relacion_sql = """
                        DELETE he FROM horarios_entrenadores he
                        JOIN horarios h ON he.id_horario = h.id
                        WHERE h.nombre = %s
                    """
                    cursor.execute(delete_relacion_sql, (nombre_horario,))

                    # Eliminar el horario de la tabla de horarios
                    delete_horario_sql = "DELETE FROM horarios WHERE nombre = %s"
                    cursor.execute(delete_horario_sql, (nombre_horario,))

                    # Confirmar los cambios en la base de datos
                    conexion.commit()

                    # Actualizar el ComboBox y la tabla después de la eliminación
                    self.cargar_nombres_horarios()
                    self.ui.tabla_horarios.clearContents()

                    # Mostrar mensaje de éxito
                    mensaje = qtw.QMessageBox(self.main_logic)
                    mensaje.setText("Horario eliminado correctamente.")
                    mensaje.setIcon(qtw.QMessageBox.Information)
                    aplicar_estilo_mensaje(mensaje) 
                    mensaje.exec_()

            except Exception as ex:
                mensaje = qtw.QMessageBox(self.main_logic)
                mensaje.setWindowTitle("Error")
                mensaje.setText(f"Fallo al eliminar el horario, revise que la conexión a la base de datos esté disponible")
                mensaje.setIcon(qtw.QMessageBox.Critical)
                aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
                mensaje.exec_()

    def activar_boton_horarios(self):
        self.main_logic.reset_button_styles(self.ui.bt_horarios)
        # Otra lógica específica para el botón de horarios
