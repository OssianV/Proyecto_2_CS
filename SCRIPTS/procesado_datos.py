import pandas as pd
import numpy as np
import re
from typing import Dict

def clean_string(string: any) -> str | None:    # Aqui estamos aplicando type hint. Le estamos diciendo a python que el argumento de entrada 'texto' puede ser cualquier
    """Limpiamos y estadarizamos un string"""                                                          # cosa, y que la funcion devuelve un string o None.
    if pd.isna(string) | (clean_number(string) != None):    # Asi evaluamos si texto es None, np.nan, NA, NaT o un numero (tras limpiar el fomato del numero)
        return None
    
    # Primero removemos espacios en los extremos, y los prefijos mencionados.
    cleaned_string = str(string).strip().removeprefix("(-)").removeprefix("( - )")

    # Ahora removemos todos los acentos y dieresis
    cleaned_string = cleaned_string.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
    cleaned_string = cleaned_string.replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "Ú").replace("ü", "u").replace("Ü", "U")

    # Ahora ponemos todo en mayusculas, sutituimos espacios en blanco por guiones bajos, removemos todo tipo de caracter menos una letra mayuscula de la A a la Z o un guion bajo,
    # removemos multiples guiones bajos contiguos, y removemos guiones bajos en los extremos
    cleaned_string = re.sub(r"[^A-Z_ñÑ]", "", cleaned_string.upper().replace(" ", "_"))
    cleaned_string = re.sub(r"_+", "_", cleaned_string).strip("_")

    return cleaned_string

def clean_number(number: any) -> float | None:
    """Limpiamos y estandarizamos un numero"""

    if pd.isna(number):
        return None
    
    try:
        cleaned_number = str(number).strip()    # Remueve leading y trailing espacios
        cleaned_number = re.sub(r"[^0-9.-]", "", cleaned_number)    # Remueve todo lo que no sea un digito, un punto o un menos
        cleaned_number = re.sub(r"(?<!^)-", "", cleaned_number)    # Remueve todos los menos que no esten al principio
        cleaned_number = re.sub(r"\.+", ".", cleaned_number)    # Remplaza puntos contiguos repetidos por un unico punto
        match = re.search(r'-?\d+\.?\d*', cleaned_number)    # Se verifica si hay un match del regex en el string
        return float(match.group()) if match else None    # Si hay un match, se retorna el valor casteado a float, si no un None
    except:
        return None

def standarize_bg_account_names(df_bg: pd.DataFrame) -> pd.DataFrame:

    df_cuentas_activos = df_bg.copy()
    df_cuentas_activos = df_cuentas_activos.iloc[:, 0:4]
    df_cuentas_activos = df_cuentas_activos.map(clean_string)

    df_standarized_cuentas_activos = df_cuentas_activos.copy()

    df_cuentas_pasycap = df_bg.copy()
    df_cuentas_pasycap = df_cuentas_pasycap.iloc[:, 6:10]
    df_cuentas_pasycap = df_cuentas_pasycap.map(clean_string)

    df_standarized_cuentas_pasycap = df_cuentas_pasycap.copy()

    # Estandarizacion de las cuentas de activos
    current_column_1_value = ""
    current_column_2_value = ""
    current_column_3_value = ""
    for index, row in df_cuentas_activos.iterrows():
        
        column_1_value = row.iloc[1]
        column_2_value = row.iloc[2]
        column_3_value = row.iloc[3]

        if column_1_value != None:
            current_column_1_value = column_1_value
            
        if column_2_value != None:
            current_column_2_value = column_2_value
            df_standarized_cuentas_activos.loc[index, :] = [None, None, "_".join([current_column_1_value, current_column_2_value]), None]
        
        if column_3_value != None:
            current_column_3_value = column_3_value
            df_standarized_cuentas_activos.loc[index, :] = [None, None, None, "_".join([current_column_2_value, current_column_3_value])]
            
    # Estandarizacion de las cuentas de pasivos y capital
    current_column_1_value = ""
    current_column_2_value = ""
    current_column_3_value = ""
    for index, row in df_cuentas_pasycap.iterrows():
        
        column_1_value = row.iloc[1]
        column_2_value = row.iloc[2]
        column_3_value = row.iloc[3]

        if column_1_value != None:
            current_column_1_value = column_1_value
            
        if column_2_value != None:
            current_column_2_value = column_2_value
            df_standarized_cuentas_pasycap.loc[index, :] = [None, None, "_".join([current_column_1_value, current_column_2_value]), None]
        
        if column_3_value != None:
            current_column_3_value = column_3_value
            df_standarized_cuentas_pasycap.loc[index, :] = [None, None, None, "_".join([current_column_2_value, current_column_3_value])]

    # Dataframe final
    df_standarized_bg = df_bg.copy()
    df_standarized_bg.iloc[:, :4] = df_standarized_cuentas_activos
    df_standarized_bg.iloc[:, 6:10] = df_standarized_cuentas_pasycap

    return df_standarized_bg

