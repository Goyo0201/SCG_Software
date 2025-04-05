
# PyQt5 Core y Widgets
from datetime import datetime
from functools import partial
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from CapaLogica.Utilidades import ampliar_imagen_utl, calcular_imc, limpiar_entrada, mover_cursor_inicio, subir_foto
from CapaLogica.Validaciones import validar_campos_obligatorios, validar_correo, validar_fecha_nacimiento
from CapaDatos.ConexionPyodbc import conexion
from Recursos.Estilos import aplicar_estilo_mensaje  # Importar la conexión de la base de datos
from CapaLogica.ampliar_imagen import ClickableLabel
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from CapaLogica.logica_camara import LogicaCamara



class LogicaUsuarios:
    def __init__(self, ui, main_logic):
        """
        Constructor que inicializa la lógica de usuarios con acceso a la interfaz de usuario.
        """
        
        self.ui = ui  # Recibe la interfaz como argumento para acceder a los elementos de la UI
        self.main_logic = main_logic  # Guardamos referencia de LogicaMenuPrincipal
        self.configurar_campos()
        self.botones()
        # Restaurar el estilo de los otros botones
        self.main_logic.reset_button_styles(except_button=self.ui.bt_usuarios)
        self.foto_cliente = None  # Esta línea puedes moverla a LogicaUsuarios si es necesario
        self.pixmap_actual = None

        # Configuración de la lógica de la cámara
        self.logica_camara = LogicaCamara(self.ui)

        # Conexión del botón para abrir la cámara
        self.ui.bt_camara.clicked.connect(self.logica_camara.abrir_camara)


    def configurar_campos(self):
        # Conectar cada campo al método limpiar_entrada
        self.ui.txt_cedula_cliente.textChanged.connect(lambda: limpiar_entrada(self.ui.txt_cedula_cliente))
        self.ui.txt_telefono_cliente.textChanged.connect(lambda: limpiar_entrada(self.ui.txt_telefono_cliente))
        self.ui.txt_cedula_entrenador.textChanged.connect(lambda: limpiar_entrada(self.ui.txt_cedula_entrenador))
        self.ui.txt_telefono_entrenador.textChanged.connect(lambda: limpiar_entrada(self.ui.txt_telefono_entrenador))
        self.ui.txt_precio_membresia.textChanged.connect(lambda: limpiar_entrada(self.ui.txt_precio_membresia))
        self.ui.txt_monto_gasto.textChanged.connect(lambda: limpiar_entrada(self.ui.txt_monto_gasto))
        self.ui.txt_peso.textChanged.connect(lambda: limpiar_entrada(self.ui.txt_peso))
        self.ui.txt_altura.textChanged.connect(lambda: limpiar_entrada(self.ui.txt_altura))
        self.ui.txt_indice_masa.textChanged.connect(lambda: limpiar_entrada(self.ui.txt_indice_masa))
        self.ui.txt_medida_pecho.textChanged.connect(lambda: limpiar_entrada(self.ui.txt_medida_pecho))
        self.ui.txt_medida_brazos.textChanged.connect(lambda: limpiar_entrada(self.ui.txt_medida_brazos))
        self.ui.txt_medida_muslos.textChanged.connect(lambda: limpiar_entrada(self.ui.txt_medida_muslos))
        self.ui.txt_medida_gluteos.textChanged.connect(lambda: limpiar_entrada(self.ui.txt_medida_gluteos))
        self.ui.txt_medida_pantorrillas.textChanged.connect(lambda: limpiar_entrada(self.ui.txt_medida_pantorrillas))
        self.ui.txt_medida_hombros.textChanged.connect(lambda: limpiar_entrada(self.ui.txt_medida_hombros))

        # Conexión de edición de campos de correo y dirección para mover el cursor al inicio
        self.ui.txt_correo_cliente.editingFinished.connect(lambda: mover_cursor_inicio(self.ui.txt_correo_cliente))
        self.ui.txt_direccion_cliente.editingFinished.connect(lambda: mover_cursor_inicio(self.ui.txt_direccion_cliente))
        self.ui.txt_correo_entrenador.editingFinished.connect(lambda: mover_cursor_inicio(self.ui.txt_correo_entrenador))
        self.ui.txt_direccion_entrenador.editingFinished.connect(lambda: mover_cursor_inicio(self.ui.txt_direccion_entrenador))

        # Conexión de los campos de peso y altura a la función de IMC en LogicaUsuarios
        self.ui.txt_peso.textChanged.connect(lambda: calcular_imc(self))
        self.ui.txt_altura.textChanged.connect(lambda: calcular_imc(self))

        # Ampliación de imagen en el perfil del cliente, manejado en LogicaUsuarios
        self.ui.label_foto_cliente.mousePressEvent = lambda event: ampliar_imagen_utl(self, self.pixmap_actual)


    def botones(self):
        # Botones de guardado y asignación para clientes y entrenadores
        self.ui.bt_guardar_nuevo_cliente.clicked.connect(self.crear_cliente)
        self.ui.bt_guardar_asignar.clicked.connect(self.asignar_cliente_entrenador)
        self.ui.bt_guardar_nuevo_entrenador.clicked.connect(self.crear_entrenador)

        # Navegación a diferentes páginas
        self.ui.bt_usuarios.clicked.connect(self.pagina_usuarios)
        self.ui.bt_asignar_entrenador_cliente.clicked.connect(self.pagina_asignaciones)

       # Guardado y edición de cliente y entrenador
        self.ui.bt_editar_cliente.clicked.connect(self.editar_cliente)
        self.ui.bt_editar_entrenador.clicked.connect(self.editar_entrenador)

        self.ui.bt_clientes.clicked.connect(self.ir_a_pagina_clientes)
        self.ui.bt_entrenadores.clicked.connect(self.ir_a_pagina_entrenadores)

        # Botones de regreso
        self.ui.bt_regresar_clientes.clicked.connect(lambda: self.main_logic.confirmar_salida(self.ui.pagina_clientes))
        self.ui.bt_regresar_entrenadores.clicked.connect(lambda: self.main_logic.confirmar_salida(self.ui.pagina_entrenadores))
      

        self.pixmap_actual = None
        #Conectar el botón a la función
        self.ui.bt_buscar_imagen.clicked.connect(lambda: subir_foto(self, self.ui.label_foto_cliente, 'cliente'))
        # Conectar la imagen al evento de clic para ampliar la imagen
        self.ui.label_foto_cliente.mousePressEvent = lambda event: ampliar_imagen_utl(self.pixmap_actual)

        # Cambio de estado en el ComboBox, gestionado en LogicaUsuarios
        self.ui.combo_buscar_estado_cliente.currentIndexChanged.connect(self.cargar_consulta_clientes_estado)

        # Cambio de selección en ComboBox
        self.ui.combo_buscar_membresia_cliente.currentIndexChanged.connect(self.cliente_seleccionado_membresia)

        

    # Página de usuarios y entrenadores
    def pagina_usuarios(self):
        # Cambiar a la página de 
        self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_usuarios)

        # Aplicar estilo activo (mantiene el estilo como si estuviera presionado)
        self.ui.bt_usuarios.setStyleSheet("""
            QPushButton {
                font: 14pt "Segoe UI";
                background-color: #000000; 
                border: 1px solid #000000;
                image: url(:/iconos_principal/iconos/usuarios.png);
                image-position: left center;
                color: white;
                padding-left: 30px;
                qproperty-iconSize: 24px 24px; 
                padding-left: 40px;
                color: #FF6704;
                text-align: left; 
            }
        """)
        

        # Botones para clientes
        
        self.ui.bt_crear_cliente.clicked.connect((self.abrir_pantalla_crear_cliente))
        
        self.ui.bt_regresar_clientes_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_clientes))
        self.ui.bt_regresar_clientes_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_clientes))
        self.ui.bt_regresar_cl_usuarios.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_usuarios))
        self.ui.txt_fecha_registro_cliente.setDate(QDate.currentDate())

        self.ui.bt_buscar_cliente.clicked.connect(self.pagina_buscar_cliente)


        # Botones para entrenadores
       
        self.ui.bt_crear_entrenador.clicked.connect((self.abrir_pantalla_crear_entrenador))
        
        self.ui.bt_regresar_en_usuarios.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_usuarios))
        self.ui.txt_fecha_contrato_entrenador.setDate(QDate.currentDate())


    #!página con tabla y acciones crear ver y asignar
    def ir_a_pagina_clientes(self):

        # Cambiar la página activa al formulario de clientes
        self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_clientes)
        self.llenar_tabla_clientes()
    
    #!Método para manejar la acción de "Crear Cliente" (al dar clic a crear)
    def abrir_pantalla_crear_cliente(self):
        # Cambiar a modo de creación
        self.modo_edicion = False

        # Llama al método que configura el modo de creación
        self.main_logic.mostrar_modo_crear()
        # Cambia a la pantalla de creación de cliente
        self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_crear_cliente)
    
        #Guarda el estado inicial de los campos de texto
        self.main_logic.guardar_estado_inicial()


    # Esta función agrega un cliente nuevo
    def crear_cliente(self):
    
        # Validación de campos obligatorios
        campos_obligatorios = [
            (self.ui.txt_cedula_cliente, "Número de cédula"),
            (self.ui.txt_nombres_cliente, "Nombres"),
            (self.ui.txt_apellido_cliente, "Apellidos"),
            (self.ui.txt_telefono_cliente, "Teléfono"),
        ]

        # usamos la funcion de validaciones
        if not validar_campos_obligatorios(campos_obligatorios, self.main_logic):
            return  # Detener la ejecución si hay campos vacíos

        # Tabla cliente
        numero_cedula = int(self.ui.txt_cedula_cliente.text())
        nombres = self.ui.txt_nombres_cliente.text()
        apellidos = self.ui.txt_apellido_cliente.text()
        direccion = self.ui.txt_direccion_cliente.text()
        num_telefono = int(self.ui.txt_telefono_cliente.text())
        fecha_registro = self.ui.txt_fecha_registro_cliente.text()
        estado = self.ui.combo_estado_cliente.currentText()
        
        # Validar fecha de nacimiento
        fecha_nacimiento = self.ui.txt_fecha_nacimiento_cliente.text()
        if not validar_fecha_nacimiento(fecha_nacimiento, self.main_logic):
            return

        # Validar correo electrónico
        correo = self.ui.txt_correo_cliente.text()
        if not validar_correo(correo, self.main_logic):
            return
        
        # Datos opcionales
        binary_foto = self.logica_camara.foto_cliente if self.logica_camara.foto_cliente is not None else self.foto_cliente

        peso_corporal = self.ui.txt_peso.text() if self.ui.txt_peso.text() != "" else None
        altura = self.ui.txt_altura.text() if self.ui.txt_altura.text() != "" else None
        # Calcula el IMC en base al peso y la altura y lo guarda con el formato adecuado
        imc = float(calcular_imc(self)) if calcular_imc(self) is not None else None
        perimetro_pecho = self.ui.txt_medida_pecho.text() if self.ui.txt_medida_pecho.text() != "" else None
        perimetro_brazos = self.ui.txt_medida_brazos.text() if self.ui.txt_medida_brazos.text() != "" else None
        perimetro_muslos = self.ui.txt_medida_muslos.text() if self.ui.txt_medida_muslos.text() != "" else None
        perimetro_gluteos = self.ui.txt_medida_gluteos.text() if self.ui.txt_medida_gluteos.text() != "" else None
        perimetro_pantorrillas = self.ui.txt_medida_pantorrillas.text() if self.ui.txt_medida_pantorrillas.text() != "" else None
        perimetro_hombros = self.ui.txt_medida_hombros.text() if self.ui.txt_medida_hombros.text() != "" else None

        try:
            with conexion.cursor() as cursor:
                # Insertar en la tabla cliente
                if binary_foto is not None:
                    sql = "INSERT INTO clientes (num_cedula, nombres, apellidos, fecha_nacimiento, direccion, telefono, correo, fecha_registro, estado, foto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (numero_cedula, nombres, apellidos, fecha_nacimiento, direccion, num_telefono, correo, fecha_registro, estado, binary_foto))
                else:
                    sql = "INSERT INTO clientes (num_cedula, nombres, apellidos, fecha_nacimiento, direccion, telefono, correo, fecha_registro, estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (numero_cedula, nombres, apellidos, fecha_nacimiento, direccion, num_telefono, correo, fecha_registro, estado))

                cliente_id = cursor.lastrowid  # Guardamos el id del cliente recién insertado

                # Verificar si al menos una medida antropométrica tiene valor antes de insertar
                if any([peso_corporal, altura, imc, perimetro_pecho, perimetro_brazos, perimetro_muslos, perimetro_gluteos, perimetro_pantorrillas, perimetro_hombros]):
                    sql = """INSERT INTO medidas_antropometricas (peso_corporal, altura, imc, perimetro_pecho, perimetro_brazos, perimetro_muslos, 
                            perimetro_gluteos, perimetro_pantorrillas, perimetro_hombros, id_cliente) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    cursor.execute(sql, (peso_corporal, altura, imc, perimetro_pecho, perimetro_brazos, perimetro_muslos, perimetro_gluteos, perimetro_pantorrillas, perimetro_hombros, cliente_id))

            # Confirmar los cambios en la base de datos
            conexion.commit()
            self.logica_camara.foto_cliente = None  # Restablecer la foto tomada con la cámara


            self.main_logic.limpiar_campos()                       

            # Aplicar el estilo solo a este cuadro de mensaje
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Éxito")
            mensaje.setText("El nuevo cliente se ha creado correctamente")
            mensaje.setIcon(qtw.QMessageBox.Information)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()

            self.llenar_tabla_clientes()
            
            print("Creación exitosa, retornando True")
            return True  

        except Exception as ex:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Fallo al almacenar los datos, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()

            return False  # Retorna False si hubo un problema


    def llenar_tabla_clientes(self):  
        tabla = self.ui.tabla_clientes  # Asegúrate de que este sea el nombre correcto de tu tabla
        # Ocultar la barra de números (índice de fila) en la tabla
        self.ui.tabla_clientes.verticalHeader().setVisible(False)

        try:
            with conexion.cursor() as cursor:
                # Se realiza la consulta a la base de datos (mostrar todos los clientes incluso aquellos que no tienen un pago asociado LEFT JOIN)
                sql = """SELECT clientes.id, clientes.foto, clientes.nombres, clientes.apellidos, clientes.telefono, clientes.correo, 
                pagos.fecha_fin, pagos.membresia, clientes.estado FROM clientes LEFT JOIN pagos ON clientes.id = pagos.id_cliente"""

                # Se ejecuta la consulta sql con el cursor y se obtienen todas las filas 
                cursor.execute(sql)
                clientes_membresia = cursor.fetchall()
            
            # Ocultamos la columna 0
            self.ui.tabla_clientes.hideColumn(0)
            self.ui.tabla_clientes.hideColumn(6)

            # Validar la existencia de la tabla antes de configurar el número de filas
            if tabla is not None:
                # Medimos la cantidad de datos de la tabla        
                i = len(clientes_membresia)
                tabla.setRowCount(i)

                # Validamos si hay por lo menos un dato para que nos muestre los mismos en la tabla
                if i > 0:
                    tablerow = 0
                    for cliente in clientes_membresia:
                        try:
                            # Crear un QLabel para la foto del cliente
                            foto_label = ClickableLabel()
                            pixmap = None
                            if cliente[1] is not None:
                                pixmap = QPixmap()
                                pixmap.loadFromData(cliente[1])
                                foto_label.setPixmap(pixmap)
                            else:
                                foto_label.setText("Sin foto")

                            # Añadir el QLabel a la tabla
                            tabla.setCellWidget(tablerow, 1, foto_label)

                            # Conectar el evento de clic a la función ampliar_imagen si hay pixmap disponible
                            if pixmap is not None:
                                foto_label.clicked.connect(lambda pixmap=pixmap: ampliar_imagen_utl(pixmap))

                                

                            fecha_fin = str(cliente[6]) if cliente[6] is not None else ""

                            # Cálculo de días restantes solo si hay fecha
                            if fecha_fin:
                                hoy = datetime.now().date()
                                fecha_fin_date = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
                                dias_restantes = (fecha_fin_date - hoy).days if fecha_fin_date >= hoy else 0
                            else:
                                dias_restantes = "N/A"

                            # Añadir los elementos a la tabla en una sola línea
                            tabla.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(cliente[0])))
                            tabla.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(cliente[2])))
                            tabla.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(cliente[3])))
                            tabla.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(cliente[4])))
                            tabla.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(cliente[5])))
                            tabla.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(cliente[6])))
                            tabla.setItem(tablerow, 7, QtWidgets.QTableWidgetItem(cliente[7] if cliente[7] is not None else "Sin Membresía"))
                            tabla.setItem(tablerow, 8, QtWidgets.QTableWidgetItem(str(dias_restantes)))  # Días restantes
                            tabla.setItem(tablerow, 9, QtWidgets.QTableWidgetItem(str(cliente[8])))


                            # Cambiar el estado a "Expirado" si los días restantes son 0
                            if dias_restantes == 0:
                                estado_texto = "Expirado"
                            else:
                                estado_texto = str(cliente[8])

                            # Actualizar el estado en la columna de estado
                            estado_item = QtWidgets.QTableWidgetItem(estado_texto)
                            
                            if estado_texto.lower() == "expirado":
                                estado_item.setForeground(QtGui.QColor("red"))  # Cambiar color de texto a rojo si está Expirado o Inactivo
                                
                                boton_estado = QPushButton()
                                boton_estado.setStyleSheet("""
                                    QPushButton {
                                        image: url(:/iconos_principal/iconos/cliente_ex.png);
                                        width: 35px;
                                        height: 35px 
                                    }""")
                                
                                
                            elif estado_texto.lower() == "inactivo":
                                estado_item.setForeground(QtGui.QColor("red"))  # Cambiar color de texto a rojo si está Expirado o Inactivo
                                
                                boton_estado = QPushButton()
                                boton_estado.setStyleSheet("""
                                    QPushButton {
                                        image: url(:/iconos_principal/iconos/cliente_off.png);
                                        width: 35px;
                                        height: 35px 
                                    }""")
                                
                            else:
                                estado_item.setForeground(QtGui.QColor("green"))  # Color verde para Activo u otros estados
                                boton_estado = QPushButton()
                                boton_estado.setStyleSheet("""
                                    QPushButton {
                                        image: url(:/iconos_principal/iconos/cliente_on.png);
                                        width: 35px;
                                        height: 35px 
                                    }""")
                            tabla.setItem(tablerow, 9, estado_item)


                            # Mostrar los días restantes y marcar en rojo si son 0
                            estado_item2 = QtWidgets.QTableWidgetItem(str(dias_restantes))
                            if dias_restantes == 0:
                                estado_item2.setForeground(QtGui.QColor("red"))  # Cambiar color de texto a rojo si vencido
                            tabla.setItem(tablerow, 8, estado_item2)

                            # Actualizar en la base de datos si el estado ha cambiado a "Expirado"
                            if dias_restantes == 0:
                                try:
                                    with conexion.cursor() as cursor:
                                        cursor.execute("UPDATE clientes SET estado = %s WHERE id = %s", ("Expirado", cliente[0]))
                                    conexion.commit()
                                except Exception as e:
                                    print(f"Error al actualizar el estado en la base de datos: {e}")
    

                            for col in range(2, 10):  
                                tabla.item(tablerow, col).setFlags(QtCore.Qt.ItemIsEnabled)


                            # Crear botón Editar y usar partial para pasar la fila correcta
                            boton_editar = QPushButton()

                            boton_editar.setStyleSheet("""
                                QPushButton {
                                    image: url(:/iconos_principal/iconos/editar_tabla.png);
                                    width: 30px;
                                    height: 30px 
                                }""")
                            
                            boton_editar.clicked.connect(partial(self.llenar_campos_editar_cliente, tablerow))

                            # Crear botón Eliminar y usar partial
                            boton_eliminar = QPushButton()
                            boton_eliminar.setStyleSheet("""
                                QPushButton {
                                    image: url(:/iconos_principal/iconos/borrar_tabla.png);
                                    width: 35px;
                                    height: 35px 
                                }""")
                            
                            boton_eliminar.clicked.connect(partial(self.eliminar_cliente, tablerow))


                            boton_estado.clicked.connect(partial(self.editar_estado_cliente, tablerow))


                            # Crear un layout horizontal para contener los botones
                            widget_opciones = QWidget()
                            layout_opciones = QHBoxLayout()
                            layout_opciones.addWidget(boton_editar)
                            layout_opciones.addWidget(boton_eliminar)
                            layout_opciones.addWidget(boton_estado)
                            layout_opciones.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes
                            widget_opciones.setLayout(layout_opciones)

                            # Insertar el widget con los botones en la columna "Opciones"
                            self.ui.tabla_clientes.setCellWidget(tablerow, 10, widget_opciones)

                            tablerow += 1

                        except Exception as e:
                            print(f"Error al procesar el pago: {e}")
                else:
                    mensaje = qtw.QMessageBox(self.main_logic)
                    mensaje.setWindowTitle("Error")
                    mensaje.setText(f"No existen clientes en el sistema")
                    mensaje.setIcon(qtw.QMessageBox.Warning)
                    aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
                    mensaje.exec_()
        except Exception as ex:
            print(ex)
    

    def eliminar_cliente(self, tablerow):
      
        id_cliente = self.ui.tabla_clientes.item(tablerow, 0).text() 
        nombre_cliente = self.ui.tabla_clientes.item(tablerow, 2).text()  
        apellido_cliente = self.ui.tabla_clientes.item(tablerow, 3).text()  # Asumiendo que el apellido está en la columna 3

        # Concatenar nombre y apellido para mostrar en el mensaje
        nombre_completo = f"{nombre_cliente} {apellido_cliente}"

            
        # Crear el cuadro de diálogo de confirmación
        mensaje = QMessageBox(self.main_logic)
        mensaje.setIcon(QMessageBox.Question)
        mensaje.setWindowTitle("Eliminar Cliente")
        mensaje.setText(
            f"¿Estás seguro de que deseas eliminar al cliente '{nombre_completo}'?\n\n"
            "Esta acción es irreversible y eliminará todos los datos relacionados con este cliente en el sistema, "
            "incluyendo:\n"
            "- Medidas antropométricas\n"
            "- Asignaciones a entrenadores\n"
            "- Pagos y facturas asociadas\n"
            "- Historial de pagos\n\n"
            "¿Deseas continuar con la eliminación?"
        )

        # Añadir botones "Sí" y "No" personalizados
        boton_si = mensaje.addButton("Sí", QMessageBox.YesRole)
        boton_no = mensaje.addButton("No", QMessageBox.NoRole)

        # Aplicar el estilo del mensaje sin agregar el botón "Aceptar"
        aplicar_estilo_mensaje(mensaje, agregar_boton_aceptar=False)

        # Mostrar el cuadro de diálogo y obtener la respuesta
        respuesta = mensaje.exec_()

        # Comprobar la respuesta
        if mensaje.clickedButton() == boton_si:
            try:
                # Realizar la consulta para eliminar el cliente de la base de datos
                with conexion.cursor() as cursor:
                    # Primero eliminamos las medidas antropométricas asociadas al cliente
                    sql_medidas = "DELETE FROM medidas_antropometricas WHERE id_cliente = %s"
                    cursor.execute(sql_medidas, (id_cliente,))

                    sql_historial = "DELETE FROM historial_pagos WHERE id_cliente = %s"
                    cursor.execute(sql_historial, (id_cliente,))

                    sql_asignaciones = "DELETE FROM clientes_entrenadores WHERE id_cliente = %s"
                    cursor.execute(sql_asignaciones, (id_cliente,))

                    sql_pagos = "DELETE FROM pagos WHERE id_cliente = %s"
                    cursor.execute(sql_pagos, (id_cliente,))
                    
                    # Luego eliminamos el cliente
                    sql_cliente = "DELETE FROM clientes WHERE id = %s"
                    cursor.execute(sql_cliente, (id_cliente,))
                    conexion.commit()


                # Mostrar mensaje de éxito con el nombre del cliente
                mensaje = qtw.QMessageBox(self.main_logic)
                mensaje.setWindowTitle("Éxito")
                mensaje.setText(f"El cliente '{nombre_cliente}' ha sido eliminado correctamente.")
                mensaje.setIcon(qtw.QMessageBox.Information)
                aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
                mensaje.exec_()

                self.llenar_tabla_clientes()

            except Exception as e:
                mensaje = qtw.QMessageBox(self.main_logic)
                mensaje.setWindowTitle("Error")
                mensaje.setText("Error al eliminar el cliente, revise que la conexión a la base de datos esté disponible")
                mensaje.setIcon(qtw.QMessageBox.Critical)
                aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
                mensaje.exec_()
                return False  # Indicar que no se cargaron clientes


    def editar_estado_cliente(self, tablerow):
        # Obtener el ID y los nombres del cliente desde la tabla
        id_cliente = self.ui.tabla_clientes.item(tablerow, 0).text() 
        nombre_cliente = self.ui.tabla_clientes.item(tablerow, 2).text()
        apellido_cliente = self.ui.tabla_clientes.item(tablerow, 3).text()  # Asumiendo que el apellido está en la columna 3
        estado_actual = self.ui.tabla_clientes.item(tablerow, 9).text()  # Columna de estado (verifica que sea la columna correcta)

        # Concatenar nombre y apellido para mostrar en el mensaje
        nombre_completo = f"{nombre_cliente} {apellido_cliente}"

        if estado_actual == "Expirado":
            # Mostrar mensaje de información sobre el estado de expirado
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Estado Expirado")
            mensaje.setText("El cliente está expirado. Para reactivarlo, debe asignarle una nueva membresía.")
            mensaje.setIcon(qtw.QMessageBox.Information)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()

        else:
            # Determinar el nuevo estado
            nuevo_estado = "Inactivo" if estado_actual == "Activo" else "Activo"
            accion = "desactivado" if estado_actual == "Activo" else "activado"

            try:
                # Cambiar el estado en la base de datos
                with conexion.cursor() as cursor:
                    sql_cambiar_estado = "UPDATE clientes SET estado = %s WHERE id = %s"
                    cursor.execute(sql_cambiar_estado, (nuevo_estado, id_cliente))
                    conexion.commit()

                # Recargar la tabla para actualizarla
                self.llenar_tabla_clientes()

                # Mostrar mensaje de éxito con el nombre del cliente
                mensaje = qtw.QMessageBox(self.main_logic)
                mensaje.setWindowTitle("Éxito")
                mensaje.setText(f"El cliente '{nombre_completo}' ha sido {accion} correctamente.")
                mensaje.setIcon(qtw.QMessageBox.Information)
                aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
                mensaje.exec_()

            except Exception as e:
                mensaje = qtw.QMessageBox(self.main_logic)
                mensaje.setWindowTitle("Error")
                mensaje.setText(f"Error al cambiar el estado del cliente, revise que la conexión a la base de datos esté disponible")
                mensaje.setIcon(qtw.QMessageBox.Critical)
                aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
                mensaje.exec_()
                return False  # Indicar que no se cargaron clientes



    def llenar_campos_editar_cliente(self, tablerow):
        # Activar el modo de edición
        self.modo_edicion = True

        # Cambiar a la página de edición de cliente
        self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_crear_cliente)

        # Obtener el ID del cliente desde la tabla
        id_cliente = self.ui.tabla_clientes.item(tablerow, 0).text()  # Suponiendo que el ID está en la columna 0

        try:
            with conexion.cursor() as cursor:
                # Consulta para obtener todos los datos del cliente
                sql_cliente = """
                    SELECT num_cedula, nombres, apellidos, fecha_nacimiento, direccion, telefono, correo, fecha_registro, estado, foto
                    FROM clientes WHERE id = %s
                """
                cursor.execute(sql_cliente, (id_cliente,))
                resultado_cliente = cursor.fetchone()

                if resultado_cliente:
                    (num_cedula, nombres, apellidos, fecha_nacimiento, direccion, telefono, correo, fecha_registro, estado, foto) = resultado_cliente

                    # Convertir las fechas a QDate
                    formato_fecha = "yyyy-MM-dd"
                    fecha_nacimiento_qdate = QDate.fromString(str(fecha_nacimiento), formato_fecha)
                    fecha_registro_qdate = QDate.fromString(str(fecha_registro), formato_fecha)

                    # Cargar los datos del cliente en los campos de edición
                    self.ui.txt_cedula_cliente.setText(str(num_cedula))
                    self.ui.txt_nombres_cliente.setText(nombres)
                    self.ui.txt_apellido_cliente.setText(apellidos)
                    self.ui.txt_fecha_nacimiento_cliente.setDate(fecha_nacimiento_qdate)
                    self.ui.txt_direccion_cliente.setText(direccion)
                    self.ui.txt_telefono_cliente.setText(str(telefono))
                    self.ui.txt_correo_cliente.setText(correo)
                    self.ui.txt_fecha_registro_cliente.setDate(fecha_registro_qdate)
                    self.ui.combo_estado_cliente.setCurrentText(estado)

                    # Cargar la foto en el QLabel y actualizar self.foto_cliente
                    if foto:
                        pixmap = QPixmap()
                        pixmap.loadFromData(foto)
                        self.ui.label_foto_cliente.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))
                        self.ui.label_foto_cliente.setScaledContents(True)
                        
                        # Actualizar pixmap_actual y reconectar el evento de clic
                        self.pixmap_actual = pixmap
                        self.ui.label_foto_cliente.mousePressEvent = lambda event: ampliar_imagen_utl(self.pixmap_actual)
                        print("pixmap_actual actualizado correctamente para el cliente editado.")
                    else:
                        self.ui.label_foto_cliente.clear()
                        self.pixmap_actual = None
                        print("No se encontró foto para este cliente. pixmap_actual restablecido.")

                    # Guarda el estado inicial de los campos de texto
                    self.main_logic.guardar_estado_inicial()
                    # Mostrar modo editar
                    self.main_logic.mostrar_modo_editar()

                # Cargar medidas antropométricas
                sql_medidas = """
                    SELECT peso_corporal, altura, perimetro_pecho, perimetro_brazos, perimetro_muslos, perimetro_gluteos, 
                    perimetro_pantorrillas, perimetro_hombros 
                    FROM medidas_antropometricas WHERE id_cliente = %s
                """
                cursor.execute(sql_medidas, (id_cliente,))
                resultado_medidas = cursor.fetchone()

                if resultado_medidas:
                    (peso, altura, pecho, brazos, muslos, gluteos, pantorrillas, hombros) = resultado_medidas
                    # Cargar medidas en los campos de edición
                    self.ui.txt_peso.setText(str(peso) if peso is not None else "")
                    self.ui.txt_altura.setText(str(altura) if altura is not None else "")
                    self.ui.txt_medida_pecho.setText(str(pecho) if pecho is not None else "")
                    self.ui.txt_medida_brazos.setText(str(brazos) if brazos is not None else "")
                    self.ui.txt_medida_muslos.setText(str(muslos) if muslos is not None else "")
                    self.ui.txt_medida_gluteos.setText(str(gluteos) if gluteos is not None else "")
                    self.ui.txt_medida_pantorrillas.setText(str(pantorrillas) if pantorrillas is not None else "")
                    self.ui.txt_medida_hombros.setText(str(hombros) if hombros is not None else "")
                else:
                    # Si no existen medidas, limpiar los campos
                    self.ui.txt_peso.clear()
                    self.ui.txt_altura.clear()
                    self.ui.txt_medida_pecho.clear()
                    self.ui.txt_medida_brazos.clear()
                    self.ui.txt_medida_muslos.clear()
                    self.ui.txt_medida_gluteos.clear()
                    self.ui.txt_medida_pantorrillas.clear()
                    self.ui.txt_medida_hombros.clear()

                # Guardar el ID del cliente que estamos editando
                self.cliente_id_actual = id_cliente

        except Exception as e:
            print(f"Error capturado: {e}") 
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al cargar los datos del cliente, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()
            return False  # Indicar que no se cargaron clientes




    def editar_cliente(self):

        # Validación de campos obligatorios
        campos_obligatorios = [
            (self.ui.txt_cedula_cliente, "Número de cédula"),
            (self.ui.txt_nombres_cliente, "Nombres"),
            (self.ui.txt_apellido_cliente, "Apellidos"),
            (self.ui.txt_telefono_cliente, "Teléfono"),
        ]

        # usamos la funcion de validaciones
        if not validar_campos_obligatorios(campos_obligatorios, self.main_logic):
            return  # Detener la ejecución si hay campos vacíos
        
        # Validar fecha de nacimiento
        fecha_nacimiento = self.ui.txt_fecha_nacimiento_cliente.text()
        if not validar_fecha_nacimiento(fecha_nacimiento, self.main_logic):
            return

        # Validar correo electrónico
        correo = self.ui.txt_correo_cliente.text()
        if not validar_correo(correo, self.main_logic):
            return
        
        # Obtener los valores editados desde los campos
        cedula_editada = self.ui.txt_cedula_cliente.text()
        nombres_editados = self.ui.txt_nombres_cliente.text()
        apellidos_editados = self.ui.txt_apellido_cliente.text()
        fecha_nacimiento_editada = self.ui.txt_fecha_nacimiento_cliente.date().toString('yyyy-MM-dd')
        direccion_editada = self.ui.txt_direccion_cliente.text()
        telefono_editado = self.ui.txt_telefono_cliente.text()
        correo_editado = self.ui.txt_correo_cliente.text()
        fecha_registro_editada = self.ui.txt_fecha_registro_cliente.date().toString('yyyy-MM-dd')
        estado = self.ui.combo_estado_cliente.currentText()

        # Datos opcionales
        foto_editada = self.logica_camara.foto_cliente if self.logica_camara.foto_cliente is not None else self.foto_cliente
        peso_editado = self.ui.txt_peso.text() if self.ui.txt_peso.text() != "" else None
        altura_editada = self.ui.txt_altura.text() if self.ui.txt_altura.text() != "" else None
        imc_editado = calcular_imc(self) 
        pecho_editado = self.ui.txt_medida_pecho.text() if self.ui.txt_medida_pecho.text() != "" else None
        brazos_editados = self.ui.txt_medida_brazos.text() if self.ui.txt_medida_brazos.text() != "" else None
        muslos_editados = self.ui.txt_medida_muslos.text() if self.ui.txt_medida_muslos.text() != "" else None
        gluteos_editados = self.ui.txt_medida_gluteos.text() if self.ui.txt_medida_gluteos.text() != "" else None
        pantorrillas_editadas = self.ui.txt_medida_pantorrillas.text() if self.ui.txt_medida_pantorrillas.text() != "" else None
        hombros_editados = self.ui.txt_medida_hombros.text() if self.ui.txt_medida_hombros.text() != "" else None

      

        try:
            with conexion.cursor() as cursor:
                # Actualizar los datos del cliente en la base de datos
                sql_cliente = """
                    UPDATE clientes
                    SET num_cedula = %s, nombres = %s, apellidos = %s, fecha_nacimiento = %s, direccion = %s, 
                    telefono = %s, correo = %s, fecha_registro = %s, estado = %s, foto = %s WHERE id = %s"""
                
                cursor.execute(sql_cliente, (cedula_editada, nombres_editados, apellidos_editados, fecha_nacimiento_editada, 
                                            direccion_editada, telefono_editado, correo_editado, fecha_registro_editada, estado, foto_editada, 
                                            self.cliente_id_actual))

                # Verificar si ya existen medidas antropométricas para el cliente
                sql_verificar_medidas = "SELECT COUNT(*) FROM medidas_antropometricas WHERE id_cliente = %s"
                cursor.execute(sql_verificar_medidas, (self.cliente_id_actual,))
                tiene_medidas = cursor.fetchone()[0]

                # Si existen medidas, actualizarlas; si no, insertarlas
                if tiene_medidas:
                    sql_medidas = """
                        UPDATE medidas_antropometricas
                        SET peso_corporal = %s, altura = %s, imc = %s, perimetro_pecho = %s, perimetro_brazos = %s, 
                            perimetro_muslos = %s, perimetro_gluteos = %s, perimetro_pantorrillas = %s, perimetro_hombros = %s
                        WHERE id_cliente = %s
                    """
                    cursor.execute(sql_medidas, (peso_editado, altura_editada, imc_editado, pecho_editado, brazos_editados, muslos_editados,
                                                gluteos_editados, pantorrillas_editadas, hombros_editados, self.cliente_id_actual))
                else:
                    sql_insertar_medidas = """
                        INSERT INTO medidas_antropometricas (peso_corporal, altura, imc, perimetro_pecho, perimetro_brazos, 
                        perimetro_muslos, perimetro_gluteos, perimetro_pantorrillas, perimetro_hombros, id_cliente)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql_insertar_medidas, (peso_editado, altura_editada, imc_editado, pecho_editado, brazos_editados, 
                                                        muslos_editados, gluteos_editados, pantorrillas_editadas, 
                                                        hombros_editados, self.cliente_id_actual))

                # Confirmar los cambios
                conexion.commit()

                mensaje = qtw.QMessageBox(self.main_logic)
                mensaje.setWindowTitle("Éxito")
                mensaje.setText("El cliente ha sido actualizado correctamente.")
                mensaje.setIcon(qtw.QMessageBox.Information)
                aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
                mensaje.exec_()
                
                # Regresar a la vista de la tabla de clientes
                self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_clientes)

                # Recargar los datos en la tabla de clientes
                self.llenar_tabla_clientes()

        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al actualizar el cliente, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()
            return False  # Indicar que no se cargaron clientes


    
    #>Pagina buscar clientes   
    def pagina_buscar_cliente(self):
        # Cambiar a la página de 
        self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_buscar_cliente)
        self.ui.tabWidget.setCurrentIndex(0)
       

         #llamamos la funcion para buscar cliente por nombre
        self.ui.txt_consulta_buscar_cliente_nombre.textChanged.connect(self.buscar_cliente_por_nombre)
        self.ui.Lista_clientes_por_nombre.itemClicked.connect(self.mostrar_cliente_en_tabla)

        #para que cada vez que entre a buscar cliente por nombre se limpien los datos
        self.ui.bt_buscar_cliente.clicked.connect(self.limpiar_busqueda_cliente)

        self.llenar_combo_membresias_buscar(mostrar_advertencia=True)


        

    #!MANEJO DE TABS   
    #*TAB - 0
    # Función para buscar clientes por nombre
    def buscar_cliente_por_nombre(self):
        nombre_cliente = self.ui.txt_consulta_buscar_cliente_nombre.text()

        # Limpiar la lista de clientes antes de cargar nuevos resultados
        self.ui.Lista_clientes_por_nombre.clear()

        try:
            with conexion.cursor() as cursor:
                # Consulta SQL para buscar clientes por nombre, incluyendo la dirección
                sql = "SELECT id, num_cedula, nombres, apellidos, telefono, correo, direccion FROM clientes WHERE nombres LIKE %s"
                cursor.execute(sql, ('%' + nombre_cliente + '%',))
                resultados = cursor.fetchall()

                # Cargar los resultados en el QListWidget
                for id_cliente, nombres, apellidos, cedula, telefono, correo, direccion in resultados:
                    item_texto = f"{nombres} {apellidos} - {cedula}"
                    item = QListWidgetItem(item_texto)
                    item.setData(Qt.UserRole, id_cliente)  # Guardar el ID del cliente en el ítem
                    self.ui.Lista_clientes_por_nombre.addItem(item)
                    
        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al buscar los clientes, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()
            return False  # Indicar que no se cargaron clientes
    

    # Función para mostrar los detalles del cliente en la QTableWidget
    def mostrar_cliente_en_tabla(self, item):
        id_cliente = item.data(Qt.UserRole)  # Obtener el ID del cliente del ítem seleccionado
        self.ui.tabla_clientes_consulta_nombre.verticalHeader().setVisible(False)

        try:
            with conexion.cursor() as cursor:
                # Consulta SQL para obtener todos los detalles del cliente
                sql = "SELECT nombres, apellidos, num_cedula, telefono, correo, direccion FROM clientes WHERE id = %s"
                cursor.execute(sql, (id_cliente,))
                resultado = cursor.fetchone()

                if resultado:
                    nombres, apellidos, cedula, telefono, correo, direccion = resultado

                    # Limpiar la tabla antes de cargar los datos
                    self.ui.tabla_clientes_consulta_nombre.setRowCount(0)
                    self.ui.tabla_clientes_consulta_nombre.insertRow(0)
                    self.ui.tabla_clientes_consulta_nombre.setItem(0, 0, QTableWidgetItem(nombres))
                    self.ui.tabla_clientes_consulta_nombre.setItem(0, 1, QTableWidgetItem(apellidos))
                    self.ui.tabla_clientes_consulta_nombre.setItem(0, 2, QTableWidgetItem(str(cedula)))  # Columna de Cédula
                    self.ui.tabla_clientes_consulta_nombre.setItem(0, 3, QTableWidgetItem(str(telefono)))
                    self.ui.tabla_clientes_consulta_nombre.setItem(0, 4, QTableWidgetItem(correo))
                    self.ui.tabla_clientes_consulta_nombre.setItem(0, 5, QTableWidgetItem(direccion))  # Columna de Dirección

        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al cargar los detalles del cliente, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()    
            return False  # Indicar que no se cargaron clientes
                  

    def limpiar_busqueda_cliente(self):
        # Limpiar el campo de texto del nombre del cliente
        self.ui.txt_consulta_buscar_cliente_nombre.clear()

        # Limpiar el QListWidget donde aparecen los nombres filtrados
        self.ui.Lista_clientes_por_nombre.clear()

        # Limpiar la tabla donde se muestran los detalles del cliente
        self.ui.tabla_clientes_consulta_nombre.setRowCount(0)


    #*TAB - 1-----------------------------------------------------------
    # Página buscar clientes con medidas antropométricas
    def pagina_buscar_medidas(self):
        # Cambiar a la página de buscar medidas
        self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_buscar_medidas_cliente)

        # Limpiar el QComboBox de clientes y la tabla de medidas
        self.ui.combo_buscar_medidas_cliente.clear()  # Limpiar el combobox
        self.ui.tabla_medidas_cliente.setRowCount(0)  # Limpiar la tabla

        # Llamamos a la función para cargar solo los clientes con medidas antropométricas
        clientes_cargados = self.cargar_clientes_con_medidas_combobox(mostrar_advertencia=True)

        # Solo conectar el combobox y cargar el primer cliente si hay clientes cargados
        if clientes_cargados:
            # Conectar el combobox al evento de selección
            self.ui.combo_buscar_medidas_cliente.currentIndexChanged.connect(self.cliente_seleccionado_medidas)
            
            # Cargar las medidas del primer cliente (dato 0) si está disponible
            self.cliente_seleccionado_medidas()
        

    # FUNCIONES BUSCAR MEDIDAS DE CLIENTES
    def cargar_clientes_con_medidas_combobox(self, mostrar_advertencia=False):
        try:
            # Realiza la consulta para obtener solo los clientes que tienen medidas
            with conexion.cursor() as cursor:
                sql = """
                SELECT c.id, c.nombres, c.apellidos
                FROM clientes c
                JOIN medidas_antropometricas m ON c.id = m.id_cliente
                """
                cursor.execute(sql)
                resultados = cursor.fetchall()

                # Verificar si no hay resultados
                if not resultados:
                    if mostrar_advertencia:
                        mensaje = qtw.QMessageBox(self.main_logic)
                        mensaje.setText("No se encontraron clientes con medidas registradas.")
                        mensaje.setIcon(qtw.QMessageBox.Warning)
                        aplicar_estilo_mensaje(mensaje)
                        mensaje.exec_()
                    return False  # Indicar que no hay clientes cargados

                # Cargar los resultados en el combobox
                for id_cliente, nombres, apellidos in resultados:
                    cliente_nombre = f"{nombres} {apellidos}"
                    self.ui.combo_buscar_medidas_cliente.addItem(cliente_nombre, id_cliente)

                return True  # Indicar que se cargaron clientes

        except Exception as e:
            
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al cargar los clientes, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()
            return False  # Indicar que no se cargaron clientes

    def cliente_seleccionado_medidas(self):
        # Obtener el id del cliente seleccionado del combobox
        id_cliente = self.ui.combo_buscar_medidas_cliente.currentData()
        self.ui.tabla_medidas_cliente.verticalHeader().setVisible(False)

        # Si no hay cliente seleccionado (ComboBox vacío o cliente no válido)
        if id_cliente is None:
            return  # Salir de la función sin mostrar el mensaje

        try:
            # Consultar las medidas antropométricas del cliente seleccionado
            with conexion.cursor() as cursor:
                sql = """
                SELECT peso_corporal, altura, perimetro_pecho, perimetro_brazos, perimetro_muslos, 
                    perimetro_gluteos, perimetro_pantorrillas, perimetro_hombros
                FROM medidas_antropometricas
                WHERE id_cliente = %s
                """
                cursor.execute(sql, (id_cliente,))
                resultado = cursor.fetchone()

                if resultado:
                    # Preparar la tabla con las filas necesarias
                    self.ui.tabla_medidas_cliente.setRowCount(1)

                    # Colocar peso y altura en las primeras dos columnas
                    for columna, valor in enumerate(resultado[:2]):
                        texto = "Sin datos" if valor is None else str(valor)
                        item = QTableWidgetItem(texto)
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                        self.ui.tabla_medidas_cliente.setItem(0, columna, item)

                    # Calcular y colocar el IMC en la tercera columna (índice 2)
                    peso_corporal, altura = resultado[0], resultado[1]
                    if peso_corporal is not None and altura is not None and altura > 0:
                        altura_m = altura / 100  # Convertir altura a metros
                        imc = peso_corporal / (altura_m ** 2)
                        imc_texto = f"{imc:.2f}"  # Formatear el IMC con 2 decimales
                    else:
                        imc_texto = "Sin datos"

                    # Asignar el IMC a la tercera columna
                    imc_item = QTableWidgetItem(imc_texto)
                    imc_item.setFlags(imc_item.flags() & ~Qt.ItemIsEditable)
                    self.ui.tabla_medidas_cliente.setItem(0, 2, imc_item)

                    # Insertar las demás medidas en las columnas correspondientes después del IMC
                    for columna, valor in enumerate(resultado[2:], start=3):  # Comienza desde la cuarta columna
                        texto = "Sin datos" if valor is None else str(valor)
                        item = QTableWidgetItem(texto)
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                        self.ui.tabla_medidas_cliente.setItem(0, columna, item)

                else:
                    # Mostrar mensaje si el cliente no tiene medidas
                    mensaje = qtw.QMessageBox(self.main_logic)
                    mensaje.setWindowTitle("Advertencia")
                    mensaje.setText("El cliente no tiene medidas registradas.")
                    mensaje.setIcon(qtw.QMessageBox.Warning)
                    aplicar_estilo_mensaje(mensaje)
                    mensaje.exec_()

        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText("Error al cargar las medidas, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()




    #*TAB - 2-----------------------------------------------------------------------------
    #Pagina buscar clientes con medidas antropometricas
    
    def pagina_buscar_estado(self):
        # Cambiar a la página de buscar medidas
        self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_buscar_cliente_estado)
        # Cargar la consulta para el valor por defecto del combo box
        self.cargar_consulta_clientes_estado()

    # Función para cargar los datos de la consulta seleccionada
    def cargar_consulta_clientes_estado(self):
        tipo_consulta = self.ui.combo_buscar_estado_cliente.currentText()

        if tipo_consulta == "Activo":
            self.consultar_estado_activo(mostrar_advertencia=True)
        elif tipo_consulta == "Inactivo":
            self.consultar_estado_inactivo(mostrar_advertencia=True)

  

    # Consulta para clientes con membresía mensual
    def consultar_estado_activo(self, mostrar_advertencia=False):
        self.ui.tabla_estado_clientes.setRowCount(0)  # Limpiar tabla
        self.ui.tabla_estado_clientes.verticalHeader().setVisible(False)
        try:
            with conexion.cursor() as cursor:
                sql = """
                 SELECT num_cedula, nombres, apellidos, fecha_registro FROM clientes WHERE estado = 'Activo'"""
                cursor.execute(sql)
                resultados = cursor.fetchall()

                                # Verificar si no hay resultados
                if not resultados:
                    if mostrar_advertencia:
                        mensaje = qtw.QMessageBox(self.main_logic)
                        mensaje.setText("No se encontraron clientes activos en el sistema.")
                        mensaje.setIcon(qtw.QMessageBox.Warning)
                        aplicar_estilo_mensaje(mensaje)
                        mensaje.exec_()
                    return False  # Indicar que no hay clientes cargados

                for fila, (cedula, nombre, apellido, fecha_registro) in enumerate(resultados):
                    self.ui.tabla_estado_clientes.insertRow(fila)
                    self.ui.tabla_estado_clientes.setItem(fila, 0, QTableWidgetItem(str(cedula)))
                    self.ui.tabla_estado_clientes.setItem(fila, 1, QTableWidgetItem(nombre))
                    self.ui.tabla_estado_clientes.setItem(fila, 2, QTableWidgetItem(apellido))
                    self.ui.tabla_estado_clientes.setItem(fila, 3, QTableWidgetItem(str(fecha_registro)))

                    
                    # Desactivar la edición de las celdas 
                    for col in range(4): 
                        for row in range(self.ui.tabla_estado_clientes.rowCount()):
                            item = self.ui.tabla_estado_clientes.item(row, col)
                            if item is not None:
                                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)  


        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al cargar los clientes, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()

     # Consulta para clientes con membresía mensual
    def consultar_estado_inactivo(self, mostrar_advertencia=False):
        self.ui.tabla_estado_clientes.setRowCount(0)  # Limpiar tabla
        self.ui.tabla_estado_clientes.verticalHeader().setVisible(False)
        try:
            with conexion.cursor() as cursor:
                sql = """
                 SELECT num_cedula, nombres, apellidos, fecha_registro FROM clientes WHERE estado = 'Inactivo'"""
                cursor.execute(sql)
                resultados = cursor.fetchall()

                if not resultados:
                    if mostrar_advertencia:
                        mensaje = qtw.QMessageBox(self.main_logic)
                        mensaje.setText("No se encontraron clientes inactivos en el sistema.")
                        mensaje.setIcon(qtw.QMessageBox.Warning)
                        aplicar_estilo_mensaje(mensaje)
                        mensaje.exec_()
                    return False  # Indicar que no hay clientes cargados

                for fila, (cedula, nombre, apellido, fecha_registro) in enumerate(resultados):
                    self.ui.tabla_estado_clientes.insertRow(fila)
                    self.ui.tabla_estado_clientes.setItem(fila, 0, QTableWidgetItem(str(cedula)))
                    self.ui.tabla_estado_clientes.setItem(fila, 1, QTableWidgetItem(nombre))
                    self.ui.tabla_estado_clientes.setItem(fila, 2, QTableWidgetItem(apellido))
                    self.ui.tabla_estado_clientes.setItem(fila, 3, QTableWidgetItem(str(fecha_registro)))

                    # Desactivar la edición de las celdas 
                    for col in range(4): 
                        for row in range(self.ui.tabla_estado_clientes.rowCount()):
                            item = self.ui.tabla_estado_clientes.item(row, col)
                            if item is not None:
                                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)  


        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al cargar los clientes, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()


    #*TAB - 3-----------------------------------------------------------------------------------
    #Pagina buscar clientes con medidas antropometricas
    def pagina_buscar_membresia(self):
        # Cambiar a la página de buscar membresías de clientes
        self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_buscar_cliente_membresia)
        
        # Llenar el ComboBox de membresías y conectar el evento de selección al método correcto
        self.llenar_combo_membresias_buscar()
        
       

        self.cliente_seleccionado_membresia() #carga el dato 0 del combo

    def llenar_combo_membresias_buscar(self, mostrar_advertencia=False):
        try:
            with conexion.cursor() as cursor:
                # Obtener las membresías activas
                sql = "SELECT id, nombre FROM membresias WHERE estado = 'Activo'"
                cursor.execute(sql)
                membresias = cursor.fetchall()

                # Desactivar las señales mientras se llena el ComboBox
                self.ui.combo_buscar_membresia_cliente.blockSignals(True)

                # Mensaje de advertencia si no hay membresías
                if not membresias and mostrar_advertencia:
                    mensaje = qtw.QMessageBox(self.main_logic)
                    mensaje.setText("No se encontraron membresías en el sistema.")
                    mensaje.setIcon(qtw.QMessageBox.Warning)
                    aplicar_estilo_mensaje(mensaje)
                    mensaje.exec_()

                # Llenar el ComboBox de membresías
                self.ui.combo_buscar_membresia_cliente.clear()
                for membresia in membresias:
                    id = membresia[0]
                    nombre = membresia[1]
                    # Agregar al ComboBox el nombre
                    self.ui.combo_buscar_membresia_cliente.addItem(nombre, id)

                # Reactivar las señales después de llenar el ComboBox
                self.ui.combo_buscar_membresia_cliente.blockSignals(False)

        except Exception as ex:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"No se pudo cargar el listado de membresías, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()

    def cliente_seleccionado_membresia(self):
        self.ui.tabla_membresia_clientes.setRowCount(0)  # Limpiar tabla
        self.ui.tabla_membresia_clientes.verticalHeader().setVisible(False)
        id_membresia = self.ui.combo_buscar_membresia_cliente.currentData()

        if id_membresia is None:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Advertencia")
            mensaje.setText("No se encontraron datos de membresía para el cliente seleccionado.")
            mensaje.setIcon(qtw.QMessageBox.Warning)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()
            return

        try:
            with conexion.cursor() as cursor:
                # Seleccionar solo los clientes con una membresía activa
                sql = """
                    SELECT clientes.num_cedula, clientes.nombres, clientes.apellidos, pagos.fecha_inicio, pagos.fecha_fin
                    FROM clientes
                    INNER JOIN pagos ON clientes.id = pagos.id_cliente
                    WHERE pagos.id_membresia = %s AND pagos.fecha_fin >= CURDATE() 
                """
                #curdate para que solo se seleccionen registros donde la fecha de fin de la membresía (almacenada en pagos.fecha_fin) 
                # es hoy o en el futuro. Esto significa que la membresía sigue vigente y no ha expirado.

                cursor.execute(sql, (id_membresia,))
                resultados = cursor.fetchall()

                if resultados:
                    # Llenar la tabla con los resultados
                    for fila, (cedula, nombre, apellido, fecha_inicio, fecha_fin) in enumerate(resultados):
                        self.ui.tabla_membresia_clientes.insertRow(fila)
                        self.ui.tabla_membresia_clientes.setItem(fila, 0, QTableWidgetItem(str(cedula)))
                        self.ui.tabla_membresia_clientes.setItem(fila, 1, QTableWidgetItem(nombre))
                        self.ui.tabla_membresia_clientes.setItem(fila, 2, QTableWidgetItem(apellido))
                        self.ui.tabla_membresia_clientes.setItem(fila, 3, QTableWidgetItem(str(fecha_inicio)))
                        self.ui.tabla_membresia_clientes.setItem(fila, 4, QTableWidgetItem(str(fecha_fin)))

                        # Desactivar la edición de las celdas 
                        for col in range(5): 
                            for row in range(self.ui.tabla_membresia_clientes.rowCount()):
                                item = self.ui.tabla_membresia_clientes.item(row, col)
                                if item is not None:
                                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)  
                else:
                    # Mostrar un mensaje si no se encontraron clientes activos en la membresía seleccionada
                    mensaje = qtw.QMessageBox(self.main_logic)
                    mensaje.setWindowTitle("Advertencia")
                    mensaje.setText("No se encontraron clientes activos en la membresía seleccionada.")
                    mensaje.setIcon(qtw.QMessageBox.Warning)
                    aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
                    mensaje.exec_()

        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al cargar los clientes, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()



    #*TAB - 4-----------------------------------------------------------------------------------------------
    #Pagina buscar clientes con medidas antropometricas
    def pagina_buscar_filtro(self):
        # Cambiar a la página de buscar medidas
        self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_filtros_consultas_cliente)

        self.ui.combo_buscar_tipo_consulta.currentIndexChanged.connect(self.cargar_consulta_clientes_filtros)
        self.cargar_consulta_clientes_filtros() #carga el dato 0 del combo

        
        
       
       
                                                # Desactivar la edición de las celdas 
        for col in range(7): 
            for row in range(self.ui.tabla_consultas_clientes.rowCount()):
                item = self.ui.tabla_consultas_clientes.item(row, col)
                if item is not None:
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)  
    
    #FUNCIONES PARA HACER CONSULTAS SEGUN EL FILTRO

    # Función para cargar los datos de la consulta seleccionada
    def cargar_consulta_clientes_filtros(self):
        self.ui.tabla_consultas_clientes.verticalHeader().setVisible(False)
        tipo_consulta = self.ui.combo_buscar_tipo_consulta.currentText()

        if tipo_consulta == "Ordenar de A a Z":
            self.consultar_clientes_ordenados_AZ()
            self.consultar_clientes_ordenados_AZ(mostrar_advertencia=True)
        elif tipo_consulta == "Ordenar de Z a A":
            self.consultar_clientes_ordenados_ZA()
            self.consultar_clientes_ordenados_ZA(mostrar_advertencia=True)
        elif tipo_consulta == "Clientes nuevos":
            self.consultar_clientes_nuevos()
            self.consultar_clientes_nuevos(mostrar_advertencia=True)
        elif tipo_consulta == "Clientes antiguos":
            self.consultar_clientes_antiguos()
            self.consultar_clientes_antiguos(mostrar_advertencia=True)


 # Consulta para clientes ordenados alfabéticamente
    def consultar_clientes_ordenados_AZ(self, mostrar_advertencia=False):
        self.ui.tabla_consultas_clientes.setRowCount(0)  # Limpiar tabla
        try:
            with conexion.cursor() as cursor:
                sql = """
                    SELECT num_cedula, nombres, apellidos, direccion, telefono, correo,
                    fecha_registro FROM clientes ORDER BY clientes.nombres ASC;"""
                cursor.execute(sql)
                resultados = cursor.fetchall()

                if not resultados:
                    if mostrar_advertencia:
                        mensaje = qtw.QMessageBox(self.main_logic)
                        mensaje.setText("No se encontraron clientes en el sistema.")
                        mensaje.setIcon(qtw.QMessageBox.Warning)
                        aplicar_estilo_mensaje(mensaje)
                        mensaje.exec_()
                    return False  # Indicar que no hay clientes cargados

                for fila, (cedula, nombres, apellidos, direccion, telefono, correo, fecha_registro) in enumerate(resultados):
                    self.ui.tabla_consultas_clientes.insertRow(fila)
                    self.ui.tabla_consultas_clientes.setItem(fila, 0, QTableWidgetItem(str(cedula)))
                    self.ui.tabla_consultas_clientes.setItem(fila, 1, QTableWidgetItem(nombres))
                    self.ui.tabla_consultas_clientes.setItem(fila, 2, QTableWidgetItem(apellidos))
                    self.ui.tabla_consultas_clientes.setItem(fila, 3, QTableWidgetItem(direccion))
                    self.ui.tabla_consultas_clientes.setItem(fila, 4, QTableWidgetItem(str(telefono)))
                    self.ui.tabla_consultas_clientes.setItem(fila, 5, QTableWidgetItem(correo))
                    self.ui.tabla_consultas_clientes.setItem(fila, 6, QTableWidgetItem(str(fecha_registro)))


        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al cargar los clientes, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()
    

    def consultar_clientes_ordenados_ZA(self, mostrar_advertencia=False):
        self.ui.tabla_consultas_clientes.setRowCount(0)  # Limpiar tabla
        try:
            with conexion.cursor() as cursor:
                sql = """
                    SELECT num_cedula, nombres, apellidos, direccion, telefono, correo,
                    fecha_registro FROM clientes ORDER BY clientes.nombres DESC;"""
                cursor.execute(sql)
                resultados = cursor.fetchall()

                if not resultados:
                    if mostrar_advertencia:
                        mensaje = qtw.QMessageBox(self.main_logic)
                        mensaje.setText("No se encontraron clientes en el sistema.")
                        mensaje.setIcon(qtw.QMessageBox.Warning)
                        aplicar_estilo_mensaje(mensaje)
                        mensaje.exec_()
                    return False  # Indicar que no hay clientes cargados

                for fila, (cedula, nombres, apellidos, direccion, telefono, correo, fecha_registro) in enumerate(resultados):
                    self.ui.tabla_consultas_clientes.insertRow(fila)
                    self.ui.tabla_consultas_clientes.setItem(fila, 0, QTableWidgetItem(str(cedula)))
                    self.ui.tabla_consultas_clientes.setItem(fila, 1, QTableWidgetItem(nombres))
                    self.ui.tabla_consultas_clientes.setItem(fila, 2, QTableWidgetItem(apellidos))
                    self.ui.tabla_consultas_clientes.setItem(fila, 3, QTableWidgetItem(direccion))
                    self.ui.tabla_consultas_clientes.setItem(fila, 4, QTableWidgetItem(str(telefono)))
                    self.ui.tabla_consultas_clientes.setItem(fila, 5, QTableWidgetItem(correo))
                    self.ui.tabla_consultas_clientes.setItem(fila, 6, QTableWidgetItem(str(fecha_registro)))

        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al cargar los clientes, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()


    def consultar_clientes_nuevos(self, mostrar_advertencia=False):
        self.ui.tabla_consultas_clientes.setRowCount(0)  # Limpiar tabla
        try:
            with conexion.cursor() as cursor:
                sql = """
                    SELECT num_cedula, nombres, apellidos, direccion, telefono, correo, fecha_registro FROM clientes 
                    WHERE fecha_registro >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) ORDER BY fecha_registro DESC;
                    """
                cursor.execute(sql)
                resultados = cursor.fetchall()

                if not resultados:
                    if mostrar_advertencia:
                        mensaje = qtw.QMessageBox(self.main_logic)
                        mensaje.setText("No se encontraron clientes nuevos en el sistema.")
                        mensaje.setIcon(qtw.QMessageBox.Warning)
                        aplicar_estilo_mensaje(mensaje)
                        mensaje.exec_()
                    return False  # Indicar que no hay clientes cargados

                for fila, (cedula, nombres, apellidos, direccion, telefono, correo, fecha_registro) in enumerate(resultados):
                    self.ui.tabla_consultas_clientes.insertRow(fila)
                    self.ui.tabla_consultas_clientes.setItem(fila, 0, QTableWidgetItem(str(cedula)))
                    self.ui.tabla_consultas_clientes.setItem(fila, 1, QTableWidgetItem(nombres))
                    self.ui.tabla_consultas_clientes.setItem(fila, 2, QTableWidgetItem(apellidos))
                    self.ui.tabla_consultas_clientes.setItem(fila, 3, QTableWidgetItem(direccion))
                    self.ui.tabla_consultas_clientes.setItem(fila, 4, QTableWidgetItem(str(telefono)))
                    self.ui.tabla_consultas_clientes.setItem(fila, 5, QTableWidgetItem(correo))
                    self.ui.tabla_consultas_clientes.setItem(fila, 6, QTableWidgetItem(str(fecha_registro)))

        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al cargar los clientes, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()



    def consultar_clientes_antiguos(self, mostrar_advertencia=False):
        self.ui.tabla_consultas_clientes.setRowCount(0)  # Limpiar tabla
        try:
            with conexion.cursor() as cursor:
                sql = """
                    SELECT num_cedula, nombres, apellidos, direccion, telefono, correo, fecha_registro FROM clientes 
                    WHERE fecha_registro < DATE_SUB(CURDATE(), INTERVAL 365 DAY) ORDER BY fecha_registro ASC;
                    """
                cursor.execute(sql)
                resultados = cursor.fetchall()

                if not resultados:
                    if mostrar_advertencia:
                        mensaje = qtw.QMessageBox(self.main_logic)
                        mensaje.setText("No se encontraron clientes antiguos en el sistema.")
                        mensaje.setIcon(qtw.QMessageBox.Warning)
                        aplicar_estilo_mensaje(mensaje)
                        mensaje.exec_()
                    return False  # Indicar que no hay clientes cargados

                for fila, (cedula, nombres, apellidos, direccion, telefono, correo, fecha_registro) in enumerate(resultados):
                    self.ui.tabla_consultas_clientes.insertRow(fila)
                    self.ui.tabla_consultas_clientes.setItem(fila, 0, QTableWidgetItem(str(cedula)))
                    self.ui.tabla_consultas_clientes.setItem(fila, 1, QTableWidgetItem(nombres))
                    self.ui.tabla_consultas_clientes.setItem(fila, 2, QTableWidgetItem(apellidos))
                    self.ui.tabla_consultas_clientes.setItem(fila, 3, QTableWidgetItem(direccion))
                    self.ui.tabla_consultas_clientes.setItem(fila, 4, QTableWidgetItem(str(telefono)))
                    self.ui.tabla_consultas_clientes.setItem(fila, 5, QTableWidgetItem(correo))
                    self.ui.tabla_consultas_clientes.setItem(fila, 6, QTableWidgetItem(str(fecha_registro)))

        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al cargar los clientes, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()



    #!página con tabla y acciones crear ver y asignar
    def ir_a_pagina_entrenadores(self):

        self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_entrenadores)
        self.llenar_tabla_entrenadores()
    
    #!Método para manejar la acción de "Crear Cliente" (al dar clic a crear)
    def abrir_pantalla_crear_entrenador(self):
        # Cambiar a modo de creación
        self.modo_edicion = False

        self.main_logic.mostrar_modo_crear()
        self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_crear_entrenador)

        #Guarda el estado inicial de los campos de texto
        self.main_logic.guardar_estado_inicial()

    def crear_entrenador(self):

        # Validación de campos obligatorios
        campos_obligatorios = [
        (self.ui.txt_cedula_entrenador, "Número de cédula"),
        (self.ui.txt_nombres_entrenador, "Nombres"),
        (self.ui.txt_apellido_entrenador, "Apellidos"),
        (self.ui.txt_telefono_entrenador, "Teléfono"),
        ]

         # usamos la funcion de validaciones
        if not validar_campos_obligatorios(campos_obligatorios, self.main_logic):
            return  # Detener la ejecución si hay campos vacíos

        # Obtener datos de los campos
        numero_cedula = self.ui.txt_cedula_entrenador.text()
        nombres = self.ui.txt_nombres_entrenador.text()
        apellidos = self.ui.txt_apellido_entrenador.text()
        direccion = self.ui.txt_direccion_entrenador.text()
        num_telefono = self.ui.txt_telefono_entrenador.text()
        fecha_contratacion = self.ui.txt_fecha_contrato_entrenador.text()

        # Validar correo electrónico
        correo = self.ui.txt_correo_entrenador.text()
        if not validar_correo(correo, self.main_logic):
            return
        
        # Combo box
        especialidad = self.ui.combo_especialidad_entrenador.currentText()
        estado = self.ui.combo_estado_entrenador.currentText()

        # Validación: No permitir que "Seleccione" sea enviado
        if especialidad == "Seleccione":
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText("Debe seleccionar una especialidad válida")
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.setIcon(qtw.QMessageBox.Warning)
            mensaje.exec_()
            return  # Evita continuar si no se seleccionó una opción válida

        try:
            with conexion.cursor() as cursor:
                # Inserta los datos en la tabla entrenadores
                sql = "INSERT INTO entrenadores (num_cedula, nombres, apellidos, direccion, num_telefono, correo, especialidad, fecha_contratacion, estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (numero_cedula, nombres, apellidos, direccion, num_telefono, correo, especialidad, fecha_contratacion, estado))
                conexion.commit()

            self.main_logic.limpiar_campos()
               
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Éxito")
            mensaje.setText("El nuevo entrenador se ha creado correctamente")
            mensaje.setIcon(qtw.QMessageBox.Information)
            aplicar_estilo_mensaje(mensaje)
            mensaje.exec_()

            self.llenar_tabla_entrenadores()

            return True

        except Exception as ex:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Fallo al almacenar los datos, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()

            return False


    def llenar_tabla_entrenadores(self):
            tabla = self.ui.tabla_entrenadores  # Asegúrate de que este sea el nombre correcto de tu tabla
            self.ui.tabla_entrenadores.verticalHeader().setVisible(False)

            try:
                with conexion.cursor() as cursor:
                    # Se realiza la consulta a la base de datos (mostrar todos los clientes incluso aquellos que no tienen un pago asociado LEFT JOIN)
                    sql = """SELECT id, num_cedula, nombres, apellidos, direccion, num_telefono, correo, especialidad, fecha_contratacion, estado
                            FROM entrenadores"""

                    # Se ejecuta la consulta sql con el cursor y se obtienen todas las filas 
                    cursor.execute(sql)
                    entrenadores = cursor.fetchall()

                # Ocultamos la columna 0
                self.ui.tabla_entrenadores.hideColumn(0)

                # Validar la existencia de la tabla antes de configurar el número de filas
                if tabla is not None:
                    # Medimos la cantidad de datos de la tabla        
                    i = len(entrenadores)
                    tabla.setRowCount(i)

                    # Validamos si hay por lo menos un dato para que nos muestre los mismos en la tabla
                    if i > 0:
                        tablerow = 0
                        for entrenador in entrenadores:

                            # Añadir los elementos a la tabla
                            tabla.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(entrenador[0])))
                            tabla.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(entrenador[1])))
                            tabla.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(entrenador[2])))
                            tabla.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(entrenador[3])))
                            tabla.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(entrenador[4])))
                            tabla.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(entrenador[5])))
                            tabla.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(entrenador[6])))
                            tabla.setItem(tablerow, 7, QtWidgets.QTableWidgetItem(str(entrenador[7])))
                            tabla.setItem(tablerow, 8, QtWidgets.QTableWidgetItem(str(entrenador[8])))

                            # Configurar la celda de estado y cambiar el color 
                            estado_item = QtWidgets.QTableWidgetItem(str(entrenador[9]))
                            if entrenador[9].lower() == "inactivo":
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
                            
                            # Desactivar la edición de las celdas agregadas (excepto la primera columna ID)
                            for col in range(1, 10):
                                tabla.item(tablerow, col).setFlags(QtCore.Qt.ItemIsEnabled)

                            # Crear botón Editar y usar partial para pasar la fila correcta
                            boton_editar = QPushButton()
                            boton_editar.clicked.connect(partial(self.llenar_campos_editar_entrenador, tablerow))
                            boton_editar.setStyleSheet("""
                                QPushButton {
                                    image: url(:/iconos_principal/iconos/editar_tabla.png);
                                    width: 35px;
                                    height: 35px 
                                }""")

                            # Crear botón Eliminar y usar partial
                            boton_eliminar = QPushButton()
                            boton_eliminar.clicked.connect(partial(self.eliminar_entrenador, tablerow))
                            boton_eliminar.setStyleSheet("""
                                QPushButton {
                                    image: url(:/iconos_principal/iconos/borrar_tabla.png);
                                    width: 35px;
                                    height: 35px 
                                }""")


                            boton_estado.clicked.connect(partial(self.editar_estado_entrenador, tablerow))


                            # Crear un layout horizontal para contener los botones
                            widget_opciones = QWidget()
                            layout_opciones = QHBoxLayout()
                            layout_opciones.addWidget(boton_editar)
                            layout_opciones.addWidget(boton_eliminar)
                            layout_opciones.addWidget(boton_estado)
                            layout_opciones.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes
                            widget_opciones.setLayout(layout_opciones)

                            # Insertar el widget con los botones en la columna "Opciones"
                            self.ui.tabla_entrenadores.setCellWidget(tablerow, 10, widget_opciones)
                                   
                            tablerow += 1
                    else:
                        # Mostrar mensaje de éxito
                        mensaje = qtw.QMessageBox(self.main_logic)
                        mensaje.setWindowTitle("Éxito")
                        mensaje.setText(f"No existen entrenadores en el sistema")
                        mensaje.setIcon(qtw.QMessageBox.Warning)
                        aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
                        mensaje.exec_()
                
            except Exception as ex:
                print(ex)


    # FUNCIÓN PARA ELIMINAR ENTRENADOR DE LA BASE DE DATOS
    def eliminar_entrenador(self, tablerow):
     
        id_entrenador = self.ui.tabla_entrenadores.item(tablerow, 0).text()  
        nombre_entrenador = self.ui.tabla_entrenadores.item(tablerow, 2).text()  
        apellido_entrenador = self.ui.tabla_entrenadores.item(tablerow, 3).text()  

        # Concatenar nombre y apellido para mostrar en el mensaje
        nombre_completo = f"{nombre_entrenador} {apellido_entrenador}"

        mensaje = QMessageBox(self.main_logic)
        mensaje.setIcon(QMessageBox.Question)
        mensaje.setWindowTitle("Eliminar Entrenador")
        mensaje.setText(
            f"¿Estás seguro de que deseas eliminar al entrenador '{nombre_completo}'?\n\n"
            "Esta acción es irreversible y eliminará todos los datos relacionados con este entrenador en el sistema, "
            "incluyendo:\n"
            "- Asignaciones a clientes\n"
            "- Gastos asociados\n"
            "- Horarios de trabajo\n\n"
            "¿Deseas continuar con la eliminación?"
        )

        # Añadir botones "Sí" y "No" personalizados
        boton_si = mensaje.addButton("Sí", QMessageBox.YesRole)
        boton_no = mensaje.addButton("No", QMessageBox.NoRole)

        # Aplicar el estilo del mensaje sin agregar el botón "Aceptar"
        aplicar_estilo_mensaje(mensaje, agregar_boton_aceptar=False)

        # Mostrar el cuadro de diálogo y obtener la respuesta
        respuesta = mensaje.exec_()

        # Comprobar la respuesta
        if mensaje.clickedButton() == boton_si:
            try:
                with conexion.cursor() as cursor:
                    # Primero eliminamos las asignaciones de los entrenadores y clientes
                    sql_medidas = "DELETE FROM clientes_entrenadores WHERE id_entrenador = %s"
                    cursor.execute(sql_medidas, (id_entrenador,))

                    sql_horarios = "DELETE FROM horarios_entrenadores WHERE id_entrenador = %s"
                    cursor.execute(sql_horarios, (id_entrenador,))

                    sql_gastos = "DELETE FROM entrenadores_gastos WHERE id_entrenador = %s"
                    cursor.execute(sql_gastos, (id_entrenador,))
                    
                    # Luego eliminamos el entrenador
                    sql_cliente = "DELETE FROM entrenadores WHERE id = %s"
                    cursor.execute(sql_cliente, (id_entrenador,))
                    conexion.commit()

                mensaje = qtw.QMessageBox(self.main_logic)
                mensaje.setText(f"El entrenador '{nombre_entrenador}' ha sido eliminado correctamente.")
                mensaje.setIcon(qtw.QMessageBox.Information)
                aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
                mensaje.exec_()

                self.llenar_tabla_entrenadores()


            except Exception as e:
                mensaje = qtw.QMessageBox(self.main_logic)
                mensaje.setWindowTitle("Error")
                mensaje.setText(f"Error al eliminar el entrenador, revise que la conexión a la base de datos esté disponible")
                mensaje.setIcon(qtw.QMessageBox.Critical)
                aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
                mensaje.exec_()


    def editar_estado_entrenador(self, tablerow):
        # Obtener el ID y los nombres del cliente desde la tabla
        id_entrenador = self.ui.tabla_entrenadores.item(tablerow, 0).text() 
        nombre_entrenador = self.ui.tabla_entrenadores.item(tablerow, 2).text()
        apellido_entrenador = self.ui.tabla_entrenadores.item(tablerow, 3).text()  # Asumiendo que el apellido está en la columna 3
        estado_actual = self.ui.tabla_entrenadores.item(tablerow, 9).text()  # Columna de estado (verifica que sea la columna correcta)

        # Concatenar nombre y apellido para mostrar en el mensaje
        nombre_completo = f"{nombre_entrenador} {apellido_entrenador}"

        # Determinar el nuevo estado
        nuevo_estado = "Inactivo" if estado_actual == "Activo" else "Activo"
        accion = "desactivado" if estado_actual == "Activo" else "activado"

        try:
            # Cambiar el estado en la base de datos
            with conexion.cursor() as cursor:
                sql_cambiar_estado = "UPDATE entrenadores SET estado = %s WHERE id = %s"
                cursor.execute(sql_cambiar_estado, (nuevo_estado, id_entrenador))
                conexion.commit()

            # Recargar la tabla para actualizarla
            self.llenar_tabla_entrenadores()

            # Mostrar mensaje de éxito con el nombre del cliente
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Éxito")
            mensaje.setText(f"El entrenador '{nombre_completo}' ha sido {accion} correctamente.")
            mensaje.setIcon(qtw.QMessageBox.Information)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()

        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al cambiar el estado del entrenador, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()

    def llenar_campos_editar_entrenador(self, tablerow):
        
        # Activar el modo de edición
        self.modo_edicion = True

        self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_crear_entrenador)

        id_entrenador = self.ui.tabla_entrenadores.item(tablerow, 0).text()
        
        # Guardar el ID de la máquina para usarlo más tarde en la actualización
        self.entrenador_id_actual = id_entrenador

        # Obtener los demás datos desde la tabla
        cedula = self.ui.tabla_entrenadores.item(tablerow, 1).text()
        nombre = self.ui.tabla_entrenadores.item(tablerow, 2).text()
        apellidos = self.ui.tabla_entrenadores.item(tablerow, 3).text()
        direccion = self.ui.tabla_entrenadores.item(tablerow, 4).text()
        telefono = self.ui.tabla_entrenadores.item(tablerow, 5).text()
        correo = self.ui.tabla_entrenadores.item(tablerow, 6).text()
        especialidad = self.ui.tabla_entrenadores.item(tablerow, 7).text()
        fecha_contrato = self.ui.tabla_entrenadores.item(tablerow, 8).text()
        estado = self.ui.tabla_entrenadores.item(tablerow, 9).text()


        # Convertir la fecha de cadena a QDate
        formato_fecha = "yyyy-MM-dd"
        fecha_qdate = QDate.fromString(fecha_contrato, formato_fecha)

        # Cargar los datos actuales en los campos de edición de la máquina
        self.ui.txt_cedula_entrenador.setText(cedula)
        self.ui.txt_nombres_entrenador.setText(nombre)
        self.ui.txt_apellido_entrenador.setText(apellidos)
        self.ui.txt_direccion_entrenador.setText(direccion)
        self.ui.txt_telefono_entrenador.setText(telefono)
        self.ui.txt_correo_entrenador.setText(correo)
        self.ui.combo_especialidad_entrenador.setCurrentText(especialidad)
        self.ui.txt_fecha_contrato_entrenador.setDate(fecha_qdate)
        self.ui.combo_estado_entrenador.setCurrentText(estado)

        #Guarda el estado inicial de los campos de texto
        self.main_logic.guardar_estado_inicial()

        #*mostrar modo editar
        self.main_logic.mostrar_modo_editar()


    def editar_entrenador(self):

        # Validación de campos obligatorios
        campos_obligatorios = [
        (self.ui.txt_cedula_entrenador, "Número de cédula"),
        (self.ui.txt_nombres_entrenador, "Nombres"),
        (self.ui.txt_apellido_entrenador, "Apellidos"),
        (self.ui.txt_telefono_entrenador, "Teléfono"),
        ]

         # usamos la funcion de validaciones
        if not validar_campos_obligatorios(campos_obligatorios, self.main_logic):
            return  # Detener la ejecución si hay campos vacíos

        # Validar correo electrónico
        correo = self.ui.txt_correo_entrenador.text()
        if not validar_correo(correo, self.main_logic):
            return

        # Obtener los valores editados desde los campos
        cedula_editada = self.ui.txt_cedula_entrenador.text()
        nombres_editados = self.ui.txt_nombres_entrenador.text()
        apellidos_editados = self.ui.txt_apellido_entrenador.text()
        direccion_editada = self.ui.txt_direccion_entrenador.text()
        telefono_editado = self.ui.txt_telefono_entrenador.text()
        correo_editado = self.ui.txt_correo_entrenador.text()
        especialidad_editada = self.ui.combo_especialidad_entrenador.currentText()
        fecha_contrato_editada = self.ui.txt_fecha_contrato_entrenador.date().toString('yyyy-MM-dd')
        estado = self.ui.combo_estado_entrenador.currentText()

        nombre_completo = f"{nombres_editados} {apellidos_editados}"


        try:
            with conexion.cursor() as cursor:
                # Actualizar los datos del entrenador en la base de datos
                sql = """
                    UPDATE entrenadores
                    SET num_cedula = %s, nombres = %s, apellidos = %s, direccion = %s, num_telefono = %s, 
                        correo = %s, especialidad = %s, fecha_contratacion = %s, estado = %s
                    WHERE id = %s
                """
                cursor.execute(sql, (cedula_editada, nombres_editados, apellidos_editados, direccion_editada, telefono_editado, 
                                    correo_editado, especialidad_editada, fecha_contrato_editada, estado, self.entrenador_id_actual))
                conexion.commit()

                # Mostrar mensaje de éxito
                mensaje = qtw.QMessageBox(self.main_logic)
                mensaje.setText(f"El entrenador '{nombre_completo}' ha sido actualizado correctamente.")
                mensaje.setIcon(qtw.QMessageBox.Information)
                aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
                mensaje.exec_()

                # Regresar a la vista principal
                self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_entrenadores)

                # Recargar los datos en la tabla
                self.llenar_tabla_entrenadores()

        except Exception as e:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Error al actualizar el entrenador, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()

    def pagina_asignaciones(self):
        # Cambiar a la página de membresias
        self.ui.stackedWidget.setCurrentWidget(self.ui.pagina_asignar_entrenador_cliente)

        self.llenar_tabla_asignaciones()
        self.llenar_combo_clientes_asignar()
        self.llenar_combo_entrenador_asignar()

    def llenar_combo_clientes_asignar(self):
        try:
            with conexion.cursor() as cursor:
                # Obtener todos los clientes
                sql = "SELECT id, nombres, apellidos FROM clientes WHERE estado = 'Activo'"
                cursor.execute(sql)
                clientes = cursor.fetchall()

                # Desactivar las señales mientras se llena el ComboBox
                self.ui.combo_usuario_asignar.blockSignals(True)

                # Verificar si se encontraron clientes
                if not clientes:
                    # Si no hay clientes, agregar "Sin datos" y mostrar un mensaje de advertencia
                    mensaje = qtw.QMessageBox(self.main_logic)
                    mensaje.setText("No se encontraron clientes en el sistema.")
                    mensaje.setIcon(qtw.QMessageBox.Warning)
                    aplicar_estilo_mensaje(mensaje)
                    mensaje.exec_()

                # Llenar el ComboBox con los nombres, apellidos e ID de los clientes
                self.ui.combo_usuario_asignar.clear()
                for cliente in clientes:
                    id_cliente = cliente[0]
                    nombre_completo = f"{cliente[1]} {cliente[2]}"
                    # Agregar al ComboBox el nombre, pero guardar el ID único
                    self.ui.combo_usuario_asignar.addItem(nombre_completo, id_cliente)

                # Reactivar las señales después de llenar el ComboBox
                self.ui.combo_usuario_asignar.blockSignals(False)

        except Exception as ex:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"No se pudo cargar el listado de clientes, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()

    
    def llenar_combo_entrenador_asignar(self):
        try:
            with conexion.cursor() as cursor:
                # Obtener todos los clientes
                sql = "SELECT id, nombres, apellidos, especialidad FROM entrenadores WHERE estado = 'Activo'"
                cursor.execute(sql)
                entrenadores = cursor.fetchall()

                # Desactivar las señales mientras se llena el ComboBox
                self.ui.combo_entrenador_asignar.blockSignals(True)

                if not entrenadores:
                    # Si no hay clientes, agregar "Sin datos" y mostrar un mensaje de advertencia
                    mensaje = qtw.QMessageBox(self.main_logic)
                    mensaje.setText("No se encontraron entrenadores en el sistema.")
                    mensaje.setIcon(qtw.QMessageBox.Warning)
                    aplicar_estilo_mensaje(mensaje)
                    mensaje.exec_()

                # Llenar el ComboBox con los nombres, apellidos e ID de los clientes
                self.ui.combo_entrenador_asignar.clear()
                for entrenador in entrenadores:
                    id_entrenador = entrenador[0]
                    nombre = entrenador[1]
                    primer_apellido = entrenador[2].split()[0]  # Tomar solo el primer apellido
                    especialidad = entrenador[3]

                    # Crear la cadena que incluye el nombre completo y la especialidad
                    texto_combo = f"{nombre} {primer_apellido} - {especialidad}"

                    # Agregar al ComboBox el nombre, pero guardar el ID único
                    self.ui.combo_entrenador_asignar.addItem(texto_combo, id_entrenador)

                # Reactivar las señales después de llenar el ComboBox
                self.ui.combo_entrenador_asignar.blockSignals(False)

        except Exception as ex:
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"No se pudo cargar el listado de entrenadores, revise que la conexión a la base de datos esté disponible")
            mensaje.setIcon(qtw.QMessageBox.Critical)
            aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
            mensaje.exec_()

    def asignar_cliente_entrenador(self):
        # Combo box
        clientes = self.ui.combo_usuario_asignar.currentData()
        entrenadores = self.ui.combo_entrenador_asignar.currentData()

        try:
            with conexion.cursor() as cursor:
                # Inserta los datos en la tabla entrenadores
                sql = "INSERT INTO clientes_entrenadores (id_cliente, id_entrenador) VALUES (%s, %s)"
                cursor.execute(sql, (clientes, entrenadores))
                conexion.commit()


            self.ui.combo_usuario_asignar.setCurrentIndex(0)  # Esto selecciona la primera opción del combo box ("Seleccione")
            self.ui.combo_entrenador_asignar.setCurrentIndex(0)

            # Mensaje de éxito
            mensaje = qtw.QMessageBox(self.main_logic)
            mensaje.setWindowTitle("Éxito")
            mensaje.setText("Se ha asignado un entrenador correctamente")
            mensaje.setIcon(qtw.QMessageBox.Information)
            aplicar_estilo_mensaje(mensaje)
            mensaje.exec_()

            # Llenar tabla al insertar una nueva relación
            self.llenar_tabla_asignaciones()
        

        except Exception as ex:
            # Verificar si el error es de entrada duplicada
            if "Duplicate entry" in str(ex):
                mensaje = qtw.QMessageBox(self.main_logic)
                mensaje.setText("La asignación ya existe en el sistema.")
                mensaje.setIcon(qtw.QMessageBox.Warning)
                aplicar_estilo_mensaje(mensaje) 
                mensaje.exec_()

            else:
                mensaje = qtw.QMessageBox(self.main_logic)
                mensaje.setWindowTitle("Error")
                mensaje.setText(f"Fallo al almacenar los datos, revise que la conexión a la base de datos esté disponible.")
                mensaje.setIcon(qtw.QMessageBox.Critical)
                aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
                mensaje.exec_()
    

    def llenar_tabla_asignaciones(self):
        tabla = self.ui.tabla_clientes_entrenadores  # Asegúrate de que este sea el nombre correcto de tu tabla
        self.ui.tabla_clientes_entrenadores.verticalHeader().setVisible(False)

        try:
            with conexion.cursor() as cursor:
                # Se realiza la consulta a la base de datos
                sql = """SELECT clientes.id, entrenadores.id, clientes.num_cedula, clientes.nombres, clientes.apellidos, entrenadores.num_cedula, entrenadores.nombres, entrenadores.apellidos, 
                        entrenadores.especialidad FROM clientes JOIN clientes_entrenadores ON clientes.id = clientes_entrenadores.id_cliente 
                        JOIN entrenadores ON clientes_entrenadores.id_entrenador = entrenadores.id"""
                
                # Se ejecuta la consulta sql con el cursor y se obtienen todas las filas 
                cursor.execute(sql)
                clientes_entrenadores = cursor.fetchall()

            # Ocultamos la columna 0 y 1
            self.ui.tabla_clientes_entrenadores.hideColumn(0)
            self.ui.tabla_clientes_entrenadores.hideColumn(1)

            # Validar la existencia de la tabla antes de configurar el número de filas
            if tabla is not None:
                # Medimos la cantidad de datos de la tabla        
                i = len(clientes_entrenadores)
                tabla.setRowCount(i)

                # Validamos si hay por lo menos un dato para que nos muestre los mismos en la tabla
                if i > 0:
                    tablerow = 0
                    for usuario in clientes_entrenadores:
                        # Asegúrate de que los índices estén correctos según la estructura de tus datos
                        tabla.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(usuario[0])))
                        tabla.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(usuario[1])))
                        tabla.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(usuario[2])))
                        tabla.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(f"{usuario[3]} {usuario[4]}")))
                        tabla.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(usuario[5])))
                        tabla.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(f"{usuario[6]} {usuario[7]}")))
                        tabla.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(usuario[8])))

                        # Desactivar la edición de las celdas agregadas (excepto la primera columna ID)
                        for col in range(2, 7):
                            tabla.item(tablerow, col).setFlags(QtCore.Qt.ItemIsEnabled)
                                           

                        boton_eliminar = QPushButton()
                        boton_eliminar.setStyleSheet("""
                            QPushButton {
                                image: url(:/iconos_principal/iconos/borrar_tabla.png);
                                width: 35px;
                                height: 35px 
                            }""")


                        boton_eliminar.clicked.connect(partial(self.eliminar_asignacion, tablerow))


                        # Crear un layout horizontal para contener los botones
                        widget_opciones = QWidget()
                        layout_opciones = QHBoxLayout()
                        layout_opciones.addWidget(boton_eliminar)
                        layout_opciones.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes
                        widget_opciones.setLayout(layout_opciones)

                        # Insertar el widget con los botones en la columna "Opciones"
                        self.ui.tabla_clientes_entrenadores.setCellWidget(tablerow, 7, widget_opciones)

                        tablerow += 1
                else:

                    mensaje = qtw.QMessageBox(self.main_logic)
                    mensaje.setText("No existen asignaciones en el sistema.")
                    mensaje.setIcon(qtw.QMessageBox.Warning)
                    aplicar_estilo_mensaje(mensaje) 
                    mensaje.exec_()

        except Exception as ex:
            print(ex)


    def eliminar_asignacion(self, tablerow):
        # Obtener el ID y el nombre del cliente de la fila seleccionada
        id_cliente = self.ui.tabla_clientes_entrenadores.item(tablerow, 0).text() 
        id_entrenador = self.ui.tabla_clientes_entrenadores.item(tablerow, 1).text()  
        nombre_cliente = self.ui.tabla_clientes_entrenadores.item(tablerow, 3).text()
        nombre_entrenador = self.ui.tabla_clientes_entrenadores.item(tablerow, 5).text()
       

        # Crear el cuadro de diálogo de confirmación
        mensaje = QMessageBox(self.main_logic)
        mensaje.setIcon(QMessageBox.Question)
        mensaje.setWindowTitle("Eliminar asignación")
        mensaje.setText(
            f"¿Estás seguro de que deseas eliminar la asignación de cliente '{nombre_cliente}' con entrenador '{nombre_entrenador}'?"
        )

        # Añadir botones "Sí" y "No" personalizados
        boton_si = mensaje.addButton("Sí", QMessageBox.YesRole)
        boton_no = mensaje.addButton("No", QMessageBox.NoRole)

        # Aplicar el estilo del mensaje sin agregar el botón "Aceptar"
        aplicar_estilo_mensaje(mensaje, agregar_boton_aceptar=False)

        # Mostrar el cuadro de diálogo y obtener la respuesta
        respuesta = mensaje.exec_()

        # Comprobar la respuesta
        if mensaje.clickedButton() == boton_si:
            try:
                # Realizar la consulta para eliminar el cliente de la base de datos
                with conexion.cursor() as cursor:
                    # Primero eliminamos las medidas antropométricas asociadas al cliente
                    sql_medidas = "DELETE FROM clientes_entrenadores WHERE id_cliente = %s AND id_entrenador = %s"
                    cursor.execute(sql_medidas, (id_cliente, id_entrenador))

                    conexion.commit()


                mensaje = qtw.QMessageBox(self.main_logic)
                mensaje.setText("La asignación ha sido eliminada.")
                mensaje.setIcon(qtw.QMessageBox.Information)
                aplicar_estilo_mensaje(mensaje) 
                mensaje.exec_()

                # Recargar la tabla para actualizarla
                self.llenar_tabla_asignaciones()

            except Exception as e:
                mensaje = qtw.QMessageBox(self.main_logic)
                mensaje.setWindowTitle("Error")
                mensaje.setText(f"Error al eliminar la asignación, revise que la conexión a la base de datos esté disponible")
                mensaje.setIcon(qtw.QMessageBox.Critical)
                aplicar_estilo_mensaje(mensaje)  # Aplicar el estilo personalizado
                mensaje.exec_()
            
    def activar_boton_usuarios(self):
        self.main_logic.reset_button_styles(self.ui.bt_usuarios)
        # Otra lógica de activación para el botón