import os
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from typing import Dict, Optional

# Librerias extra para mejorar la apariencia de tkinter basico
import ttkbootstrap as ttk
from ttkbootstrap.constants import OUTLINE, PRIMARY, SECONDARY, WARNING

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
    return {"Razones de solvencia": "Tal y cual razon de solvencia esta muy alta\nTal y cual muy baja\nTal y cual en valores sanos para una aseguradora",
            "Razones de liquidez":"Nada que comentar\nDe nuevo nada que comentar"}

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
        self.root.geometry("920x560")    # Tamano inicial
        self.root.minsize(820, 500)    # Tamano minimo
        

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
            path = askopenfilename(title=f"Escoge el archivo .csv de {display_name}", initialdir="../INPUTS", filetypes=[("CSV files", "*.csv")])

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

    def _build_file_panel(self, parent, title: str, file_var: tk.StringVar, command) -> None:
        """Panel visual para selección de un archivo CSV."""
        ttk.Label(parent, text=title).pack(anchor="w")    # Titulo del panel de seleecion de .csv
        ttk.Label(parent, text="Archivo seleccionado").pack(anchor="w", pady=(8, 4))
        ttk.Label(parent, textvariable=file_var, wraplength=300, justify="left").pack(anchor="w", pady=(0, 16))    # Archive seleccionado actualmente
        ttk.Button(parent, text="Seleccionar CSV", command=command, bootstyle=PRIMARY).pack(anchor="w")    # Boton para seleccionar archivo

    def welcome_window(self) -> None:
        """Ventana de bienvenida al usuario."""
        try:
            # Configurar ventana
            content = self._build_window_shell("Bienvenida", "Análisis de estados financieros", "Proyecto escolar con una interfaz más limpia, manteniendo la lógica actual.")

            # Congifurar grid() de la ventana: Define 4 columnas en el frame content, se expanden horizontalmente.
            # Si sobra espacio horizontal, se reparte equitativamente entre todas la columnas.
            for col in range(4):
                content.columnconfigure(col, weight=1)

            # Definicion de widgets

            # Text widgets
            title_label = ttk.Label(content, text="Bienvenido al programa")
            info_label = ttk.Label(content,
                text=(
                    "Esta versión mantiene tu flujo de navegación por ventanas, "
                    "pero mejora la jerarquía visual con un encabezado, tarjeta central, "
                    "tipografía moderna y botones con estilo consistente."
                ),
                justify="left",
                wraplength=760,
            )
            manual_note = ttk.Label(content, text="El botón de manual puede conectarse después con un PDF o una ventana de ayuda.", justify="left")

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
            ttk.Label(content, text="La lógica de carga se mantiene igual; aquí solo cambia la presentación.", wraplength=760, justify="left").grid(row=1, column=0, columnspan=2, sticky="w", pady=(6, 16))

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

            # Configurar ventana
            content = self._build_window_shell(
                "Resultados",
                "Razones financieras calculadas",
                "La misma información ahora se presenta en una tabla más legible.",
            )

            # Configurar grid
            for col in range(4):
                content.columnconfigure(col, weight=1)
            content.rowconfigure(2, weight=1)    # Configuramos que la fila 2 (asociada al frame de resultados) se extienda verticalmente en todo el espacio sobrante.

            # Crear titulo y subtitulo
            ttk.Label(content, text="Resultados del cálculo").grid(row=0, column=0, columnspan=4, sticky="w")
            ttk.Label(content, text="Se usa el mismo diccionario de resultados, solo cambia el formato visual.", wraplength=760, justify="left").grid(row=1, column=0, columnspan=4, sticky="w", pady=(6, 16))

            # Crear contenedor de resultados
            table_border = tk.Frame(content)
            table_border.grid(row=2, column=0, columnspan=4, sticky="nsew", pady=(0, 24))

            # Definir frame del contenido de resultados dentro del contenedor de resultados
            table_frame = ttk.Frame(table_border, padding=0)
            table_frame.pack(fill="both", expand=True, padx=1, pady=1)
            table_frame.columnconfigure(0, weight=1)
            table_frame.rowconfigure(0, weight=1)

            #ESTO PLANEO CAMBIARLO_________
            tree = ttk.Treeview(table_frame, columns=("indicador", "valor"), show="headings", height=12)
            tree.heading("indicador", text="Indicador")
            tree.heading("valor", text="Valor")
            tree.column("indicador", width=420, anchor="w")
            tree.column("valor", width=240, anchor="center")

            if self.state.results:
                for key, value in self.state.results.items():
                    tree.insert("", "end", values=(str(key), str(value)))
            else:
                tree.insert("", "end", values=("Sin datos", "No hay resultados disponibles"))

            scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)

            tree.grid(row=0, column=0, sticky="nsew")
            scrollbar.grid(row=0, column=1, sticky="ns")

            #__________________________________

            # Boton siguiente y regresar
            back_button = ttk.Button(content, text="Regresar", command=self.start_window, bootstyle=(SECONDARY, OUTLINE))
            next_button = ttk.Button(content, text="Siguiente", command=self.dashboard_window, bootstyle=PRIMARY)
            back_button.grid(row=3, column=0, sticky="w")
            next_button.grid(row=3, column=3, sticky="e")

        except Exception as e:
            self._show_error(f"Error en la ventana de resultados: {str(e)}")

    def dashboard_window(self) -> None:
        """Ventana temporal - representa el dashboard (no implementado aun)."""
        try:
            content = self._build_window_shell("Dashboard", "Dashboard", "Vista temporal mientras se implementa la parte gráfica final.")

            for col in range(2):
                content.columnconfigure(col, weight=1)

            ttk.Label(content, text="Dashboard", style="Title.TLabel").grid(row=0, column=0, columnspan=2, sticky="w")

            ttk.Label(content, text="No implementado aún.", style="Body.TLabel").grid(row=1, column=0, columnspan=2, sticky="w", pady=(8, 24))

            back_button = ttk.Button(content, text="Regresar", command=self.results_window, bootstyle=(SECONDARY, OUTLINE))
            back_button.grid(row=2, column=0, sticky="w")

        except Exception as e:
            self._show_error(f"Error en la ventana del dashboard: {str(e)}")

    def get_paths(self) -> tuple:
        """Get file paths for processing by other modules."""
        return (self.state.bg_csv_path, self.state.er_csv_path)