def standarize_er_account_names(df_er: pd.DataFrame) -> pd.DataFrame:

    df_cuentas_er = df_er.copy()
    df_cuentas_er = df_cuentas_er.iloc[:, 0:2]
    df_cuentas_er = df_cuentas_er.map(clean_string)

    df_standarized_cuentas_er = df_cuentas_er.copy()

    current_column_0_value = ""
    current_column_1_value = ""
    for index, row in df_cuentas_er.iterrows():
        
        column_0_value = row.iloc[0]
        column_1_value = row.iloc[1]

        if column_0_value != None:
            current_column_0_value = column_0_value
            
        if column_1_value != None:
            current_column_1_value = column_1_value
            df_standarized_cuentas_er.loc[index, :] = [None, "_".join([current_column_0_value, current_column_1_value])]
    
    df_standarized_er = df_er.copy()
    df_standarized_er.iloc[:, 0:2] = df_standarized_cuentas_er

    return df_standarized_er

def build_bg_accounts_map(bg_csv_path: str, list_accounts: list) -> Dict:
    df_original = pd.read_csv(bg_csv_path, encoding="utf-8", header=None)

    df_original_v2 = df_original.copy()
    df_original_v2 = df_original_v2.iloc[2: ]

    # Aqui se aplica la funcion para ajustar los nombres de las cuentas
    df_original_v2 = standarize_bg_account_names(df_original_v2)

    # Copia del dataframe donde se estandarizan nombres de cuentas y se remueven primeras dos filas
    df_cleaned = df_original_v2.copy()
    df_cleaned.iloc[:, [0,1,2,3]] = df_cleaned.iloc[:, [0,1,2,3]].map(clean_string)
    df_cleaned.iloc[:, [6,7,8,9]] = df_cleaned.iloc[:, [6,7,8,9]].map(clean_string)

    # Copia del df original a la cual le removemos las pimeras dos filas y las columnas que tienen valores numericos
    df_cuentas = df_original_v2.copy()
    df_cuentas = df_cuentas.iloc[:, [0,1,2,3,6,7,8,9]]

    # Limpiamos cada una de las entradas del df
    df_cuentas = df_cuentas.map(clean_string)
    
    bg_accounts_map = {}
    for account in list_accounts:
        cleaned_account = clean_string(account)    # Limpiamos el nombre de la cuenta
        match = df_cuentas.eq(cleaned_account).any(axis=1)    # Genera una serie con valores True o False, indicando el incide de las filas que que contienen el item
        
        if not match.any():
            bg_accounts_map[cleaned_account] = None
            continue

        match_row = df_cleaned.loc[match]    # Trae la fila del dataframe original donde se encuentra el item
        
        match_column_index = int(np.where(match_row.eq(cleaned_account).any(axis=0) == True)[0])
        section_row_to_search = match_row.iloc[:, match_column_index+1:match_column_index+6]

        for value in section_row_to_search.values[0].tolist():
            account_value = None
            value_cleaned = clean_number(value)
            if value_cleaned != None:
                account_value = value_cleaned
                break

        if account_value != None:
            bg_accounts_map[cleaned_account] = account_value
        else:
            bg_accounts_map[cleaned_account] = None
            
    return bg_accounts_map

