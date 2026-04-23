"""
Script principal del proyecto

En este script se importaran los modulos de la GUI, de la lectura/limpieza/validacion, del calculo de razones financieras
y de la generacion de dashboards. Este script inicializa y corre la aplicion completa.

"""

from gui import ProgramaGui

# Test data
test_results = {
    "liq_circulante": 2.5,
    "liq_disponibilidad": 0.8,
    "liq_exigibilidad": 0.15,
    "liq_reserva_tec": 0.54,
    "sya_activos_pasivos": 0.34,
    "sya_depurada": 0.34,
    "sya_pasivo_capital": 0.34,
    "sya_reserva_capital": 0.34,
    "suf_costo_operacion": 0.34,
    "suf_costo_adquisicion": 0.34,
    "suf_costo_siniestralidad": 0.34,
    "suf_indice_combinado": 0.34,
    "suf_de_la_prima": 0.34,
    "rea_prima_cedida": 0.34,
    "rea_prima_retenida": 0.34,
    "rea_comision_reaseguro": 0.34,
    "ren_utilidad_capital": 0.34,
    "ren_utilidad_patrimonio": 0.34,
    "ren_utilidad_prima": 0.34,
}

if __name__ == "__main__":
    app = ProgramaGui(results_dict=test_results)
    app.welcome_window()
    
    # After app closes, you can access the paths:
    bg_path, er_path = app.get_paths()
    print(f"Balance General path: {bg_path}")
    print(f"Estado de Resultados path: {er_path}")

