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

def _preparar_totales(d):
    """
    Suma las cuentas individuales para obtener los totales necesarios.
    """

    # Liquidez
    d["ACTIVO_CIRCULANTE"] = d.get("DISPONIBILIDAD_CAJA_Y_BANCOS") + d.get("DEUDORES") + d.get("REASEGURADORES_Y_REAFIANZADORES_NETO")
    d["PASIVO_CIRCULANTE"] = d.get("RESERVA_PARA_OBLIGACIONES_LABORALES") + d.get("ACREEDORES") + d.get("REASEGURADORES_Y_REAFIANZADORES")
    d["ACTIVO_DISPONIBLE"] = d.get("INVERSIONES") + d.get("DISPONIBILIDAD_CAJA_Y_BANCOS")
    d["PASIVO_EXIGIBLE"] = d.get("RESERVA_PARA_OBLIGACIONES_PENDIENTES_DE_CUMPLIR_POR_POLIZAS_VENCIDAS_Y_SINIESTROS_OCURRIDOS_PENDIENTES_DE_PAGO") + d.get("ACREEDORES_AGENTES_Y_AJUSTADORES") + d.get("ACREEDORES_DIVERSOS") +d.get("REASEGURADORES_Y_REAFIANZADORES_INSTITUCIONES_DE_SEGUROS_Y_FIANZAS") + d.get("OTROS_PASIVOS_PROVISION_PARA_EL_PAGO_DE_IMPUESTOS") + d.get("OTROS_PASIVOS_OTRAS_OBLIGACIONES") + d.get("OTROS_PASIVOS_PROVISION_PARA_LA_PARTICIPACION_DE_LOS_TRABAJADORES_EN_LA_UTILIDAD")
    
    # Solvencia y apalancamiento
    d["ACTIVO_FIJO"] = d.get("INVERSIONES_PERMANENTES") + d.get("OTROS_ACTIVOS")
    
    return d

def calcular_modulo_razones(dict_bg, dict_er):
    """
    Motor principal de cálculo de razones financieras.
    INPUT:  Diccionario con nombres exactos del Excel (ej. 'Reserva_de_Capital')
    OUTPUT: Diccionario con alias de las razones (ej. {'liq_circulante': 0.34})
    """
    # 1. Limpieza de valores (quita $, comas y convierte a float)
    d = {k: _limpiar_valor(v) for k, v in dict_bg.items()}
    e = {k: _limpiar_valor(v) for k, v in dict_er.items()}
    
    # 2. Pre-procesamiento: Sumar cuentas para obtener totales que no vienen en el Excel
    d = _preparar_totales(d)
    
    r = {}

    # --- CATEGORÍA: LIQUIDEZ ---
    r["liq_circulante"] = _div(d.get("ACTIVO_CIRCULANTE"), d.get("PASIVO_CIRCULANTE"))
    r["liq_disponibilidad"] = _div(d.get("ACTIVO_DISPONIBLE"), d.get("PASIVO_EXIGIBLE"))
    r["liq_exigibilidad"] = _div(d.get("ACTIVO_CIRCULANTE"), d.get("PASIVO_EXIGIBLE"))
    r["liq_reserva_tec"] = _div(d.get("ACTIVO_CIRCULANTE"), d.get("RESERVAS_TECNICAS"))

    # --- CATEGORÍA: SOLVENCIA Y APALANCAMIENTO ---
    r["sya_activos_pasivos"] = _div(d.get("SUMA_DEL_ACTIVO"), d.get("SUMA_DEL_PASIVO"))
    
    # Solvencia Depurada: (AT - AF) / (PT - Reservas Específicas)
    num_sol = d.get("SUMA_DEL_ACTIVO") - d.get("ACTIVO_FIJO") 
    den_sol = (d.get("SUMA_DEL_PASIVO") - 
               d.get("RESERVAS_TECNICAS_DE_RIESGOS_EN_CURSO") - 
               d.get("RESERVAS_TECNICAS_RESERVA_PARA_OBLIGACIONES_PENDIENTES_DE_CUMPLIR"))
    r["sya_depurada"] = _div(num_sol, den_sol)
    
    r["sya_pasivo_capital"] = _div(d.get("SUMA_DEL_PASIVO"), d.get("SUMA_DEL_CAPITAL"))
    r["sya_reserva_capital"] = _div(d.get("RESERVAS_TECNICAS"), d.get("SUMA_DEL_CAPITAL"))

    #a partir de aqui se usa el diccionario de cuentas del er

    # --- CATEGORÍA: SUFICIENCIA DE LA PRIMA ---
    r["suf_costo_operacion"] = _div(e.get("GASTOS_DE_OPERACION_NETOS"), e.get("PRIMAS_EMITIDAS")) 
    r["suf_costo_adquisicion"] = _div(e.get("COSTO_NETO_DE_ADQUISICION"), e.get("PRIMAS_DE_RETENCION"))
    r["suf_costo_siniestralidad"] = _div(e.get("COSTO_NETO_DE_SINIESTRALIDAD_RECLAMACIONES_Y_OTRAS_OBLIGACIONES_PENDIENTES_DE_CUMPLIR"), e.get("PRIMAS_DE_RETENCION"))
    
    r["suf_indice_combinado"] = r.get("suf_costo_operacion") + r.get("suf_costo_adquisicion") + r.get("suf_costo_siniestralidad")
    r["suf_de_la_prima"] = 1 - r.get("suf_indice_combinado")

    # --- CATEGORÍA: REASEGURO ---
    r["rea_prima_cedida"] = _div(e.get("PRIMAS_CEDIDAS"), e.get("PRIMAS_EMITIDAS"))
    r["rea_prima_retenida"] = _div(e.get("PRIMAS_DE_RETENCION"), e.get("PRIMAS_EMITIDAS"))
    r["rea_comision_reaseguro"] = _div(e.get("COSTO_NETO_DE_ADQUISICION_COMISIONES_POR_REASEGURO_Y_REAFIANZAMIENTO_CEDIDO"), e.get("PRIMAS_CEDIDAS"))

    # --- CATEGORÍA: RENTABILIDAD ---
    r["ren_utilidad_capital"] = _div(d.get("CAPITAL_GANADO_RESULTADO_O_REMANENTE_DEL_EJERCICIO"), d.get("SUMA_DEL_CAPITAL")) # Este usa el dict del balance general
    r["ren_utilidad_patrimonio"] = _div(d.get("CAPITAL_GANADO_RESULTADO_O_REMANENTE_DEL_EJERCICIO"), d.get("CAPITAL_CONTRIBUIDO_CAPITAL_O_FONDO_SOCIAL_PAGADO")) # Este usa el dict del balance general
    r["ren_utilidad_prima"] = _div(e.get("OPERACIONES_DISCONTINUADAS_UTILIDAD_PERDIDA_DEL_EJERCICIO"), e.get("PRIMAS_EMITIDAS")) # Este usa el dict del estado de resultados de nuevo

    return r