def build_er_accounts_map(er_csv_path: str, list_accounts: list) -> Dict:
    df_original = pd.read_csv(er_csv_path, encoding="utf-8", header=None)

    df_original_v2 = df_original.copy()
    df_original_v2 = df_original_v2.iloc[2: ]

    # Aqui se aplica la funcion para ajustar los nombres de las cuentas
    df_original_v2 = standarize_er_account_names(df_original_v2)

    # Copia del dataframe donde se estandarizan nombres de cuentas y se remueven primeras dos filas
    df_cleaned = df_original_v2.copy()
    df_cleaned.iloc[:, [0,1]] = df_cleaned.iloc[:, [0,1]].map(clean_string)

    # Copia del df original a la cual le removemos las pimeras dos filas y las columnas que tienen valores numericos
    df_cuentas = df_original_v2.copy()
    df_cuentas = df_cuentas.iloc[:, [0,1]]

    # Limpiamos cada una de las entradas del df
    df_cuentas = df_cuentas.map(clean_string)
    
    er_accounts_map = {}
    for account in list_accounts:
        cleaned_account = clean_string(account)    # Limpiamos el nombre de la cuenta
        match = df_cuentas.eq(cleaned_account).any(axis=1)    # Genera una serie con valores True o False, indicando el incide de las filas que que contienen el item
        
        if not match.any():
            er_accounts_map[cleaned_account] = None
            continue

        match_row = df_cleaned.loc[match]    # Trae la fila del dataframe original donde se encuentra el item
        
        match_column_index = int(np.where(match_row.eq(cleaned_account).any(axis=0) == True)[0])
        section_row_to_search = match_row.iloc[:, match_column_index+1:match_column_index+5]

        for value in section_row_to_search.values[0].tolist():
            account_value = None
            value_cleaned = clean_number(value)
            if value_cleaned != None:
                account_value = value_cleaned
                break

        if account_value != None:
            er_accounts_map[cleaned_account] = account_value
        else:
            er_accounts_map[cleaned_account] = None
            
    return er_accounts_map

def bg_validation(bg_accounts_map: Dict) -> tuple:

    errores = []

    if None in bg_accounts_map.values():
        lista_cuentas_faltantes = [key for key, value in bg_accounts_map.items() if value == None]
        string_cuentas_faltantes = "\n".join(lista_cuentas_faltantes)
        errores.append("Las siguientes cuentas no se encuentran en el .csv del balance general:\n")
        return (False, errores[0]+string_cuentas_faltantes)

    activos = bg_accounts_map.get(clean_string("Suma del Activo"))
    pasivos = bg_accounts_map.get(clean_string("Suma del Pasivo"))
    capital = bg_accounts_map.get(clean_string("Suma del Capital"))
    pasivos_mas_capital = bg_accounts_map.get(clean_string("Suma del Pasivo y Capital"))
    
    if activos != pasivos + capital:
        errores.append("Suma del Activo ≠ Suma del Pasivo + Capital")
    elif activos != pasivos_mas_capital:
        errores.append("Suma del Activo ≠ Suma del Pasivo y Capital")

    if len(errores) == 0:
        return (True, "")
    else:
        return (False, "; ".join(errores))
    
def er_validation(er_accounts_map: Dict) -> tuple:

    errores = []
    
    if None in er_accounts_map.values():
        lista_cuentas_faltantes = [key for key, value in er_accounts_map.items() if value == None]
        string_cuentas_faltantes = "\n".join(lista_cuentas_faltantes)
        errores.append("Las siguientes cuentas no se encuentran en el .csv del estado de resultados:\n")
        return (False, errores[0]+string_cuentas_faltantes)

    emitidas = er_accounts_map.get(clean_string("Primas_Emitidas"))
    cedidas = er_accounts_map.get(clean_string("Primas_Cedidas"))
    a = er_accounts_map.get(clean_string("Primas_Incremento Neto de la Reserva de Riesgos en Curso y de Fianzas en Vigor"))
    b = er_accounts_map.get(clean_string("Costo Neto de Adquisición"))
    c = er_accounts_map.get(clean_string("Costo Neto de Siniestralidad, Reclamaciones y Otras Obligaciones Pendientes de Cumplir"))
    d = er_accounts_map.get(clean_string("Incremento Neto de Otras Reservas Técnicas"))
    e = er_accounts_map.get(clean_string("Resultado de Operaciones Análogas y Conexas"))
    f = er_accounts_map.get(clean_string("Gastos de Operación Netos"))
    g = er_accounts_map.get(clean_string("Resultado Integral de Financiamiento"))
    h = er_accounts_map.get(clean_string("Provisión para el pago del Impuestos a la Utilidad"))
    i = er_accounts_map.get(clean_string("Provisión para el pago del Impuestos a la Utilidad_Utilidad (Pérdida) antes de Operaciones Discontinuadas"))
    
    if abs(emitidas - (cedidas + a + b + c + d - e + f - g + h + i)) > 0.00001:
        errores.append("Las cuentas no dan como suma las primas emitidas")
     
    return (len(errores) == 0, "; ".join(errores))

