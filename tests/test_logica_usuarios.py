import sys
import os
from unittest import mock

# Añadir el directorio raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import ANY, MagicMock, call, patch
from CapaLogica.logica_usuarios import LogicaUsuarios

class TestLogicaUsuarios(unittest.TestCase):

    def setUp(self):
        self.mock_ui = MagicMock()
        self.mock_main_logic = MagicMock()
        self.mock_main_logic.reset_button_styles = MagicMock()
        self.logica_usuarios = LogicaUsuarios(self.mock_ui, self.mock_main_logic)

        # Configuración de los mocks de UI para clientes
        self.logica_usuarios.ui.txt_cedula_cliente.text.return_value = "12345678"
        self.logica_usuarios.ui.txt_nombres_cliente.text.return_value = "Juan"
        self.logica_usuarios.ui.txt_apellido_cliente.text.return_value = "Pérez"
        self.logica_usuarios.ui.txt_telefono_cliente.text.return_value = "5551234"
        self.logica_usuarios.ui.txt_fecha_registro_cliente.text.return_value = "2023-01-01"
        self.logica_usuarios.ui.combo_estado_cliente.currentText.return_value = "Activo"
        self.logica_usuarios.ui.txt_correo_cliente.text.return_value = "juan.perez@example.com"
        self.logica_usuarios.ui.txt_peso.text.return_value = "70"
        self.logica_usuarios.ui.txt_altura.text.return_value = "175"
        self.logica_usuarios.ui.txt_fecha_nacimiento_cliente.text.return_value = "1990-05-15"
        self.logica_usuarios.ui.txt_direccion_cliente.text.return_value = "Calle 123"
        self.logica_usuarios.ui.txt_medida_pecho.text.return_value = "95"
        self.logica_usuarios.ui.txt_medida_brazos.text.return_value = "30"
        self.logica_usuarios.ui.txt_medida_muslos.text.return_value = "60"
        self.logica_usuarios.ui.txt_medida_gluteos.text.return_value = "90"
        self.logica_usuarios.ui.txt_medida_pantorrillas.text.return_value = "40"
        self.logica_usuarios.ui.txt_medida_hombros.text.return_value = "50"

        # Configuración de los mocks de UI para entrenadores
        self.logica_usuarios.ui.txt_cedula_entrenador.text.return_value = "87654321"
        self.logica_usuarios.ui.txt_nombres_entrenador.text.return_value = "Carlos"
        self.logica_usuarios.ui.txt_apellido_entrenador.text.return_value = "Gomez"
        self.logica_usuarios.ui.txt_telefono_entrenador.text.return_value = "1234567"
        self.logica_usuarios.ui.txt_direccion_entrenador.text.return_value = "Avenida Siempre Viva"
        self.logica_usuarios.ui.txt_fecha_contrato_entrenador.text.return_value = "2023-01-01"
        self.logica_usuarios.ui.txt_correo_entrenador.text.return_value = "carlos.gomez@example.com"
        self.logica_usuarios.ui.combo_especialidad_entrenador.currentText.return_value = "Pesas"
        self.logica_usuarios.ui.combo_estado_entrenador.currentText.return_value = "Activo"

        # Configuración de la tabla para eliminar
        self.logica_usuarios.ui.tabla_clientes.item.return_value.text.side_effect = ["1", "Juan", "Pérez"]

    # Validaciones de campos
    @patch('CapaLogica.logica_usuarios.conexion')
    @patch('CapaLogica.Validaciones.QMessageBox')
    @patch('CapaLogica.logica_usuarios.qtw.QMessageBox')
    def test_crear_cliente_faltan_campos_obligatorios(self, mock_qmessagebox_logica_usuarios, mock_qmessagebox_validaciones, mock_conexion):
        self.logica_usuarios.ui.txt_nombres_cliente.text.return_value = ""
        resultado = self.logica_usuarios.crear_cliente()
        self.assertFalse(resultado, "No debería crear el cliente si faltan campos obligatorios")

    @patch('CapaLogica.logica_usuarios.conexion')
    @patch('CapaLogica.Validaciones.QMessageBox')
    @patch('CapaLogica.logica_usuarios.qtw.QMessageBox')
    def test_crear_cliente_con_correo_invalido(self, mock_qmessagebox_logica_usuarios, mock_qmessagebox_validaciones, mock_conexion):
        self.logica_usuarios.ui.txt_correo_cliente.text.return_value = "correo-invalido"
        resultado = self.logica_usuarios.crear_cliente()
        self.assertFalse(resultado, "No debería crear el cliente si el correo es inválido")

    @patch('CapaLogica.logica_usuarios.conexion')
    @patch('CapaLogica.Validaciones.QMessageBox')
    @patch('CapaLogica.logica_usuarios.qtw.QMessageBox')
    def test_crear_cliente_manejo_error_bd(self, mock_qmessagebox_logica_usuarios, mock_qmessagebox_validaciones, mock_conexion):
        mock_cursor = mock_conexion.cursor.return_value.__enter__.return_value
        mock_cursor.execute.side_effect = Exception("Error en la base de datos")
        resultado = self.logica_usuarios.crear_cliente()
        self.assertFalse(resultado, "La función debería manejar el error de base de datos y retornar False")

    # Crear cliente
    @patch('CapaLogica.logica_usuarios.conexion')
    @patch('CapaLogica.Validaciones.QMessageBox')
    @patch('CapaLogica.logica_usuarios.qtw.QMessageBox')
    def test_crear_cliente_exitoso(self, mock_qmessagebox_logica_usuarios, mock_qmessagebox_validaciones, mock_conexion):
        """Prueba que la creación del cliente se realice correctamente con datos válidos"""

        # Configuración del mock del cursor de la conexión
        mock_cursor = mock_conexion.cursor.return_value.__enter__.return_value
        mock_cursor.execute.return_value = None
        mock_cursor.lastrowid = 1
        mock_conexion.commit.return_value = None

        # Ejecutar el método
        print("Ejecutando prueba de creación de cliente exitoso...")
        resultado = self.logica_usuarios.crear_cliente()
        print(f"Resultado de crear_cliente: {resultado}")
        
        # Verificación de que el resultado sea True
        self.assertTrue(resultado, "El cliente debería crearse exitosamente")

        # Verificar que el commit fue llamado una vez
        mock_conexion.commit.assert_called_once()

    # Editar cliente
    @patch('CapaLogica.logica_usuarios.conexion')
    @patch('CapaLogica.Validaciones.QMessageBox')
    @patch('CapaLogica.logica_usuarios.qtw.QMessageBox')
    def test_editar_cliente_exitoso(self, mock_qmessagebox_logica_usuarios, mock_qmessagebox_validaciones, mock_conexion):
        """Prueba que la edición del cliente se realice correctamente con datos válidos"""

        # Configuración del mock del cursor de la conexión
        mock_cursor = mock_conexion.cursor.return_value.__enter__.return_value
        mock_cursor.execute.return_value = None
        mock_conexion.commit.return_value = None

        # Establecer el ID del cliente actual
        self.logica_usuarios.cliente_id_actual = 1

        # Ejecutar el método
        print("Ejecutando prueba de edición de cliente...")
        resultado = self.logica_usuarios.editar_cliente()
        print(f"Resultado de editar_cliente: {resultado}")
        
        # Verificar que el commit fue llamado una vez
        mock_conexion.commit.assert_called_once()

    # Crear entrenador
    @patch('CapaLogica.logica_usuarios.conexion')
    @patch('CapaLogica.Validaciones.QMessageBox')
    @patch('CapaLogica.logica_usuarios.qtw.QMessageBox')
    def test_crear_entrenador_exitoso(self, mock_qmessagebox_logica_usuarios, mock_qmessagebox_validaciones, mock_conexion):
        """Prueba que la creación del entrenador se realice correctamente con datos válidos"""

        # Configuración del mock del cursor de la conexión
        mock_cursor = mock_conexion.cursor.return_value.__enter__.return_value
        mock_cursor.execute.return_value = None
        mock_cursor.lastrowid = 1
        mock_conexion.commit.return_value = None

        # Ejecutar el método
        print("Ejecutando prueba de creación de entrenador exitoso...")
        resultado = self.logica_usuarios.crear_entrenador()
        print(f"Resultado de crear_entrenador: {resultado}")
        
        # Verificación de que el resultado sea True
        self.assertTrue(resultado, "El entrenador debería crearse exitosamente")

        # Verificar que el commit fue llamado una vez
        mock_conexion.commit.assert_called_once()

    # Editar entrenador
    @patch('CapaLogica.logica_usuarios.conexion')
    @patch('CapaLogica.Validaciones.QMessageBox')
    @patch('CapaLogica.logica_usuarios.qtw.QMessageBox')
    def test_editar_entrenador_exitoso(self, mock_qmessagebox_logica_usuarios, mock_qmessagebox_validaciones, mock_conexion):
        """Prueba que la edición del entrenador se realice correctamente con datos válidos"""

        # Configuración del mock del cursor de la conexión
        mock_cursor = mock_conexion.cursor.return_value.__enter__.return_value
        mock_cursor.execute.return_value = None
        mock_conexion.commit.return_value = None

        # Establecer el ID del entrenador actual
        self.logica_usuarios.entrenador_id_actual = 1

        # Ejecutar el método
        print("Ejecutando prueba de edición de entrenador...")
        resultado = self.logica_usuarios.editar_entrenador()
        print(f"Resultado de editar_entrenador: {resultado}")
        
        # Verificar que el commit fue llamado una vez
        mock_conexion.commit.assert_called_once()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLogicaUsuarios)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
