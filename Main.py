
from PyQt5 import QtWidgets as qtw
from CapaLogica.logica_login import Login
from CapaPresentacion.Menú_principal import Ui_menu_principal  # Importación de Ui_menu_principal

class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_menu_principal()
        self.ui.setupUi(self)

# Ejecución principal
if __name__ == "__main__":
    app = qtw.QApplication([])
    widget = Login()  # Asegurándote de que Login es una ventana funcional y principal
    widget.show()
    app.exec_()
