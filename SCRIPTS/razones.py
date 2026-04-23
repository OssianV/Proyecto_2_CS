def calcular_modulo_razones(datos_entrada):
    """
    Motor principal de cálculo de razones financieras.
    INPUT:  Diccionario con nombres exactos del Excel (ej. 'Reserva_de_Capital')
    OUTPUT: Diccionario con alias de las razones (ej. {'liq_circulante': 0.34})
    """
    # 1. Limpieza de valores (quita $, comas y convierte a float)
    d = {k: _limpiar_valor(v) for k, v in datos_entrada.items()}
    
    # 2. Pre-procesamiento: Sumar cuentas para obtener totales que no vienen en el Excel
    d = _preparar_totales(d)
    
    r = {}

    # --- CATEGORÍA: LIQUIDEZ ---
    r["liq_circulante"] = _div(d.get("Total_Activo_Circulante"), d.get("Total_Pasivo_Circulante"))
    r["liq_disponibilidad"] = _div(d.get("Activo_Disponible"), d.get("Pasivo_Exigible"))
    r["liq_exigibilidad"] = _div(d.get("Total_Activo_Circulante"), d.get("Pasivo_Exigible"))
    r["liq_reserva_tec"] = _div(d.get("Total_Activo_Circulante"), d.get("Reservas_Tecnicas"))

    # --- CATEGORÍA: SOLVENCIA Y APALANCAMIENTO ---
    r["sya_activos_pasivos"] = _div(d.get("Activos_Totales"), d.get("Pasivos_Totales"))
    
    # Solvencia Depurada: (AT - AF) / (PT - Reservas Específicas)
    num_sol = d.get("Activos_Totales", 0.0) - d.get("Activo_Fijo", 0.0)
    den_sol = (d.get("Pasivos_Totales", 0.0) - 
               d.get("Reserva_de_Prevision", 0.0) - 
               d.get("Reserva_para_Riesgos_en_Curso", 0.0) - 
               d.get("Reserva_para_Obligaciones_Pendientes_de_Cumplimiento", 0.0))
    r["sya_depurada"] = _div(num_sol, den_sol)
    
    r["sya_pasivo_capital"] = _div(d.get("Pasivo_Total"), d.get("Capital_Contable"))
    r["sya_reserva_capital"] = _div(d.get("Reservas_Tecnicas"), d.get("Capital_Contable"))

    # --- CATEGORÍA: SUFICIENCIA DE LA PRIMA ---
    r["suf_costo_operacion"] = _div(d.get("Costo_Medio_de_Operacion"), d.get("Prima_Emitida"))
    r["suf_costo_adquisicion"] = _div(d.get("Costo_Medio_de_Adquisicion"), d.get("Prima_Emitida"))
    r["suf_costo_siniestralidad"] = _div(d.get("Costo_Medio_de_Siniestralidad"), d.get("Prima_Emitida"))
    
    costos_totales = (d.get("Costo_Medio_de_Operacion", 0.0) + 
                      d.get("Costo_Medio_de_Adquisicion", 0.0) + 
                      d.get("Costo_Medio_de_Siniestralidad", 0.0))
    r["suf_indice_combinado"] = _div(costos_totales, d.get("Prima_Emitida"))
    r["suf_de_la_prima"] = _div(d.get("Suficiencia_de_la_Prima"), d.get("Prima_Emitida"))

    # --- CATEGORÍA: REASEGURO ---
    r["rea_prima_cedida"] = _div(d.get("Prima_Cedida"), d.get("Prima_Emitida"))
    r["rea_prima_retenida"] = _div(d.get("Prima_Retenida"), d.get("Prima_Emitida"))
    r["rea_comision_reaseguro"] = _div(d.get("Comisiones_del_Reaseguro_Cedido"), d.get("Prima_Cedida"))

    # --- CATEGORÍA: RENTABILIDAD ---
    r["ren_utilidad_capital"] = _div(d.get("Utilidad_Neta"), d.get("Capital_Contable"))
    patrimonio_base = d.get("Capital_Pagado", 0.0) + d.get("Reserva_de_Capital", 0.0)
    r["ren_utilidad_patrimonio"] = _div(d.get("Utilidad_Neta"), patrimonio_base)
    r["ren_utilidad_prima"] = _div(d.get("Utilidad_Neta"), d.get("Prima_Emitida"))

    return r

def _preparar_totales(d):
    """
    Suma las cuentas individuales para obtener los totales necesarios.
    """
    # 1. Total Activo Circulante = Caja + Bancos + Deudores + Reaseguradores
    caja_y_bancos = d.get("Caja", 0.0) + d.get("Bancos", 0.0) + d.get("Disponibilidades", 0.0)
    deudores = d.get("Deudores", 0.0) + d.get("Deudores_por_Primas", 0.0)
    reaseguradores = d.get("Reaseguradores", 0.0) + d.get("Instituciones_de_Seguros_y_Fianzas", 0.0)
    d["Total_Activo_Circulante"] = caja_y_bancos + deudores + reaseguradores

    # 2. Total Pasivo Circulante = Caja + Bancos + Inversiones (según requerimiento)
    inversiones_pasivo = d.get("Inversiones", 0.0) + d.get("Valores_y_Operaciones_con_Productos_Derivados", 0.0)
    d["Total_Pasivo_Circulante"] = caja_y_bancos + inversiones_pasivo

    # 3. Activos Totales = Circulante + Inversiones + Otros Activos
    d["Activos_Totales"] = (d["Total_Activo_Circulante"] + d.get("Inversiones", 0.0) + 
                            d.get("Inversiones_Permanentes", 0.0) + d.get("Otros_Activos", 0.0))
    
    # 4. Pasivos Totales = Reservas Técnicas + Otras Cuentas de Pasivo
    d["Pasivos_Totales"] = (d.get("Reservas_Tecnicas", 0.0) + d.get("Acreedores", 0.0) + 
                            d.get("Reaseguradores_Pasivo", 0.0) + d.get("Otros_Pasivos", 0.0))
    
    return d

def _div(n, d):
    """División segura con redondeo a 4 decimales."""
    try:
        num, den = float(n or 0), float(d or 0)
        return round(num / den, 4) if den != 0 else 0.0
    except: return 0.0

def _limpiar_valor(v):
    """Convierte strings de contabilidad a flotantes."""
    if v is None or v == "": return 0.0
    if isinstance(v, (int, float)): return float(v)
    try: return float(str(v).replace(',', '').replace('$', '').strip())
    except: return 0.0