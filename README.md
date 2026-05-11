# Parcial 2 - Sistema de análisis financiero para las aseguradoras

---

Abstract: [PENDIENTE] - Poner un resumen del proyecto de un parrafo y pocas oraciones.

NOTA - Por el momento, la organizacion del proyecto la llevaremos a cabo en este READ.me. Al finalizar el proyecto ya lo convertimos en un READ.me normal.

## Alcances del proyecto

---

El proyecto debe cumplir lo solicitado para el parcial 2 y para el PIA.

### Para el parcial 2

Para ver mas info, vean la [rubrica](ATTACHMENTS//_pdf/Rúbrica%20para%20examen%202%20Conta%20de%20seguros.pdf)

- Creacion de un modulo de entrada, procesamiento y validacion de informacion.
- Analisis financiero de las siguientes razones financieras:
    - Liquidez
        - Activo circulante/Pasivo circulante
        - Activo disponible/Pasivo exigible
        - Activo circulante/Pasivo exigible
        - Activo circulante/Reserva tecnica
    - Solvencia y apalancamiento
        - Activos totales/Pasivos totales
        - (Activo total - fijo)/(Pasivo total - Rva. Prev. - Rva. rgos. curso - Rva. oblig. pend. cumpl.)
        - Pasivo total/Capital contable
        - Reservas tecnicas/Capital contable
    - Suficiencia de la prima
        - Costo medio de operacion
        - Costo medio de adquisicion
        - Costo medio de siniestralidad
        - Indice combinado
        - Suficiencia de la prima
    - Reaseguro
        - Prima cedida/Prima emitida
        - Prima retenida/Prima emitida
        - Comisiones del reaseguro cedido/Prima cedida
    - Rentabilidad
        - Utilidad neta/Capital contable
        - Utilidad neta/Capital pagado + Rva. capital
        - Utilidad neta/Prima emitida
- Visualizacion de resultados
- Dashboard de las razones financieras
- GUI util

### Para el parcial 3

Para ver mas info, vean la [rubrica](/ATTACHMENTS/_pdf/PIA-Contabilidad%20de%20seguros.pdf).

- Extender el analisis a 5 años usando los estados financieros de metlife de los ultimos 5 años.
- Realizar una proyección de ventas de los próximos 12 meses.
- Realizar una proyeccion de sinistralidad de los proximos 12 meses.
- Rentabilidad de la aseguradora de los ultimos 5 años y de la proyeccion que realizamos.
- Proponer estrategias para mejorar los resultados proyectados.
- Hacer una analisis de la aseguradora y de los resultados y analisis realizados con el programa.

## Entregables

---

- Scripts de python
    - Script principal: [main.py](/SCRIPTS/main.py)
    - Modulo GUI: [gui.py](/SCRIPTS/gui.py)
    - Modulo de lectura, limpieza y validacion de datos: [procesado_datos.py](/SCRIPTS/procesado_datos.py)
    - Modulo: Calculo de razones financieras: [razones.py](/SCRIPTS/razones.py)
    - Modulo: Generacion del dashboard: [dashboard.py](/SCRIPTS/dashboard.py)
- Manual de usuario y operacion del sistema (pdf): [manual_de_usuario.py](/ATTACHMENTS/_pdf/manual_de_usuario.pdf)
- Documento con resultados del analisis (pdf): [PENDIENTE]()

## Segmentacion de avances

---

### Tareas no asignadas

- Agregar funcionalidad para extraer datos de un pdf
- Agregar funcionalidad para inputs editables
- Extender dinamismo del formato excel de entrada. Esto es, hacer las implementaciones necesarias al codigo para que formatos mas laxos del script de entrada se puedan leer correctamente.
- Agregar funcionalidad en la GUI para inputs editables
- Agregar funcionalidad para escenarios what if?
- Agregar interpretacion automatica de razones financieras
- Agregar opcion para que el ususario pueda seleccionar el estandar de las cifras (en miles, cientos de miles, millones de pesos), y que esto se vea reflejado en las graficas desarrolladas y los analisis realizados.

### IDEAS EXTRA EJECUTABLES

- [ ] Agregar opcion para mostrar y permitir editar valores de cuentas y modificar el archivo de excel
- [ ] 

### Ossian

- py teseract para cortar imagenes
    - cortar por secciones
        - cortar por estado financiero
        - cortar por seccion dentro del estado financiero
- buscar palabras inteligentemente
    - utilizar wildcards
- plantear un dashboard ejecutivo
    - agregar pestana de bienvenida donde se permita modificar los valores de cada cuenta
    - Agregar opcion para analisis de razones financieras por ano

> Yo me encargo de todo lo relacionado a implementar el trabajo en python y generar el dashboard.

> Extraccion de informacion:
> Voy a hacer scripts que leean directamente la informacion de los estados financieros en los pdfs, sin tener que sacar la informacion a mano.

> Procesamiento de datos:
> Voy a cambiar la manera en la que procesamos los datos usando pandas, cambiar convenciones de nombres y buscar palabras inteligentemente. El objetivo es que sea mas robusto y requiera menos handholding.

> GUI:
> Voy a hacer la GUI mas bonita y mas funcional.

> Dashboard:
> Voy a mejorar el dashboard, va a incluir mas informacion y va a parecerse mas a un dashboard tipo ejecutivo.

> Calculo de razones:
> Voy a agregar un semaforo para las razones e insights automaticos.

### Diego

> MAIN: Excel
> - [ ] Sacar manualmente los valores de los estados financieros del 2021 al 2025 de metlife
> - [ ] Realizar proyeccion de ventas de los 12 meses de 2026
> - [ ] Realizar proyeccion de ventas de los 12 meses de 2026
> - [ ] Obtener la rentabilidad de la aseguradora en los ultimos 5 años y de las proyecciones que realizamos
> - [ ] Concluir sobre lo que se espera de la proyeccion de ventas y rentabilidad.

### Maria

> MAIN: Excel
> - [ ] Calcular las razones financieras de cada año (2021 - 2025) a partir de los datos de los estados financieros que saco Diego a mano.
> - [ ] Analizar los resultados de las razones financieras y proponer estrategias con el objetivo de mejorar rendimiento.
    - Pensar en que analisis se podrian hacer entre razones de diferentes categorias.
    - Pensar en como mostrar dichos analisis conjuntos (no en programar la GUI o dashboard, sino ideas de como mostrarlo).
> - [ ] Calcular las razones financieras asociadas a las proyecciones realizadas y concluir al respecto

## Hipervinculos a archivos importantes dentro del proyecto

---

- [Formato basico de los archivos .csv de ingesta](SCRIPTS/Libreta_formato_csv_ingests.ipynb)
- [Estructura de los inputs y ouputs de los modulos](SCRIPTS/Estructura_inputs_outputs_modulos.ipynb) 

## Tutoriales, articulos, documentacion relevante

---

- Si no saben usar github y git, yo aprendi lo superbasico usando [esta lista de reproduccion](https://www.youtube.com/watch?v=BCQHnlnPusY&list=PLRqwX-V7Uu6ZF9C0YMKuns9sLDzK6zoiV). Alternativamente, pueden usar los propios [tutoriales de github](https://docs.github.com/en/get-started/start-your-journey/hello-world). O solo preguntenle a un LLM.
- Para que aprendan a usar la funcion de "issues", solo vean [este video](https://www.youtube.com/watch?v=WMykv2ZMyEQ&list=PLRqwX-V7Uu6ZF9C0YMKuns9sLDzK6zoiV&index=4)
- Lo basico de pandas lo pueden encontrar [aqui](https://pandas.pydata.org/docs/user_guide/index.html)
- Para que entiendan como funciona la programacion modular vean [este short](https://www.youtube.com/shorts/Ju6tP03GI7c). Para que vean como se veria un modulo creado por ustedes muy sencillo vean [este video](https://www.youtube.com/watch?v=cgxEqlGJcrY). Cuando yo he usado modulos siempre defino clases, y funciones dentro de clases; si puueden hagan lo mismo, aunque como se ve en el ultimo video esto no es necesario.
