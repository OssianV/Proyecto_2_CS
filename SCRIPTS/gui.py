import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from typing import Optional, Dict, Callable

# Constantes
FONT_TITLE = ("Century Gothic", 12, "bold")
FONT_BODY = ("Century Gothic", 10)


# Pendientes

# 1. Remplazar el uso de Optional, por simplemente usar el simbolo de disyuncion "|"
# 2. Al presionar el boton "Regresar" en la ventana de resultados, se tienen que volver a ingresar
#    los archivos .csv? - Si es asi, se tiene que cambiar esto. - No se tienen que volver a ingresar!
# 3. Agregar un cuadro de texto que muestre el nombre del .csv seleccionado


# Clases

class PathAndResults:
    """Definir esta clase sustituye el uso de variables globales para los path y el diccionario de resultados"""
    def __init__(self):
        self.bg_csv_path: Optional[str] = None    # Type hint: Indica que el atributo bf_csv_path de la clase ApplicationState es string o None (sin asignar valor).
        self.er_csv_path: Optional[str] = None    # Type hint: Indica que el atributo er_csv_path de la clase ApplicationState es string o None (sin asignar valor).
        self.results: Dict = {}    # Type hint: Indica que el atributo results de la clase ApplicationState es un dict (sin asignar valor).
    
    def set_bg_path(self, path: str) -> None:
        self.bg_csv_path = path
    
    def set_er_path(self, path: str) -> None:
        self.er_csv_path = path
    
    def set_results(self, results: Dict) -> None:
        self.results = results

class ProgramaGui:
    """Clase principal de la GUI del programa"""

    def __init__(self, results_dict: Optional[Dict] = None):
        self.state = PathAndResults()    # El atributo .state de la clase ProgramGui es una instancia de la clase PathAndResults
        if results_dict:
            self.state.set_results(results_dict)
        self.root: Optional[tk.Tk] = None    # El atributo .root de la clase ProgramGui es una ventana de tkinter o None
    
    def _create_window(self) -> tk.Tk:
        """Crear y retornar una nueva ventana de Tkinter"""
        if self.root:
            self.root.destroy()
        self.root = tk.Tk()
        return self.root

    def _show_error(self, message: str) -> None:
        """Muestra mensaje de error al usuario"""
        messagebox.showerror("Error", message)
    
    def _show_info(self, title: str, message: str) -> None:
        """Muestra mensaje de informacion al usuario"""
        messagebox.showinfo(title, message)

    def _select_csv_file(self, file_type: str) -> None:
        """Abre explorador de archivos y guarda el exact path del archivo en el atributo adecuado de la instancia de la clase PathAndResults "self.state" 

        Argumentos: file_type: "BG" (Balance General) o "ER" (Estado de Resultados)
        """
        try:
            path = askopenfilename(title=f"Escoge el archivo .csv de {file_type}",
                                   initialdir="../INPUTS",
                                   filetypes=[("CSV files", "*.csv")])
            if path:
                if file_type == "BG":
                    self.state.set_bg_path(path)
                    self._show_info("Exito", "Se cargo el archivo del Balance General exitosamente")
                elif file_type == "ER":
                    self.state.set_er_path(path)
                    self,self._show_info("Exito", "Se cargo el archivo del Estado de Resultados exitosamente")
        except Exception as e:
            self._show_error(f"Error en la seleccion del archivo: {str(e)}")

    @staticmethod    # A partir de aqui se definen metodos dentro de la clase que no requieren acceso a 'self' u otros datos de la clase
    def _dict_to_string(data: Dict) -> str:
        """Convierte diccionarios a un string formateado"""
        if not data:
            return "No hay datos disponibles"
        return "\n".join(f"{key}: {value}" for key, value in data.items())
    
    def start_window(self) -> None:
        """Ventana INICIAL - Donde el usuario ingresa los archivos .csv de los estados financieros"""
        try:
            self._create_window()

            # Definicion de widgets de la ventana

            # Texto
            title_label = tk.Label(self.root, text="Carga los archivos CSV de los estados financieros", font=FONT_TITLE)

            # Botones
            bg_button = tk.Button(self.root, text="Selecciona el csv del Balance General", command=lambda: self._select_csv_file("BG"), font = FONT_BODY)
            er_button = tk.Button(self.root, text="Selecciona el csv del Estado de Resultados", command=lambda: self._select_csv_file("ER"), font = FONT_BODY)
            next_button = tk.Button(self.root, text="Siguiente", command=self.results_window, font=FONT_BODY)
            
            # Posicionamiento de widgets
            title_label.grid(row=0, column=0, columnspan=4, padx=20, pady=20)
            bg_button.grid(row=1, column=1, padx=10, pady=20)
            er_button.grid(row=1, column=3, padx=10, pady=20)
            next_button.grid(row=3, column=3, padx=15, pady=10)

            self.root.mainloop()
        except Exception as e:
            self._show_error(f"Error en la ventana inicial: {str(e)}")

    def results_window(self) -> None:
        """Visualizacion de resultados"""
        try:
            self._create_window()
            
            # Definicion de widgest de la ventana

            # Texto
            title_label = tk.Label(self.root, text="Resultado del calculo de las razones financieras", font=FONT_TITLE  )
            results_text = self._dict_to_string(self.state.results)
            results_label = tk.Label(self.root, text=results_text, font=FONT_BODY, justify="left")

            # Botones
            back_button = tk.Button(self.root, text="Regresar", command=self.start_window, font=FONT_BODY)
            next_button = tk.Button(self.root, text="Siguiente", command=self.dashboard_window, font=FONT_BODY)

            # Posicionamiento de widgets
            title_label.grid(row=0, column=0, columnspan=4, padx=20, pady=20)
            results_label.grid(row=1, column=0, columnspan=4, padx=50, pady=50)
            back_button.grid(row=2, column=0, padx=15, pady=10)
            next_button.grid(row=2, column=3, padx=15, pady=10)

            self.root.mainloop()
        except Exception as e:
            self._show_error(f"Error en la ventana de resultados: {str(e)}")

    def dashboard_window(self) -> None:
        """Ventana temporal - Representa la ventana del dashboard (no implementado aun)"""
        try:
            self._create_window()

            message_label = tk.Label(self.root, text="Dashboard\n(No implementado aun)", font=FONT_TITLE)
            back_button = tk.Button(self.root, text="Regresar", command=self.results_window, font=FONT_BODY )

            message_label.pack(padx=20, pady=20)
            back_button.pack(padx=15, pady=10)
            
            self.root.mainloop()
        except Exception as e:
            self._show_error(f"Error en la ventana del dashboard: {str(e)}")

    def get_paths(self) -> tuple:
        """Get file paths for processing by other modules"""
        return (self.state.bg_csv_path, self.state.er_csv_path)