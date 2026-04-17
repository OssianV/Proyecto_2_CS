"""
Script principal del proyecto

En este script se importaran los modulos de la GUI, de la lectura/limpieza/validacion, del calculo de razones financieras
y de la generacion de dashboards. Este script inicializa y corre la aplicion completa.

"""

from gui import ProgramaGui

# Test data
test_results = {
    "Liquidity Ratio": 2.5,
    "Debt-to-Equity": 0.8,
    "ROA": 0.15,
}

if __name__ == "__main__":
    app = ProgramaGui(results_dict=test_results)
    app.welcome_window()
    
    # After app closes, you can access the paths:
    bg_path, er_path = app.get_paths()
    print(f"Balance General path: {bg_path}")
    print(f"Estado de Resultados path: {er_path}")