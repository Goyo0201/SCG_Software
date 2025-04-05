import unittest
import colorama
from colorama import Fore, Style

# Inicializa colorama
colorama.init()

class CustomTextTestRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return CustomTestResult(self.stream, self.descriptions, self.verbosity)

class CustomTestResult(unittest.TextTestResult):
    def startTest(self, test):
        super().startTest(test)
        print(f"{Fore.CYAN}Iniciando prueba: {test._testMethodName}{Style.RESET_ALL}")

    def addSuccess(self, test):
        super().addSuccess(test)
        print(f"{Fore.GREEN}✔ Prueba exitosa: {test._testMethodName}{Style.RESET_ALL}")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        print(f"{Fore.RED}✖ Prueba fallida: {test._testMethodName}{Style.RESET_ALL}")

    def addError(self, test, err):
        super().addError(test, err)
        print(f"{Fore.YELLOW}⚠ Error en la prueba: {test._testMethodName}{Style.RESET_ALL}")

if __name__ == "__main__":
    # Cargar todos los tests desde el módulo de pruebas
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests')  # Asegúrate de que 'tests' es el directorio de pruebas

    # Ejecutar el runner personalizado
    runner = CustomTextTestRunner(verbosity=2)
    runner.run(test_suite)