def process_data(bg_csv_path: str, er_csv_path: str):
    
    cuentas_balance = [
        "Inversiones",
        "Inversiones_Valores y Operaciones con Productos Derivados",
        "Inversiones_Valores",
        "Valores_Gubernamentales",
        "Valores_Empresas Privadas. Tasa Conocida",
        "Valores_Empresas Privadas. Renta Variable",
        "Valores_Extranjeros",
        "Valores_Dividendos por Cobrar sobre Títulos de Capital",
        "Valores_(-) Deterioro de Valores",
        "Valores_Inversiones en Valores dados en Préstamo",
        "Valores_Valores Restringidos",
        "Inversiones_Operaciones con Productos Derivados",
        "Inversiones_Deudor por Reporto",
        "Inversiones_Cartera de Crédito (Neto)",
        "Cartera de Crédito (Neto)_Cartera de Crédito Vigente",
        "Cartera de Crédito (Neto)_Cartera de Crédito Vencida",
        "Cartera de Crédito (Neto)_(-) Estimaciones Preventivas por Riesgo Crediticio",
        "Inversiones_Inmuebles (Neto)",
        "Inversiones para Obligaciones Laborales",
        "Disponibilidad",
        "Disponibilidad_Caja y Bancos",
        "Deudores",
        "Deudores_Por Primas",
        "Deudores_Deudor por Prima por Subsidio Daños",
        "Deudores_Adeudos a cargo de Dependencias y Entidades de la Administración Pública Federal",
        "Deudores_Primas por Cobrar de Fianzas Expedidas",
        "Deudores_Agentes y Ajustadores",
        "Deudores_Documentos por Cobrar",
        "Deudores_Deudores por Responsabilidades",
        "Deudores_Otros",
        "Deudores_(-) Estimación para Castigos",
        "Reaseguradores y Reafianzadores (Neto)",
        "Reaseguradores y Reafianzadores (Neto)_Instituciones de Seguros y Fianzas",
        "Reaseguradores y Reafianzadores (Neto)_Depósitos Retenidos",
        "Reaseguradores y Reafianzadores (Neto)_Importes Recuperables de Reaseguro",
        "Reaseguradores y Reafianzadores (Neto)_(-) Estimación preventiva de riesgos crediticios de Reaseguradores Extranjeros",
        "Reaseguradores y Reafianzadores (Neto)_Intermediarios de Reaseguro y Reafianzamiento",
        "Reaseguradores y Reafianzadores (Neto)_(-) Estimación para Castigos",
        "Inversiones Permanentes",
        "Inversiones Permanentes_Subsidiarias",
        "Inversiones Permanentes_Asociadas",
        "Inversiones Permanentes_Otras Inversiones Permanentes",
        "Otros Activos",
        "Otros Activos_Mobiliario y Equipo (Neto)",
        "Otros Activos_Activos Adjudicados (Neto)",
        "Otros Activos_Diversos",
        "Otros Activos_Activos Intangibles Amortizables (Netos)",
        "Otros Activos_Activos Intangibles de larga duración (Netos)",
        "Suma del Activo",
        "Reservas Técnicas",
        "Reservas Técnicas_De Riesgos en Curso",
        "De Riesgos en Curso_Seguros de Vida",
        "De Riesgos en Curso_Seguros de Accidentes y Enfermedades",
        "De Riesgos en Curso_Seguros de Daños",
        "De Riesgos en Curso_Reafianzamiento Tomado",
        "De Riesgos en Curso_De Fianzas en Vigor",
        "Reservas Técnicas_Reserva para Obligaciones Pendientes de Cumplir",
        "Reserva para Obligaciones Pendientes de Cumplir_Por Pólizas Vencidas y Siniestros Ocurridos pendientes de Pago",
        "Reserva para Obligaciones Pendientes de Cumplir_Por Siniestros Ocurridos y No Reportados y Gastos de Ajuste Asignados a los Siniestros",
        "Reserva para Obligaciones Pendientes de Cumplir_Por Fondos en Administración",
        "Reserva para Obligaciones Pendientes de Cumplir_Por Primas en Depósito",
        "Reservas Técnicas_Reserva de Contingencia",
        "Reservas Técnicas_Reserva para Seguros Especializados",
        "Reservas Técnicas_Reserva de Riesgos Catastróficos",
        "Reserva para Obligaciones Laborales",
        "Acreedores",
        "Acreedores_Agentes y Ajustadores",
        "Acreedores_Fondos en Administración de Pérdidas",
        "Acreedores_Acreedores por Responsabilidades de Fianzas por Pasivos Constituidos",
        "Acreedores_Diversos",
        "Reaseguradores y Reafianzadores",
        "Reaseguradores y Reafianzadores_Instituciones de Seguros y Fianzas",
        "Reaseguradores y Reafianzadores_Depósitos Retenidos",
        "Reaseguradores y Reafianzadores_Otras Participaciones",
        "Reaseguradores y Reafianzadores_Intermediarios de Reaseguro y Reafianzamiento",
        "Operaciones con Productos Derivados. Valor Razonable (parte pasiva) al momento de la adquisición",
        "Financiamientos Obtenidos",
        "Financiamientos Obtenidos_Emisión de Deuda",
        "Financiamientos Obtenidos_Por Obligaciones Subordinadas No Susceptibles de Convertirse en Acciones",
        "Financiamientos Obtenidos_Otros Títulos de Crédito",
        "Financiamientos Obtenidos_Contratos de Reaseguro Financiero",
        "Otros Pasivos",
        "Otros Pasivos_Provisión para la Participación de los Trabajadores en la Utilidad",
        "Otros Pasivos_Provisión para el Pago de Impuestos",
        "Otros Pasivos_Otras Obligaciones",
        "Otros Pasivos_Créditos Diferidos",
        "Suma del Pasivo",
        "Capital Contribuido",
        "Capital Contribuido_Capital o Fondo Social Pagado",
        "Capital o Fondo Social Pagado_Capital o Fondo Social",
        "Capital o Fondo Social Pagado_(-) Capital o Fondo Social No Suscrito",
        "Capital o Fondo Social Pagado_(-) Capital o Fondo Social No Exhibido",
        "Capital o Fondo Social Pagado_(-) Acciones Propias Recompradas",
        "Capital o Fondo Social Pagado_Obligaciones Subordinadas de Conversión Obligatoria a Capital",
        "Capital Ganado",
        "Capital Ganado_Reservas",
        "Reservas_Legal",
        "Reservas_Para Adquisición de Acciones Propias",
        "Reservas_Otras",
        "Capital Ganado_Superávit por Valuación",
        "Capital Ganado_Inversiones Permanentes",
        "Capital Ganado_Resultados o Remanentes de Ejercicios Anteriores",
        "Capital Ganado_Resultado o Remanente del Ejercicio",
        "Capital Ganado_Resultado por Tenencia de Activos No Monetarios",
        "Capital Ganado_Remediciones por Beneficios Definidos a los Empleados",
        "Capital Ganado_Participación Controladora",
        "Capital Ganado_Participación No Controladora",
        "Suma del Capital",
        "Suma del Pasivo y Capital"
    ]

    cuentas_resultados = [
        "Primas_Emitidas",
        "Primas_Cedidas",
        "Primas_De Retención",
        "Primas_Incremento Neto de la Reserva de Riesgos en Curso y de Fianzas en Vigor",
        "Primas_Primas de Retención Devengadas",
        "Costo Neto de Adquisición",
        "Costo Neto de Adquisición_Comisiones a Agentes",
        "Costo Neto de Adquisición_Compensaciones Adicionales a Agentes",
        "Costo Neto de Adquisición_Comisiones por Reaseguro y Reafianzamiento Tomado",
        "Costo Neto de Adquisición_Comisiones por Reaseguro y Reafianzamiento Cedido",
        "Costo Neto de Adquisición_Cobertura de Exceso de Pérdida",
        "Costo Neto de Adquisición_Otros",
        "Costo Neto de Siniestralidad, Reclamaciones y Otras Obligaciones Pendientes de Cumplir",
        "Costo Neto de Siniestralidad, Reclamaciones y Otras Obligaciones Pendientes de Cumplir_Siniestralidad y Otras Obligaciones Pendientes de Cumplir",
        "Costo Neto de Siniestralidad, Reclamaciones y Otras Obligaciones Pendientes de Cumplir_Siniestralidad Recuperada del Reaseguro No Proporcional",
        "Costo Neto de Siniestralidad, Reclamaciones y Otras Obligaciones Pendientes de Cumplir_Reclamaciones",
        "Costo Neto de Siniestralidad, Reclamaciones y Otras Obligaciones Pendientes de Cumplir_Utilidad (Pérdida) Técnica",
        "Incremento Neto de Otras Reservas Técnicas",
        "Incremento Neto de Otras Reservas Técnicas_Reserva para Riesgos Catastróficos",
        "Incremento Neto de Otras Reservas Técnicas_Reserva para Seguros Especializados",
        "Incremento Neto de Otras Reservas Técnicas_Reserva de Contingencia",
        "Incremento Neto de Otras Reservas Técnicas_Otras Reservas",
        "Resultado de Operaciones Análogas y Conexas",
        "Resultado de Operaciones Análogas y Conexas_Utilidad (Pérdida) Bruta",
        "Gastos de Operación Netos",
        "Gastos de Operación Netos_Gastos Administrativos y Operativos",
        "Gastos de Operación Netos_Remuneraciones y Prestaciones al Personal",
        "Gastos de Operación Netos_Depreciaciones y Amortizaciones",
        "Gastos de Operación Netos_Utilidad (Pérdida) de la Operación",
        "Resultado Integral de Financiamiento",
        "Resultado Integral de Financiamiento_De Inversiones",
        "Resultado Integral de Financiamiento_Por Venta de Inversiones",
        "Resultado Integral de Financiamiento_Por Valuación de Inversiones",
        "Resultado Integral de Financiamiento_Por Recargo sobre Primas",
        "Resultado Integral de Financiamiento_Por Emisión de Instrumentos de Deuda",
        "Resultado Integral de Financiamiento_Por Reaseguro Financiero",
        "Resultado Integral de Financiamiento_Intereses por créditos",
        "Resultado Integral de Financiamiento_Castigos preventivos por importes recuperables de reaseguro",
        "Resultado Integral de Financiamiento_Castigos preventivos por riesgos crediticios",
        "Resultado Integral de Financiamiento_Otros",
        "Resultado Integral de Financiamiento_Resultado Cambiario",
        "Resultado Integral de Financiamiento_Resultado por Posición Monetaria",
        "Participación en el Resultado de Inversiones Permanentes",
        "Participación en el Resultado de Inversiones Permanentes_Utilidad (Pérdida) antes de Impuestos a la Utilidad",
        "Provisión para el pago del Impuestos a la Utilidad",
        "Provisión para el pago del Impuestos a la Utilidad_Utilidad (Pérdida) antes de Operaciones Discontinuadas",
        "Operaciones Discontinuadas",
        "Operaciones Discontinuadas_Utilidad (Pérdida) del Ejercicio",
        "Operaciones Discontinuadas_Participación Controladora",
        "Operaciones Discontinuadas_Participación No Controladora"
    ]

    bg_map = build_bg_accounts_map(bg_csv_path, cuentas_balance)
    er_map = build_er_accounts_map(er_csv_path, cuentas_resultados)
    
    bg_validation_result = bg_validation(bg_map)
    er_validation_result = er_validation(er_map)
    
    validaciones = {"BG": bg_validation_result, "ER": er_validation_result}
    
    return bg_map, er_map, validaciones