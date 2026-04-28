"""
Script principal del proyecto

En este script se importaran los modulos de la GUI, de la lectura/limpieza/validacion, del calculo de razones financieras
y de la generacion de dashboards. Este script inicializa y corre la aplicion completa.

"""

from gui import ProgramaGui

if __name__ == "__main__":
    app = ProgramaGui(results_dict=None)
    app.welcome_window()
