import os
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from typing import Dict, Optional

# Librerias extra para mejorar la apariencia de tkinter basico
import ttkbootstrap as ttk
from ttkbootstrap.constants import OUTLINE, PRIMARY, SECONDARY, WARNING

from dashboard import build_dashboard

# Fuentes del texto de la GUI
FONT_HEADER = ("Segoe UI Semibold", 18)
FONT_TITLE = ("Segoe UI Semibold", 13)
FONT_BODY = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)

# Funciones temporales - representan funciones que se importaran de otros modulos no hechos

# Esta funcion es para probar la implementacion de la validacion en la GUI
def csv_validation(bg_path: str, er_path: str) -> Dict:
    return {"BG": (True, "El balance general no respeta la ecuacion contable A=P+C\nEl balance general no respeta regla 1\nEl balance general no respeta regla 2\n"), "ER": (True, "")}

# Esta funcion es para hacer los analisis automaticos de las razones financieras
def auto_analysis(results_dict: dict) -> Dict:
    return {"Liquidez":"Observacion_1\nObservacion_2\nObservacion_3",
            "Solvencia y Apalancamiento": "Observacion_4\nObservacion_5\nObservacion_6",
            "Suficiencia de la Prima": "Observacion_7\nObservacion_8\nObservacion_9",
            "Reaseguro": "Observacion_10\nObservacion_11\nObservacion_12",
            "Rentabilidad": "Observacion_13\nObservacion_14\nObservacion_15"}

#_____________________________

class PathAndResults:
    """Sustituye variables globales para paths y resultados."""

    # Se definen los atributos de la clase PathAndResults, siendo esstos:
    # bg_csv_path - el path del csv del balance general
    # er_csv_path - el path del csv del estado de resultados
    # resilts - el diccionario de resultados
    # En todos se usa type hint definiendolos como None, y definiendo que pueden tomar valot tipo string
    def __init__(self):
        self.bg_csv_path: Optional[str] = None
        self.er_csv_path: Optional[str] = None
        self.results: Dict = {}

    # Todas estas funciones son para cambiar el valor de los atributos
    def set_bg_path(self, path: str) -> None:
        self.bg_csv_path = path

    def set_er_path(self, path: str) -> None:
        self.er_csv_path = path

    def set_results(self, results: Dict) -> None:
        self.results = results


