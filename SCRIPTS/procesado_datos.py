import pandas as pd
import re
import numpy as np

# Helper functions
def extraer_numero(valor):
    """Busca un patron numerico dentro de un valor"""
    if pd.isna(valor):
        return None
    
    match = re.search(r'-?\d+[\d,]*\.?\d*', str(valor))    # Busca un patron numerico dentro de 'valor'
    if match:
        return float(match.group().replace(",", ""))
    return None

def normalizar_nombre_cuenta(texto):
    """Estandariza los nombres de las cuentas"""
    if texto is None:
        return None
    
    texto = str(texto).strip()
    
    texto = texto.replace("(-)", "")
    texto = texto.replace("( - )", "")
    texto = texto.replace("(Neto)", "")
    texto = texto.replace("(Netos)", "")
    texto = texto.replace("(neto)", "")
    texto = texto.strip()
    
    texto = re.sub(r'\s+', ' ', texto)
    texto = texto.replace(" ", "_")
    
    return texto

# Funciones de validacion
def validar_balance(diccionario):
    
    errores = []
    
    activos = diccionario.get(normalizar_nombre_cuenta("Suma del Activo"), 0)
    pasivos = diccionario.get(normalizar_nombre_cuenta("Suma del Pasivo"), 0)
    capital = diccionario.get(normalizar_nombre_cuenta("Suma del Capital"), 0)
    
    if activos != pasivos + capital:
        errores.append("Suma del Activo ≠ Suma del Pasivo + Capital")
    
    if len(errores) == 0:
        return (True, "")
    else:
        return (False, "; ".join(errores))

def validar_resultados(diccionario):
    errores = []
    
    emitidas = diccionario.get(normalizar_nombre_cuenta("Emitidas"), 0)
    cedidas = diccionario.get(normalizar_nombre_cuenta("Cedidas"), 0)
    a = diccionario.get(normalizar_nombre_cuenta("Incremento Neto de la Reserva de Riesgos en Curso y de Fianzas en Vigor"), 0)
    b = diccionario.get(normalizar_nombre_cuenta("Costo Neto de Adquisición"), 0)
    c = diccionario.get(normalizar_nombre_cuenta("Costo Neto de Siniestralidad, Reclamaciones y Otras Obligaciones Pendientes de Cumplir"), 0)
    d = diccionario.get(normalizar_nombre_cuenta("Incremento Neto de Otras Reservas Técnicas"), 0)
    e = diccionario.get(normalizar_nombre_cuenta("Resultado de Operaciones Análogas y Conexas"), 0)
    f = diccionario.get(normalizar_nombre_cuenta("Gastos de Operación Netos"), 0)
    g = diccionario.get(normalizar_nombre_cuenta("Resultado Integral de Financiamiento"), 0)
    h = diccionario.get(normalizar_nombre_cuenta("Provisión para el pago del Impuestos a la Utilidad"), 0)
    i = diccionario.get(normalizar_nombre_cuenta("Utilidad (Pérdida) antes de Operaciones Discontinuadas"), 0)
    
    if abs(emitidas - (cedidas + a + b + c + d - e + f - g + h + i)) > 0.00001:
        errores.append("Las cuentas no dan como suma las primas emitidas")
    
    if None in diccionario.values():
        errores.append("Hay cuentas no encontradas en el archivo")
    
    return (len(errores) == 0, "; ".join(errores))


# Funciones principales
def construir_diccionario_balance(df_bg, cuentas_objetivo):
    """Definir un diccionario 'cuentas':valor , del BG"""
    df = df_bg.copy()

    resultado = {}
    
    for cuenta in cuentas_objetivo:
        llave = normalizar_nombre_cuenta(cuenta)
        encontrado = False
        
        for _, row in df.iterrows():
            for celda in row:
                
                if normalizar_nombre_cuenta(celda) == normalizar_nombre_cuenta(cuenta):
                    
                    for valor in row:
                        numero = extraer_numero(valor)
                        if numero is not None:
                            resultado[llave] = numero
                            encontrado = True
                            break
                    break
            
            if encontrado:
                break
        
        if not encontrado:
            resultado[llave] = None
    
    return resultado

