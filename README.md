# Parcial 2 - Sistema de análisis financiero para las aseguradoras

---

Abstract: [PENDIENTE] - Poner un resumen del proyecto de un parrafo y pocas oraciones.

NOTA - Por el momento, la organizacion del proyecto la llevaremos a cabo en este READ.me. Al finalizar el proyecto ya lo convertimos en un READ.me normal.

### Alcances del proyecto

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
- Dashboard de los indicadores
- GUI util

### Entregables

- Scripts de python
    - Script principal: GUI
    - Modulo: Lectura, limpieza y validacion de datos.
    - Modulo: Calculo de razones financieras.
    - Modulo: Generacion del dashboard.
- Manual de usuario y operacion del sistema (pdf)
- Documento con resultados del analisis (pdf)

---

## Segmentacion de avances

A continuacion se lista con brevedad las tareas que cada uno debe realizar. Cada quien tiene tres secciones:

- MAIN: Esta seccion incluye las tareas que caen casi por completo en su responsabilidad, i.e. deben hacerlas casi por completo ustedes solos.
- SUBMAIN: Esta seccion incluye las tareas que colindan con las responsabilidades de otros. Un ejemplo es el de asegurarse que su codigo sea compatible con el de los demas y que se integre en el script principal correctamente.

La tercera seccion "EXTRA" se explica a detalle a continuacion:

### Tareas no asignadas

Las siguientes tareas o implementaciones deseadas no estan asignadas a nadie. Si alguien termina su parte y le sobra tiempo, pueden escoger alguna a discrecion y empezar a resolverla. Si hacen eso, borren de esta seccion dicha tarea y muevanla a su seccion de "EXTRA".

- Agregar funcionalidad para extraer datos de un pdf
- Agregar funcionalidad para inputs editables
- Extender dinamismo del formato excel de entrada. Esto es, hacer las implementaciones necesarias al codigo para que formatos mas laxos del script de entrada se puedan leer correctamente.
- Agregar funcionalidad en la GUI para inputs editables
- Agregar funcionalidad para escenarios what if?
- Agregar interpretacion automatica de razones financieras


### Ossian


> MAIN: Script GUI y modulo "Generacion del dashboard"
> - [ ] Planificar GUI completa.
> - [ ] Desarrollar GUI - no funcional.
> - [ ] Implementar funcionalidad a la GUI.
> - [ ] Planificar Dashboard completo.
> - [ ] Seleccionar plataforma/herramienta para hacer el dashboard.
> - [ ] Desarrollar Dashboard.

> SUBMAIN:
> - [ ] Definir una estructura basica de los archivos de excel de ingesta.
> - [ ] Definir estadares para el output del modulo "Lectura, limpieza y validacion de datos" y del modulo "Calculo de razones financieras"

EXTRA:
- [ ] None 

### Diego

> MAIN: Modulo "Lectura, limpieza y validacion de datos"
> - [ ] En base a la estructura basica de los archivos de excel de ingesta, desarrollar funciones para la lectura y la limpieza de los datos.
> - [ ] Determinar validaciones a realizar y desarrollar funciones que las implementen.
> - [ ] Documentar el proceso de lectura, limpieza y validacion de datos en una libreta de ipython
>     - Tienes que desarrollar un script .py limpio, la libreta es solo para que podamos ver como es que desarrollaste las funciones. Si vibe-codeaste algo, pidele al LLM que de  una breve explicacion del codigo para que podamos seguir el hilo.

> SUBMAIN:
> - [ ] Comprender la estrutura de la GUI.
>     - Algunas partes de tu codigo estaran estrictamente hiladas a la GUI, especialmente si implementamos inputs editables (esta en la lista de tareas extra, pero espero alcanzar a implementarlo). Es por esto que necesitas entender como funciona la GUI y ver que hace cada boton con precision.
> - [ ] El modulo "Calculo de razones financieras" depende del tuyo. Es por esto que debes analizar los estandares que definimos del tipo de output que esperamos. Asi idealmente no habra errores.

EXTRA:
- 

### Maria

> MAIN: Modulo "Calculo de razones financieras" y extra "Dashboard"
> - [ ] Desarrollar un modulo con las funciones para el calculo de razones financieras.
> - [ ] Pensar en que tipos de analisis podemos realizar usando las razones financieras.
>     - El documento final con el analisis obtenido debe incluir un analisis de las razones, no simplemente sus valores. Ve pensando en que informacion podemos obtener de cada indicador. Esto servira por si implementamos la tarea extra "interpretacion automatica de razones financieras".
> - [ ] Planificacion de las graficas a incluir en el dashboard.
>     - Creo que el modulo de calculo de razones financieras va a ser el mas sencillo. Por eso, si puedes ayuda a planear el dashboard. Esto no implica seleccionar la herramienta, ni programarlo. Simplemente bocetar como se deberia ver, pensar en el tipo de graficas a poner, etc. Una parte importante del dashboard es que se vea tipo "ejecutivo". Para eso habra que pensar bien en la paleta de colores, aspectos visuales, etc. A ese tipo de cosas me refiero con la planificacion.

> SUBMAIN:
> - [ ] Entender los estadandares definidos para el output esperado del modulo de limpieza, transformacion y validacion de datos. Tu modulo depende de dicho modulo, por tanto para que no haya errores al implementarlos en el script principal lo ideal es que entiendas bien lo que este retorna.


EXTRA:
- 

## Hipervinculos a archivos importantes dentro del proyecto

- [Formato basico de los archivos .csv de ingesta]()
- [Estructura de los inputs y ouputs de los modulos]() 

## Tutoriales, articulos, documentacion relevante

- Si no saben usar github y git, yo aprendi lo superbasico usando [esta lista de reproduccion](https://www.youtube.com/watch?v=BCQHnlnPusY&list=PLRqwX-V7Uu6ZF9C0YMKuns9sLDzK6zoiV). Alternativamente, pueden usar los propios [tutoriales de github](https://docs.github.com/en/get-started/start-your-journey/hello-world). O solo preguntenle a un LLM.
- Para que aprendan a usar la funcion de "issues", solo vean [este video](https://www.youtube.com/watch?v=WMykv2ZMyEQ&list=PLRqwX-V7Uu6ZF9C0YMKuns9sLDzK6zoiV&index=4)
- Lo basico de pandas lo pueden encontrar [aqui](https://pandas.pydata.org/docs/user_guide/index.html)
- Para que entiendan como funciona la programacion modular vean [este short](https://www.youtube.com/shorts/Ju6tP03GI7c). Para que vean como se veria un modulo creado por ustedes muy sencillo vean [este video](https://www.youtube.com/watch?v=cgxEqlGJcrY). Cuando yo he usado modulos siempre defino clases, y funciones dentro de clases; si puueden hagan lo mismo, aunque como se ve en el ultimo video esto no es necesario.