class ProgramaGui:
    """Clase principal de la GUI del programa."""

    def __init__(self, results_dict: Optional[Dict] = None):
        
        # Se define al atributo .state como una instancia de la clase PathAndResults()
        self.state = PathAndResults()

        # Evalua si contamos con el diccionario de resultados (razones financieras)
        if results_dict:
            self.state.set_results(results_dict)

        # Esto es nuevo. Antes para cambiar de ventana se destruian y creaban nuevas ventanas,
        # ahora se define una unica ventana como atributo de la clase, junto con sus caracteristicas
        # de apariencia. En las funciones de ventanas ahora solo se borraran los widgets, no la ventana.
        self.root: tk.Tk = ttk.Window(themename="cosmo")    # Se define el atributo .root como una ventana de ttk (la raiz)
        self.root.geometry("920x600")    # Tamano inicial
        self.root.minsize(820, 600)    # Tamano minimo
        
        self.chosen_analysis_text = tk.StringVar()
        self.bg_file_var: Optional[tk.StringVar] = None
        self.er_file_var: Optional[tk.StringVar] = None
        
        # Antes se llamaba a mainloop() en cada ventana, ahora se hace una sola vez. Este atributo lleva
        # registro de si ya se uso mainloop() para quye no se use de nuevo.
        self._loop_started = False

        #self._configure_styles()

    def _create_window(self, title: str) -> tk.Tk:
        """Reutiliza la misma ventana principal."""
        
        # Se cambia el titulo de la ventana
        self.root.title(title)
        
        # Se borran todos los widgets de la ventana
        for child in self.root.winfo_children():
            child.destroy()

        return self.root

    def _build_window_shell(self, window_title: str, header_title: str, header_subtitle: str) -> ttk.Frame:
        """Construye la carcasa visual base de cada ventana."""
        
        # Limpiamos la ventana principal
        self._create_window(window_title)

        # Definimos el frame exterior, definiendo que se ocupe todo el espacio sobrante, y que rellene 
        # vertical y horizontalmente
        outer = ttk.Frame(self.root, padding=24)
        outer.pack(fill="both", expand=True)

        # Definimos el frame del encabezado, donde solo rellena horizontalmente.
        header = tk.Frame(outer, height=96)
        header.pack(fill="x")
    
        # Titulo y subtitulo (dentro del encabezado)
        tk.Label(header, text=header_title, font=FONT_HEADER).pack(anchor="w", padx=24, pady=(18, 0))
        tk.Label(header, text=header_subtitle, font=FONT_BODY).pack(anchor="w", padx=24, pady=(4, 16))

        # Definimos frame que represente el borde del frame de contenido. Rellenando todo el espacio restante
        # (vertical y horizontal)
        card_border = tk.Frame(outer)
        card_border.pack(fill="both", expand=True, pady=(18, 0))

        # Definimos el frame del contenido. Aqui se pondran los widgets especificos de cada ventana.
        content = ttk.Frame(card_border, padding=24)
        content.pack(fill="both", expand=True, padx=1, pady=1)

        return content

    def _show_error(self, message: str) -> None:
        """Muestra mensaje de error al usuario."""
        messagebox.showerror("Error", message)

    def _show_info(self, title: str, message: str) -> None:
        """Muestra mensaje de informacion al usuario."""
        messagebox.showinfo(title, message)

    @staticmethod
    def _selected_file_text(path: Optional[str]) -> str:
        """Retorna solo el nombre del archivo, o un texto por defecto."""
        return os.path.basename(path) if path else "Ningún archivo seleccionado"

    def _select_csv_file(self, file_type: str) -> None:
        """Abre explorador de archivos y guarda el path del archivo seleccionado."""
        display_name = "Balance General" if file_type == "BG" else "Estado de Resultados"

        try:
            path = askopenfilename(title=f"Escoge el archivo .csv de {display_name}", filetypes=[("CSV files", "*.csv")])

            # Si no se selecciona archivo, no hace nada.
            if not path:
                return

            # Si el archivo esta asociado al balance general, se define su path y de actualiza el 
            # nombre del archivo actual seleccionado.
            if file_type == "BG":
                self.state.set_bg_path(path)
                if self.bg_file_var is not None:
                    self.bg_file_var.set(self._selected_file_text(path))
                self._show_info("Éxito", "Se cargó el archivo del Balance General exitosamente")

            # Mismo deal, pero ahora para el estado de resultados.
            elif file_type == "ER":
                self.state.set_er_path(path)
                if self.er_file_var is not None:
                    self.er_file_var.set(self._selected_file_text(path))
                self._show_info("Éxito", "Se cargó el archivo del Estado de Resultados exitosamente")

        except Exception as e:
            self._show_error(f"Error en la selección del archivo: {str(e)}")

    @staticmethod
    def _dict_to_string(data: Dict) -> str:
        """Convierte diccionarios a un string formateado."""
        if not data:
            return "No hay datos disponibles"
        return "\n".join(f"{key}: {value}" for key, value in data.items())

    def update_results_display(self, chosen_analysis: tk.StringVar) -> None:
        """Funcion para actualizar el texto de resultados cuando el tipo de analisis cambie"""
        selected = chosen_analysis.get()

        if selected == "Selecciona categoria de razon":
            self.chosen_analysis_text.set("")
        else:
            self.chosen_analysis_text.set(auto_analysis(self.state.results)[selected])

    @staticmethod
    def chosen_analysis_values(results: Dict, chosen_analysis: tk.StringVar) -> Dict:
        """Retorna un diccionario con los valores de las razones de la categoria seleccionada"""

        prefix_analysis_map = {"Liquidez":"liq",
                                "Solvencia y Apalancamiento": "sya",
                                "Suficiencia de la Prima": "suf",
                                "Reaseguro": "rea",
                                "Rentabilidad": "ren"}
        chosen_analysis_prefix = prefix_analysis_map[chosen_analysis.get()]
        chosen_results = {key: value for key, value in results.items() if key[:3] == chosen_analysis_prefix}

        return chosen_results

    def _build_file_panel(self, parent, title: str, file_var: tk.StringVar, command) -> None:
        """Panel visual para selección de un archivo CSV."""
        ttk.Label(parent, text=title).pack(anchor="w")    # Titulo del panel de seleecion de .csv
        ttk.Label(parent, text="Archivo seleccionado").pack(anchor="w", pady=(8, 4))
        ttk.Label(parent, textvariable=file_var, wraplength=300, justify="left").pack(anchor="w", pady=(0, 16))    # Archive seleccionado actualmente
        ttk.Button(parent, text="Seleccionar CSV", command=command, bootstyle=PRIMARY).pack(anchor="w")    # Boton para seleccionar archivo

    def update_treeview(self, tree) -> None:
        """Actualiza los valores del widget treeview dependiendo en el tipo de analisis escogido"""
        tree.delete(*tree.get_children())

        chosen_values = self.chosen_analysis_values(results=self.state.results, chosen_analysis=self.chosen_analysis)
        if chosen_values:
            for key, value in chosen_values.items():
                tree.insert("", "end", values=(str(key), str(value)))
        else:
            tree.insert("", "end", values=("Sin datos", "No hay resultados disponibles"))

    def welcome_window(self) -> None:
        """Ventana de bienvenida al usuario."""
        try:
            # Configurar ventana
            content = self._build_window_shell("Bienvenida", "Análisis de estados financieros", "Mini-app para calcular algunas razones financieras y generar un dashboard.")

            # Congifurar grid() de la ventana: Define 4 columnas en el frame content, se expanden horizontalmente.
            # Si sobra espacio horizontal, se reparte equitativamente entre todas la columnas.
            for col in range(4):
                content.columnconfigure(col, weight=1)

            # Definicion de widgets

            # Text widgets
            title_label = ttk.Label(content, text="Bienvenido al programa")
            info_label = ttk.Label(content,
                text=("Para ver como usar efectivamente esta mini-app, por favor presiona el boton 'Manual de usuario'."),
                justify="left",
                wraplength=760,
            )
            manual_note = ttk.Label(content, text="Presiona 'Siguiente' para avanzar cuando estes listo.", justify="left")

            # Separator widgets
            separator = ttk.Separator(content, orient="horizontal")

            # Button widgets
            user_manual_button = ttk.Button(content, text="Manual de usuario", command=lambda: self._show_info("Manual de usuario", "Pendiente de implementar."), bootstyle=(WARNING, OUTLINE))
            next_button = ttk.Button(content, text="Siguiente", command=self.start_window, bootstyle=PRIMARY)

            # Wiidget positioning
            title_label.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 8))
            info_label.grid(row=1, column=0, columnspan=4, sticky="w", pady=(0, 12))
            separator.grid(row=2, column=0, columnspan=4, sticky="ew", pady=(0, 16))
            manual_note.grid(row=3, column=0, columnspan=4, sticky="w", pady=(0, 24))
            user_manual_button.grid(row=4, column=2, sticky="e", padx=(0, 8))
            next_button.grid(row=4, column=3, sticky="e")

            # Inicio del loop de la ventana
            if not self._loop_started:
                self._loop_started = True
                self.root.mainloop()

        except Exception as e:
            self._show_error(f"Ocurrió un error en la ventana de bienvenida: {str(e)}")

    def start_window(self) -> None:
        """Ventana inicial - carga de archivos CSV."""
        try:

            # Configurar ventana
            content = self._build_window_shell(
                "Carga de archivos",
                "Carga de archivos CSV",
                "Selecciona el Balance General y el Estado de Resultados para continuar.",
            )

            # Configurar el grid() de la ventana
            content.columnconfigure(0, weight=1)
            content.columnconfigure(1, weight=1)
            content.rowconfigure(2, weight=1)

            # Crear titulo y subtitulo
            ttk.Label(content, text="Archivos requeridos").grid(row=0, column=0, columnspan=2, sticky="w")
            ttk.Label(content, text="Un archivo .csv para el Balance General y el Estado de Resultados es necesario.", wraplength=760, justify="left").grid(row=1, column=0, columnspan=2, sticky="w", pady=(6, 16))

            # Definimos los atributos asociados a los path de los archivos seleccionados (al inicio seran "Ningún archivo seleccionado")
            self.bg_file_var = tk.StringVar(value=self._selected_file_text(self.state.bg_csv_path))
            self.er_file_var = tk.StringVar(value=self._selected_file_text(self.state.er_csv_path))

            # Definimos el frame que contendra al frame que contendra al panel de seleccion del .csv del balance general
            bg_border = tk.Frame(content)
            
            # Definimos el frame que contendra el panel de seleccion de .csv del balance general, y lo generamos
            bg_panel = ttk.Frame(bg_border, padding=18)
            self._build_file_panel(bg_panel, "Balance General", self.bg_file_var, lambda: self._select_csv_file("BG"))

            # Frame del frame del panel de la seleccion .csv del estado de resultados
            er_border = tk.Frame(content)
            
            # Frame del panel y el panel de la seleccion del .csv del estado de resultados
            er_panel = ttk.Frame(er_border, padding=18)
            self._build_file_panel(er_panel, "Estado de Resultados", self.er_file_var, lambda: self._select_csv_file("ER"))

            # Button widgets
            back_button = ttk.Button(content, text="Regresar", command=self.welcome_window, bootstyle=(SECONDARY, OUTLINE))
            next_button = ttk.Button(content, text="Siguiente", command=self.results_window, bootstyle=PRIMARY)

            # Widget positioning
            bg_border.grid(row=2, column=0, sticky="nsew", padx=(0, 12), pady=(0, 24))
            bg_panel.pack(fill="both", expand=True, padx=1, pady=1)
            er_border.grid(row=2, column=1, sticky="nsew", padx=(12, 0), pady=(0, 24))
            er_panel.pack(fill="both", expand=True, padx=1, pady=1)
            back_button.grid(row=3, column=0, sticky="w")
            next_button.grid(row=3, column=1, sticky="e")

        except Exception as e:
            self._show_error(f"Error en la ventana inicial: {str(e)}")

    def results_window(self) -> None:
        """Visualización de resultados."""
        try:
            
            # Verificar que se hayan seleccionado .csv's
            if (self.state.bg_csv_path == None) | (self.state.er_csv_path == None):
                self._show_info("Error", "Necesitas ingresar los .csv's del Balance General y el Estado de Resultados")
                return
            
            # Verificar que los csv's hayan pasado la validacion
            csv_validation_results = csv_validation(bg_path=self.state.bg_csv_path, er_path=self.state.er_csv_path)

            validation_results = {}
            for key, value in csv_validation_results.items():
                if value[0] == False:
                    validation_results[key]=value[1]

            if validation_results:
                self._show_error("Oops. Los archivos .csv no son validos",self._dict_to_string(validation_results))
                return

            # Configurar ventana
            content = self._build_window_shell(
                "Resultados",
                "Razones financieras calculadas",
                "Aquí se muestran los valores de las razones calculadas.",
            )

            # Configurar grid
            for col in range(4):
                content.columnconfigure(col, weight=1)
            content.rowconfigure(3, weight=1)    # Configuramos que la fila 2 (asociada al frame de resultados) se extienda verticalmente en todo el espacio sobrante.

            # Crear titulo y subtitulo
            ttk.Label(content, text="Resultados del cálculo").grid(row=0, column=0, columnspan=4, sticky="w")
            ttk.Label(content, text="Selecciona la categoría de las razones.", wraplength=760, justify="left").grid(row=1, column=0, columnspan=4, sticky="w", pady=(6, 16))

            # Crear contenedor de resultados
            table_border = tk.Frame(content)
            table_border.grid(row=3, column=0, columnspan=4, sticky="nsew", pady=(0, 24))

            # Definir frame del contenido de resultados dentro del contenedor de resultados
            table_frame = ttk.Frame(table_border, padding=0)
            table_frame.pack(fill="both", expand=True, padx=1, pady=1)
            table_frame.columnconfigure(0, weight=1)
            table_frame.rowconfigure(0, weight=1)

            # Define el widget Treeview para mostrar resultados
            tree = ttk.Treeview(table_frame, columns=("indicador", "razon"), show="headings", height=12)
            tree.heading("indicador", text="Indicador")
            tree.heading("razon", text="Razon")
            tree.column("indicador", width=420, anchor="w")
            tree.column("razon", width=240, anchor="center")

            # Crear menu de opciones para seleccionar categoria de analisis y actualizar treeview
            analysis_options = ["Liquidez", "Solvencia y Apalancamiento", "Suficiencia de la Prima", "Reaseguro", "Rentabilidad"]
            self.chosen_analysis = tk.StringVar()
            self.chosen_analysis.set("Selecciona categoria de razon")
            analysis_menu = ttk.OptionMenu(content, self.chosen_analysis, "Selecciona categoria de razon", *analysis_options,  command=lambda _:self.update_treeview(tree))    # Falta modificar el chosen_analysis_text y definir un label para mostrarlo
            analysis_menu.grid(row=2, column=0, columnspan=1, sticky="w", pady=(6, 16))

            # Se agrega una scrollbar en el treeview
            scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            tree.grid(row=0, column=0, sticky="nsew")
            scrollbar.grid(row=0, column=1, sticky="ns")

            # Boton siguiente y regresar
            back_button = ttk.Button(content, text="Regresar", command=self.start_window, bootstyle=(SECONDARY, OUTLINE))
            next_button = ttk.Button(content, text="Siguiente", command=self.dashboard_window, bootstyle=PRIMARY)
            back_button.grid(row=4, column=0, sticky="w")
            next_button.grid(row=4, column=3, sticky="e")

        except Exception as e:
            self._show_error(f"Error en la ventana de resultados: {str(e)}")

    def dashboard_window(self) -> None:
        """Construye la ventana del dashboard usando el modulo dashboard.py"""
        try:
            content = self._build_window_shell("Dashboard", "Dashboard", "Visualización de los resultados del calculo de las razones financieras.")

            content.columnconfigure(0, weight=1)
            content.rowconfigure(0, weight=1)

            dashboard_frame = ttk.Frame(content)
            dashboard_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 16))

            build_dashboard(dashboard_frame, self.state.results)

            back_button = ttk.Button(
                content,
                text="Regresar",
                command=self.results_window,
                bootstyle=(SECONDARY, OUTLINE),
            )
            back_button.grid(row=1, column=0, sticky="w")

        except Exception as e:
            self._show_error(f"Error en la ventana del dashboard: {str(e)}")

    def get_paths(self) -> tuple:
        """Get file paths for processing by other modules."""
        return (self.state.bg_csv_path, self.state.er_csv_path)