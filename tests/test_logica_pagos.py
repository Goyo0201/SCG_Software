import sys
import os
import unittest
from unittest.mock import ANY, MagicMock, patch
from datetime import datetime, date

# Añadir el directorio raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar la clase LogicaPagos
from CapaLogica.logica_pagos import LogicaPagos

class TestLogicaPagos(unittest.TestCase):

    def setUp(self):
        # Mockear la interfaz gráfica y la lógica principal
        self.mock_ui = MagicMock()
        self.mock_main_logic = MagicMock()
        self.mock_main_logic.reset_button_styles = MagicMock()
        self.logica_pagos = LogicaPagos(self.mock_ui, self.mock_main_logic)

        # Configuración de los mocks de UI para los pagos
        self.logica_pagos.ui.txt_fecha_inicio_factura.text.return_value = "2024-11-21"
        self.logica_pagos.ui.txt_fecha_fin_factura.text.return_value = "2024-11-24"
        self.logica_pagos.ui.txt_numero_factura.text.return_value = "1006"
        self.logica_pagos.ui.txt_nombre_cliente_factura.text.return_value = "Juan Perez"
        self.logica_pagos.ui.txt_cedula_factura.text.return_value = "12345678901"
        self.logica_pagos.ui.txt_direccion_cliente_factura.text.return_value = "Calle Falsa 123"
        self.logica_pagos.ui.txt_telefono_factura.text.return_value = "1234567890"
        self.logica_pagos.ui.spin_cantidad.value.return_value = 1
        self.logica_pagos.ui.combo_membresia.currentText.return_value = "Membresía Mensual"
        self.logica_pagos.ui.txt_valor_unitario.text.return_value = "50.0"
        self.logica_pagos.ui.txt_valor_total.text.return_value = "50.0"
        self.logica_pagos.ui.txt_observaciones.toPlainText.return_value = "Sin observaciones"
        self.logica_pagos.ui.txt_subtotal.text.return_value = "50.0"
        self.logica_pagos.ui.txt_porcentaje_recibo.text.return_value = "10.0"
        self.logica_pagos.ui.txt_total_full.text.return_value = "45.0"
        self.logica_pagos.ui.combo_clientes_pagos.currentData.return_value = 11
        self.logica_pagos.ui.combo_membresia.currentData.return_value = 5

    @patch('CapaLogica.logica_pagos.conexion')
    @patch('CapaLogica.Validaciones.QMessageBox')
    @patch('CapaLogica.logica_pagos.qtw.QMessageBox')
    def test_crear_recibo_exitoso(self, mock_qmessagebox_logica_pagos, mock_qmessagebox_validaciones, mock_conexion):
        """Prueba que la creación del recibo se realice correctamente con datos válidos"""

        # Configuración del mock del cursor de la conexión
        mock_cursor = mock_conexion.cursor.return_value.__enter__.return_value
        mock_cursor.execute.return_value = None
        mock_cursor.lastrowid = 1  # Simular generación de un ID para el recibo
        mock_conexion.commit.return_value = None

        # Simular la respuesta del QMessageBox para que se seleccione reemplazar la membresía
        mock_qmessagebox_logica_pagos.exec_.return_value = 0  # Simular el botón "Sí" presionado
        mock_qmessagebox_logica_pagos.clickedButton.return_value = MagicMock()

        # Simular que el cliente ya tiene una membresía activa
        mock_cursor.fetchone.side_effect = [
            (11, 'Membresía Mensual', date(2024, 11, 1), date(2024, 11, 15)),  # Devuelve datos válidos en lugar de cadenas
            None  # Simular que después de insertar, la consulta confirma que se ha insertado correctamente
        ]

        resultado = self.logica_pagos.crear_recibo()

        # Verificación de que el resultado sea True
        self.assertTrue(resultado, "El recibo debería crearse exitosamente")

        # Verificar que el commit fue llamado al menos una vez (ya que puede ser llamado más de una vez)
        self.assertGreaterEqual(mock_conexion.commit.call_count, 1, "Se esperaba al menos una llamada a commit()")

    # Validaciones de campos
    @patch('CapaLogica.logica_pagos.conexion')
    @patch('CapaLogica.Validaciones.QMessageBox')
    @patch('CapaLogica.logica_pagos.qtw.QMessageBox')
    def test_crear_recibo_faltan_campos_obligatorios(self, mock_qmessagebox_logica_pagos, mock_qmessagebox_validaciones, mock_conexion):
        self.logica_pagos.ui.txt_nombre_cliente_factura.text.return_value = ""
        resultado = self.logica_pagos.crear_recibo()
        self.assertFalse(resultado, "No debería crear el recibo si faltan campos obligatorios")

    @patch('CapaLogica.logica_pagos.conexion')
    @patch('CapaLogica.Validaciones.QMessageBox')
    @patch('CapaLogica.logica_pagos.qtw.QMessageBox')
    def test_crear_recibo_manejo_error_bd(self, mock_qmessagebox_logica_pagos, mock_qmessagebox_validaciones, mock_conexion):
        mock_cursor = mock_conexion.cursor.return_value.__enter__.return_value
        mock_cursor.execute.side_effect = Exception("Error en la base de datos")
        resultado = self.logica_pagos.crear_recibo()
        self.assertFalse(resultado, "La función debería manejar el error de base de datos y retornar False")




        

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLogicaPagos)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
