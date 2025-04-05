
# PyQt5 Core y Widgets

from functools import partial
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from CapaLogica.Utilidades import ampliar_imagen_utl, subir_foto
from CapaLogica.Validaciones import validar_campos_obligatorios
from CapaDatos.ConexionPyodbc import conexion
from CapaLogica.estado_maquina import DialogoEstado
from Recursos.Estilos import aplicar_estilo_mensaje
from CapaLogica.ampliar_imagen import ClickableLabel
from PyQt5 import QtWidgets as qtw
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore


class LogicaMaquinas:
    def __init__(self, ui, main_logic):
        """
        Constructor que inicializa la lógica de maquinas con acceso a la interfaz de usuario.
        """
        self.ui = ui  # Recibe la interfaz como argumento para acceder a los elementos de la UI
        self.main_logic = main_logic
        # Restaurar el estilo de los otros botones
        self.main_logic.reset_button_styles(except_button=self.ui.bt_maquinas)

        # Navegación a la página de máquinas
        self.ui.bt_maquinas.clicked.connect(self.pagina_maquinas)


        self.pixmap_actual = None

        self.foto_maquina = None
    
        #Conectar el botón a la función
        self.ui.bt_buscar_imagen_maquina.clicked.connect(lambda: subir_foto(self, self.ui.label_foto_maquina, 'maquina'))

        # Conectar la imagen al evento de clic para ampliar la imagen
        self.ui.label_foto_maquina.mousePressEvent = lambda event: ampliar_imagen_utl(self.pixmap_actual)

        # Configuración de botones para agregar y editar máquinas
        self.ui.bt_guardar_nueva_maquina.clicked.connect(self.crear_maquina)
        self.ui.bt_editar_maquina.clicked.connect(self.editar_maquina)

        # Botón para regresar de la página de máquinas con confirmación de salida
        self.ui.bt_regresar_maquina.clicked.connect(lambda: self.main_logic.confirmar_salida(self.ui.pagina_maquinas))



    def pagina_maquinas(self):
        # Cambiar a la página de 
        self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_maquinas)

        self.ui.bt_maquinas.setStyleSheet("""
            QPushButton {
                font: 14pt "Segoe UI";
                background-color: #000000; 
                border: 1px solid #000000;
                image: url(:/iconos_principal/iconos/maquina1.png);
                image-position: left center;
                color: white;
                padding-left: 30px;
                qproperty-iconSize: 24px 24px; 
                padding-left: 40px;
                color: #FF6704;
                text-align: left; 
            }
        """)

        
    
        self.ui.bt_agregar_maquina.clicked.connect(self.abrir_pantalla_crear_maquina)
        self.llenar_tabla_maquinas()
        self.ui.txt_fecha_ingreso_maquina.setDate(QDate.currentDate())

        # Ocultar boton y label de editar
        # Limpiar todos los campos
        self.ui.txt_nombre_maquina.clear()
        self.ui.txt_descripcion_maquina.clear()
        self.ui.txt_fecha_ingreso_maquina.setDate(QDate.currentDate())
        self.ui.combo_estado_maquina.setCurrentIndex(0)

        # Limpiar foto si hay alguna cargada
        self.ui.label_foto_maquina.clear()
        self.foto_maquina = None

        #!Método para manejar la acción de crear máquina
    def abrir_pantalla_crear_maquina(self):
        # Cambiar a modo de creación
        self.modo_edicion = False
 
        self.main_logic.mostrar_modo_crear()
        # Cambia a la pantalla de creación de cliente
        self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_crear_maquinas)
                #Guarda el estado inicial de los campos de texto
        self.main_logic.guardar_estado_inicial()


        # FUNCION PARA AGREGAR MÁQUINA A LA BASE DE DATOS
    def crear_maquina(self):

        # Validar campos obligatorios
        campos_obligatorios = [
            (self.ui.txt_nombre_maquina, "Nombre máquina"),
        ]

        # Usamos la función de validaciones
        if not validar_campos_obligatorios(campos_obligatorios, self.main_logic):
            return  # Detener la ejecución si hay campos vacíos

        # Datos de la tabla máquinas
        nombre = self.ui.txt_nombre_maquina.text()
        fecha_adquisicion = self.ui.txt_fecha_ingreso_maquina.text()
        estado = self.ui.combo_estado_maquina.currentText()
        descripcion = self.ui.txt_descripcion_maquina.toPlainText()

        foto = self.foto_maquina if hasattr(self, 'foto_maquina') and self.foto_maquina else None

        descripcion = self.ui.txt_descripcion_maquina.toPlainText().strip() if self.ui.txt_descripcion_maquina.toPlainText().strip() != "" else None


        try:
            with conexion.cursor() as cursor:
                # Insertar en la tabla máquinas
                if foto is not None:
                    # Asegurarnos de que la foto sea del tipo binario esperado (en caso de que sea un archivo)
                    sql = "INSERT INTO maquinas (foto, nombre, fecha_adquisicion, estado, descripcion) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(sql, (foto, nombre, fecha_adquisicion, estado, descripcion))
                else:
                    sql = "INSERT INTO maquinas (nombre, fecha_adquisicion, estado, descripcion) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql, (nombre, fecha_adquisicion, estado, descripcion))

            # Confirmar los cambios en la base de datos
            conexion.commit()

            self.main_logic.limpiar_campos()

            # Aplicar el estilo solo a este cuadro de mensaje
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Éxito")
            mensaje.setText("Datos almacenados correctamente")
            mensaje.setIcon(qtw.QMessageBox.Information)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()

            # Refresca la tabla de máquinas después de agregar una nueva
            self.llenar_tabla_maquinas()

        except Exception as ex:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al agregar la máquina, revise que la conexión a la base de datos esté disponible.")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()



    # FUNCION PARA VER DATOS EN LA TABLA MAQUINAS
    def llenar_tabla_maquinas(self):
        tabla = self.ui.tabla_maquinas
        self.ui.tabla_maquinas.verticalHeader().setVisible(False)

        try:
            with conexion.cursor() as cursor:
                # Se realiza la consulta a la base de datos 
                sql = "SELECT id, foto, nombre, fecha_adquisicion, estado, descripcion FROM maquinas"

                # Se ejecuta la consulta sql con el cursor y se obtienen todas las filas 
                cursor.execute(sql)
                maquinas = cursor.fetchall()

            # Validar la existencia de la tabla antes de configurar el número de filas
            if tabla is not None:
                # Medimos la cantidad de datos de la tabla        
                i = len(maquinas)
                tabla.setRowCount(i)
                
                 # Ocultamos la columna 0
                self.ui.tabla_maquinas.hideColumn(0)

                # Validamos si hay por lo menos un dato para que nos muestre los mismos en la tabla
                if i > 0:
                    tablerow = 0
                    for maquina in maquinas:
                        # Crear un QLabel para la foto del cliente
                        foto_label = ClickableLabel()
                        pixmap = None
                        if maquina[1] is not None:  # Usar el índice 1 para la foto
                            pixmap = QPixmap()
                            pixmap.loadFromData(maquina[1])
                            foto_label.setPixmap(pixmap)
                        else:
                            foto_label.setText("Sin foto")

                        # Añadir el QLabel a la tabla
                        tabla.setCellWidget(tablerow, 1, foto_label)


                        if pixmap is not None:
                            foto_label.clicked.connect(lambda pixmap=pixmap: ampliar_imagen_utl(pixmap))

                        # Crear un QTableWidgetItem para el nombre de la máquina
                        nombre_item = qtw.QTableWidgetItem(str(maquina[2]))

                        # Almacenar el ID de la máquina en el QTableWidgetItem del nombre usando setData
                        nombre_item.setData(QtCore.Qt.UserRole, maquina[0])  # Almacena el ID en el rol de usuario

                        # Añadir los elementos a la tabla
                        tabla.setItem(tablerow, 0, qtw.QTableWidgetItem(str(maquina[0]))) # Nombre
                        tabla.setItem(tablerow, 2, qtw.QTableWidgetItem(str(maquina[2]))) # Nombre
                        tabla.setItem(tablerow, 3, qtw.QTableWidgetItem(str(maquina[3])))  # Fecha adquisición
                        tabla.setItem(tablerow, 4, qtw.QTableWidgetItem(maquina[5] if maquina[5] is not None else "Sin Descripción"))  # Descripción

                        # Configurar la celda de estado y cambiar el color según el estado
                        estado_item = qtw.QTableWidgetItem(str(maquina[4]))

                        # Cambiar color según el estado de la máquina
                        estado_texto = maquina[4].lower()
                        if estado_texto == "en mantenimiento":
                            estado_item.setForeground(QtGui.QColor("orange"))  # Color naranja para "En Mantenimiento"
                            boton_estado = QPushButton()
                            boton_estado.setStyleSheet("""
                                QPushButton {
                                    image: url(:/iconos_principal/iconos/mantenimiento.png);
                                    width: 35px;
                                    height: 35px 
                                }""")


                        elif estado_texto == "fuera de servicio":
                            estado_item.setForeground(QtGui.QColor("red"))  # Color rojo para "Fuera de Servicio"
                            boton_estado = QPushButton()
                            boton_estado.setStyleSheet("""
                                QPushButton {
                                    image: url(:/iconos_principal/iconos/fuera_servicio.png);
                                    width: 35px;
                                    height: 35px 
                                }""")
                            
                        else:
                            estado_item.setForeground(QtGui.QColor("green"))  # Color verde para "Disponible"
                            boton_estado = QPushButton()
                            boton_estado.setStyleSheet("""
                                QPushButton {
                                    image: url(:/iconos_principal/iconos/funcionando.png);
                                    width: 35px;
                                    height: 35px 
                                }""")

                        # Asignar el item a la celda de la tabla
                        tabla.setItem(tablerow, 5, estado_item)
            
                        for col in range(2, 6):  
                            tabla.item(tablerow, col).setFlags(QtCore.Qt.ItemIsEnabled)

                        # Crear botón Editar y usar partial para pasar la fila correcta
                        boton_editar = QPushButton()
                        boton_editar.clicked.connect(partial(self.llenar_campos_editar_maquina, tablerow))
                        boton_editar.setStyleSheet("""
                            QPushButton {
                                image: url(:/iconos_principal/iconos/editar_tabla.png);
                                width: 35px;
                                height: 35px 
                            }""")
                        
                        # Crear botón Eliminar y usar partial
                        boton_eliminar = QPushButton()
                        boton_eliminar.clicked.connect(partial(self.eliminar_maquina, tablerow))
                        boton_eliminar.setStyleSheet("""
                            QPushButton {
                                image: url(:/iconos_principal/iconos/borrar_tabla.png);
                                width: 35px;
                                height: 35px 
                            }""")       
                                         
                        
                        boton_estado.clicked.connect(partial(self.editar_estado_maquina, tablerow))

                        
                        # Crear un layout horizontal para contener los botones
                        widget_opciones = QWidget()
                        layout_opciones = QHBoxLayout()
                        layout_opciones.addWidget(boton_editar)
                        layout_opciones.addWidget(boton_eliminar)
                        layout_opciones.addWidget(boton_estado)
                        layout_opciones.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes
                        widget_opciones.setLayout(layout_opciones)

                        # Insertar el widget con los botones en la columna "Opciones"
                        self.ui.tabla_maquinas.setCellWidget(tablerow, 6, widget_opciones)

                        tablerow += 1
                else:
                    mensaje = qtw.QMessageBox(self.main_logic)
                    mensaje.setText("No existen máquinas en el sistema.")
                    mensaje.setIcon(qtw.QMessageBox.Warning)
                    aplicar_estilo_mensaje(mensaje) 
                    mensaje.exec_()

        except Exception as ex:
            print(ex)




    def eliminar_maquina(self, tablerow):
        # Obtener el nombre de la máquina de la fila seleccionada
        id = self.ui.tabla_maquinas.item(tablerow, 0).text()
        nombre_maquina = self.ui.tabla_maquinas.item(tablerow, 2)  # Columna 2 es el nombre
        nombre_maquina = nombre_maquina.text()

        mensaje = QMessageBox(self.main_logic)
        mensaje.setIcon(QMessageBox.Question)
        mensaje.setWindowTitle("Eliminar Máquina")
        mensaje.setText(
            f"¿Estás seguro de que deseas eliminar la máquina '{nombre_maquina}'?\n\n"
            "Esta acción es irreversible y eliminará todos los datos relacionados con esta máquina en el sistema, "
            "incluyendo:\n"
            "- Gastos asociados a la máquina\n\n"
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

                # Realizar la consulta para eliminar la máquina de la base de datos
                with conexion.cursor() as cursor:
                    sql_eliminar = "DELETE FROM maquinas_gastos WHERE id_maquina = %s"
                    cursor.execute(sql_eliminar, (id,))

                    sql_eliminar = "DELETE FROM maquinas WHERE id = %s"
                    cursor.execute(sql_eliminar, (id,))
                    conexion.commit()

                mensaje = qtw.QMessageBox(self.main_logic)
                mensaje.setText(f"La máquina '{nombre_maquina}' ha sido eliminada correctamente.")
                mensaje.setIcon(qtw.QMessageBox.Information)
                aplicar_estilo_mensaje(mensaje) 
                mensaje.exec_()

                self.llenar_tabla_maquinas()

            except Exception as e:
                mensaje = qtw.QMessageBox(self.main_logic)
                mensaje.setWindowTitle("Error")
                mensaje.setText(f"Error al eliminar la máquina, revise que la conexión a la base de datos esté disponible")
                mensaje.setIcon(qtw.QMessageBox.Critical)
                aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
                mensaje.exec_()



    def editar_estado_maquina(self, tablerow):
        # Obtener datos de la tabla
        id_maquina = self.ui.tabla_maquinas.item(tablerow, 0).text() 
        nombre_maquina = self.ui.tabla_maquinas.item(tablerow, 2).text()

        # Crear lista de opciones
        opciones_estado = ["Disponible", "En Mantenimiento", "Fuera de Servicio"]

        # Crear y mostrar el diálogo personalizado
        dialogo = DialogoEstado(nombre_maquina, opciones_estado, self.main_logic)
        if dialogo.exec_() == qtw.QDialog.Accepted:
            estado_seleccionado = dialogo.obtener_estado_seleccionado()

            # Aquí puedes manejar el estado seleccionado y actualizar la base de datos
            if estado_seleccionado in opciones_estado:
                try:
                    with conexion.cursor() as cursor:
                        sql_cambiar_estado = "UPDATE maquinas SET estado = %s WHERE id = %s"
                        cursor.execute(sql_cambiar_estado, (estado_seleccionado, id_maquina))
                        conexion.commit()

                                   # Recargar la tabla para actualizarla
                    self.llenar_tabla_maquinas()

                    # Mostrar mensaje de éxito
                    mensaje = qtw.QMessageBox(self.main_logic)
                    mensaje.setWindowTitle("Éxito")
                    mensaje.setText(f"El estado de la máquina '{nombre_maquina}' ha sido actualizado a '{estado_seleccionado}' correctamente.")
                    mensaje.setIcon(qtw.QMessageBox.Information)
                    aplicar_estilo_mensaje(mensaje)  # Aplica estilo al mensaje
                    mensaje.exec_()

                except Exception as e:
                    mensaje = qtw.QMessageBox(self.main_logic)
                    mensaje.setWindowTitle("Error")
                    mensaje.setText(f"No se pudo actualizar el estado, revise que la conexión a la base de datos esté disponible")
                    mensaje.setIcon(qtw.QMessageBox.Critical)
                    aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
                    mensaje.exec_()



    def llenar_campos_editar_maquina(self, tablerow):

        # Activar el modo de edición
        self.modo_edicion = True


        # Cambiar a la página de crear/editar máquina
        self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_crear_maquinas)

        id_maquina = self.ui.tabla_maquinas.item(tablerow, 0).text()
        
        # Guardar el ID de la máquina para usarlo más tarde en la actualización
        self.maquina_id_actual = id_maquina

        # Obtener los demás datos desde la tabla
        nombre_actual = self.ui.tabla_maquinas.item(tablerow, 2).text()
        fecha_actual = self.ui.tabla_maquinas.item(tablerow, 3).text()
        estado_actual = self.ui.tabla_maquinas.item(tablerow, 4).text()
        descripcion_actual = self.ui.tabla_maquinas.item(tablerow, 5).text() if self.ui.tabla_maquinas.item(tablerow, 5) else "Sin Descripción"

        # Convertir la fecha de cadena a QDate
        formato_fecha = "yyyy-MM-dd"
        fecha_qdate = QDate.fromString(fecha_actual, formato_fecha)

        # Cargar los datos actuales en los campos de edición de la máquina
        self.ui.txt_nombre_maquina.setText(nombre_actual)
        self.ui.txt_fecha_ingreso_maquina.setDate(fecha_qdate) 
        self.ui.combo_estado_maquina.setCurrentText(estado_actual)
        self.ui.txt_descripcion_maquina.setPlainText(descripcion_actual)

        # Obtener la foto desde la tabla y cargarla en el QLabel
        foto_label = self.ui.tabla_maquinas.cellWidget(tablerow, 1)
        if isinstance(foto_label, ClickableLabel) and foto_label.pixmap() is not None:
            self.ui.label_foto_maquina.setPixmap(foto_label.pixmap().scaled(150, 150, Qt.KeepAspectRatio))
            self.pixmap_actual = foto_label.pixmap()
        else:
            # Limpiar el QLabel si no hay foto
            self.ui.label_foto_maquina.clear()
            self.pixmap_actual = None

        # Ocultar el botón de guardar una nueva máquina y mostrar el de editar
        self.ui.bt_guardar_nueva_maquina.setVisible(False)
        self.ui.bt_editar_maquina.setVisible(True)

        # Ocultar el label de crear y mostrar el label de editar
        self.ui.label_crear_maquina.setVisible(False)
        self.ui.label_editar_maquina.setVisible(True)

        #Guarda el estado inicial de los campos de texto
        self.main_logic.guardar_estado_inicial()

        #*mostrar modo editar
        self.main_logic.mostrar_modo_editar()


    def editar_maquina(self):

        # Validar campos obligatorios
        campos_obligatorios = [
            (self.ui.txt_nombre_maquina, "Nombre máquina"),
        ]

        # Usamos la función de validaciones
        if not validar_campos_obligatorios(campos_obligatorios, self.main_logic):
            return  # Detener la ejecución si hay campos vacíos

        # Obtener los valores editados desde los campos
        nombre_editado = self.ui.txt_nombre_maquina.text()
        fecha_editada = self.ui.txt_fecha_ingreso_maquina.text()
        estado_editado = self.ui.combo_estado_maquina.currentText()
   
        # Datos opcionales se mandan como null 
        foto = self.foto_maquina if hasattr(self, 'foto_maquina') and self.foto_maquina is not None else None
        descripcion_editado = self.ui.txt_descripcion_maquina.toPlainText().strip() if self.ui.txt_descripcion_maquina.toPlainText().strip() != "" else None


        try:
            with conexion.cursor() as cursor:
                if foto is not None:
                    sql = """
                        UPDATE maquinas
                        SET nombre = %s, fecha_adquisicion = %s, estado = %s, descripcion = %s, foto = %s
                        WHERE id = %s
                    """
                    cursor.execute(sql, (nombre_editado, fecha_editada, estado_editado, descripcion_editado, foto, self.maquina_id_actual))
                else:
                    sql = """
                        UPDATE maquinas
                        SET nombre = %s, fecha_adquisicion = %s, estado = %s, descripcion = %s
                        WHERE id = %s
                    """
                    cursor.execute(sql, (nombre_editado, fecha_editada, estado_editado, descripcion_editado, self.maquina_id_actual))
  
                conexion.commit()

                mensaje = qtw.QMessageBox(self.main_logic)
                mensaje.setText("La máquina ha sido actualizada correctamente.")
                mensaje.setIcon(qtw.QMessageBox.Information)
                aplicar_estilo_mensaje(mensaje) 
                mensaje.exec_()

                # Recargar la tabla para actualizarla
                self.llenar_tabla_maquinas()
                #Volver a la pagina anterior
                self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_maquinas)

                self.foto_maquina = None

        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al actualizar la máquina, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()
    
    def activar_boton_maquinas(self):
        self.main_logic.reset_button_styles(self.ui.bt_maquinas)
        # Otra lógica específica para el botón de máquinas