def construir_diccionario_resultados(df_er, cuentas_objetivo):
    """Definir un diccionario 'cuentas':valor , del ER"""
    df = df_er.copy()
    
    resultado = {}
    
    for cuenta in cuentas_objetivo:
        llave = normalizar_nombre_cuenta(cuenta)
        encontrado = False
        
        for _, row in df.iterrows():
            for celda in row:
                
                if normalizar_nombre_cuenta(celda) == normalizar_nombre_cuenta(cuenta):
                    
                    for valor in row:
                        numero = extraer_numero(valor)
                        if numero is not None:
                            resultado[llave] = numero
                            encontrado = True
                            break
                    break
            
            if encontrado:
                break
        
        if not encontrado:
            resultado[llave] = None
    
    return resultado

def procesar_estados(balance_path, resultados_path):
    """Aplica el procesado y retorna el diccinario asociado al BG, al ER, y el de validaciones"""
    
    # Correr la funcion de transformacion del balance al nuevo formato

    

    #_______________________________________________


    cuentas_balance = [
        "Inversiones",
        "Valores y Operaciones con Productos Derivados",
        "Valores",
        "Gubernamentales",
        "Empresas Privadas. Tasa Conocida",
        "Empresas Privadas. Renta Variable",
        "Extranjeros",
        "Dividendos por Cobrar sobre Títulos de Capital",
        "(-) Deterioro de Valores",
        "Inversiones en Valores dados en Préstamo",
        "Valores Restringidos",
        "Operaciones con Productos Derivados",
        "Deudor por Reporto",
        "Cartera de Crédito (Neto)",
        "Cartera de Crédito Vigente",
        "Cartera de Crédito Vencida",
        "(-) Estimaciones Preventivas por Riesgo Crediticio",
        "Inmuebles (Neto)",
        "Inversiones para Obligaciones Laborales",
        "Disponibilidad",
        "Caja y Bancos",
        "Deudores",
        "Por Primas",
        "Deudor por Prima por Subsidio Daños",
        "Adeudos a cargo de Dependencias y Entidades de la Administración Pública Federal",
        "Primas por Cobrar de Fianzas Expedidas",
        "Agentes y Ajustadores",
        "Documentos por Cobrar",
        "Deudores por Responsabilidades",
        "Otros",
        "(-) Estimación para Castigos",
        "Reaseguradores y Reafianzadores (Neto)",
        "Instituciones de Seguros y Fianzas",
        "Depósitos Retenidos",
        "Importes Recuperables de Reaseguro",
        "(-) Estimación preventiva de riesgos crediticios de  Reaseguradores Extranjeros",
        "Intermediarios de Reaseguro y Reafianzamiento",
        "(-) Estimación para Castigos",
        "Inversiones Permanentes",
        "Subsidiarias",
        "Asociadas",
        "Otras Inversiones Permanentes",
        "Otros Activos",
        "Mobiliario y Equipo (Neto)",
        "Activos Adjudicados (Neto)",
        "Diversos",
        "Activos Intangibles Amortizables (Netos)",
        "Activos Intangibles de larga duración (Netos)",
        "Suma del Activo",
        "Reservas Técnicas",
        "De Riesgos en Curso",
        "Seguros de Vida",
        "Seguros de Accidentes y Enfermedades",
        "Seguros de Daños",
        "Reafianzamiento Tomado",
        "De Fianzas en Vigor",
        "Reserva para Obligaciones Pendientes de Cumplir",
        "Por Pólizas Vencidas y Siniestros Ocurridos pendientes de Pago",
        "Por Siniestros Ocurridos y No Reportados y Gastos de Ajuste Asignados a los Siniestros",
        "Por Fondos en Administración",
        "Por Primas en Depósito",
        "Reserva de Contingencia",
        "Reserva para Seguros Especializados",
        "Reserva de Riesgos Catastróficos",
        "Reserva para Obligaciones Laborales",
        "Acreedores",
        "Agentes y Ajustadores",
        "Fondos en Administración de Pérdidas",
        "Acreedores por Responsabilidades de Fianzas por Pasivos Constituidos",
        "Diversos",
        "Reaseguradores y Reafianzadores",
        "Instituciones de Seguros y Fianzas",
        "Depósitos Retenidos",
        "Otras Participaciones",
        "Intermediarios de Reaseguro y Reafianzamiento",
        "Operaciones con Productos Derivados. Valor Razonable (parte pasiva) al momento de la adquisición",
        "Financiamientos Obtenidos",
        "Emisión de Deuda",
        "Por Obligaciones Subordinadas No Susceptibles de Convertirse en Acciones",
        "Otros Títulos de Crédito",
        "Contratos de Reaseguro Financiero",
        "Otros Pasivos",
        "Provisión para la Participación de los Trabajadores en la Utilidad",
        "Provisión para el Pago de Impuestos",
        "Otras Obligaciones",
        "Créditos Diferidos",
        "Suma del Pasivo",
        "Capital Contable",
        "Capital Contribuido",
        "Capital o Fondo Social Pagado",
        "Capital o Fondo Social",
        "(-) Capital o Fondo Social No Suscrito",
        "(-) Capital o Fondo Social No Exhibido",
        "(-) Acciones Propias Recompradas",
        "Obligaciones Subordinadas de Conversión Obligatoria a Capital",
        "Capital Ganado",
        "Reservas",
        "Legal",
        "Para Adquisición de Acciones Propias",
        "Otras",
        "Superávit por Valuación",
        "Inversiones Permanentes",
        "Resultados o Remanentes de Ejercicios Anteriores",
        "Resultado o Remanente del Ejercicio",
        "Resultado por Tenencia de Activos No Monetarios",
        "Remediciones por Beneficios Definidos a los Empleados",
        "Participación Controladora",
        "Participación No Controladora",
        "Suma del Capital",
        "Suma del Pasivo y Capital"
    ]

    cuentas_resultados = [
        "Emitidas",
        "Cedidas",
        "De Retención",
        "Incremento Neto de la Reserva de Riesgos en Curso y de Fianzas en Vigor",
        "Primas de Retención Devengadas",
        "Costo Neto de Adquisición",
        "Comisiones a Agentes",
        "Compensaciones Adicionales a Agentes",
        "Comisiones por Reaseguro y Reafianzamiento Tomado",
        "Comisiones por Reaseguro y Reafianzamiento Cedido",
        "Cobertura de Exceso de Pérdida",
        "Otros",
        "Costo Neto de Siniestralidad, Reclamaciones y Otras Obligaciones Pendientes de Cumplir",
        "Siniestralidad y Otras Obligaciones Pendientes de Cumplir",
        "Siniestralidad Recuperada del Reaseguro No Proporcional",
        "Reclamaciones",
        "Utilidad (Pérdida) Técnica",
        "Incremento Neto de Otras Reservas Técnicas",
        "Reserva para Riesgos Catastróficos",
        "Reserva para Seguros Especializados",
        "Reserva de Contingencia",
        "Otras Reservas",
        "Resultado de Operaciones Análogas y Conexas",
        "Utilidad (Pérdida) Bruta",
        "Gastos de Operación Netos",
        "Gastos Administrativos y Operativos",
        "Remuneraciones y Prestaciones al Personal",
        "Depreciaciones y Amortizaciones",
        "Utilidad (Pérdida) de la Operación",
        "Resultado Integral de Financiamiento",
        "De Inversiones",
        "Por Venta de Inversiones",
        "Por Valuación de Inversiones",
        "Por Recargo sobre Primas",
        "Por Emisión de Instrumentos de Deuda",
        "Por Reaseguro Financiero",
        "Intereses por créditos",
        "Castigos preventivos por importes recuperables de reaseguro",
        "Castigos preventivos por riesgos crediticios",
        "Otros",
        "Resultado Cambiario",
        "Resultado por Posición Monetaria",
        "Participación en el Resultado de Inversiones Permanentes",
        "Utilidad (Pérdida) antes de Impuestos a la Utilidad",
        "Provisión para el pago del Impuestos a la Utilidad",
        "Utilidad (Pérdida) antes de Operaciones Discontinuadas",
        "Operaciones Discontinuadas",
        "Utilidad (Pérdida) del Ejercicio",
        "Participación Controladora",
        "Participación No Controladora"
    ]

    balance_dict = construir_diccionario_balance(bg_df, cuentas_balance.copy())
    resultados_dict = construir_diccionario_resultados(er_df, cuentas_resultados)
    
    val_balance = validar_balance(balance_dict)
    val_resultados = validar_resultados(resultados_dict)
    
    validaciones = {
        "BG": val_balance,
        "ER": val_resultados
    }
    
    return balance_dict, resultados_dict, validaciones



""" La estructura es la siguiente:

Se parte de una lista con los nombres de las cuentas sin
procesar del balance general, y una lista de los nombres
de las cuentas del estado de resultados.

Despues se construye un diccionario asociado al BG y
un diccionario asociado a el ER.

En base a los diccionarios, se ejecutan las validaciones.

Las funciones construir_diccionario hacen:

Reciben el path del balance de resultados y la lista de
las cuentas:

La del BG hace:
- lee el .csv
- Itera por los elementos de la lista de cuentas del BG
    - Itera por las filas 


"""