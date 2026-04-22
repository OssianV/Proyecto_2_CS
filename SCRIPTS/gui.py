import os
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from typing import Dict, Optional

import ttkbootstrap as ttk
from ttkbootstrap.constants import OUTLINE, PRIMARY, SECONDARY, WARNING

FONT_HEADER = ("Segoe UI Semibold", 18)
FONT_TITLE = ("Segoe UI Semibold", 13)
FONT_BODY = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)

COLORS = {
    "navy": "#0F172A",
    "gold": "#D4A017",
    "yellow": "#FACC15",
    "white": "#FFFFFF",
    "off_white": "#F8FAFC",
    "black": "#111827",
    "muted": "#64748B",
    "border": "#E5E7EB",
}


class PathAndResults:
    """Sustituye variables globales para paths y resultados."""

    def __init__(self):
        self.bg_csv_path: Optional[str] = None
        self.er_csv_path: Optional[str] = None
        self.results: Dict = {}

    def set_bg_path(self, path: str) -> None:
        self.bg_csv_path = path

    def set_er_path(self, path: str) -> None:
        self.er_csv_path = path

    def set_results(self, results: Dict) -> None:
        self.results = results


class ProgramaGui:
    """Clase principal de la GUI del programa."""

    def __init__(self, results_dict: Optional[Dict] = None):
        self.state = PathAndResults()
        if results_dict:
            self.state.set_results(results_dict)

        self.root: tk.Tk = ttk.Window(themename="cosmo")
        self.root.geometry("920x560")
        self.root.minsize(820, 500)
        self.root.configure(bg=COLORS["off_white"])

        self.bg_file_var: Optional[tk.StringVar] = None
        self.er_file_var: Optional[tk.StringVar] = None
        self._loop_started = False

        self._configure_styles()

    def _create_window(self, title: str) -> tk.Tk:
        """Reutiliza la misma ventana principal."""
        self.root.title(title)
        self.root.configure(bg=COLORS["off_white"])

        for child in self.root.winfo_children():
            child.destroy()

        return self.root

    def _start_loop_once(self) -> None:
        """Inicia mainloop solo una vez."""
        if not self._loop_started:
            self._loop_started = True
            self.root.mainloop()

    def _configure_styles(self) -> None:
        """Estilos globales."""
        style = ttk.Style()
        style.configure("App.TFrame", background=COLORS["off_white"])
        style.configure("Card.TFrame", background=COLORS["white"])

        style.configure(
            "Title.TLabel",
            font=FONT_TITLE,
            background=COLORS["white"],
            foreground=COLORS["black"],
        )
        style.configure(
            "Body.TLabel",
            font=FONT_BODY,
            background=COLORS["white"],
            foreground=COLORS["black"],
        )
        style.configure(
            "Muted.TLabel",
            font=FONT_SMALL,
            background=COLORS["white"],
            foreground=COLORS["muted"],
        )
        style.configure(
            "Section.TLabel",
            font=("Segoe UI Semibold", 11),
            background=COLORS["white"],
            foreground=COLORS["black"],
        )

        style.configure("TButton", font=("Segoe UI Semibold", 10), padding=(12, 8))
        style.configure("Treeview", font=FONT_BODY, rowheight=30)
        style.configure("Treeview.Heading", font=("Segoe UI Semibold", 10))

    def _build_window_shell(
        self,
        window_title: str,
        header_title: str,
        header_subtitle: str,
    ) -> ttk.Frame:
        """Construye la carcasa visual base de cada ventana."""
        self._create_window(window_title)

        outer = ttk.Frame(self.root, style="App.TFrame", padding=24)
        outer.pack(fill="both", expand=True)

        header = tk.Frame(outer, bg=COLORS["navy"], height=96)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text=header_title,
            font=FONT_HEADER,
            fg=COLORS["white"],
            bg=COLORS["navy"],
        ).pack(anchor="w", padx=24, pady=(18, 0))

        tk.Label(
            header,
            text=header_subtitle,
            font=FONT_BODY,
            fg="#D6E4FF",
            bg=COLORS["navy"],
        ).pack(anchor="w", padx=24, pady=(4, 16))

        accent = tk.Frame(outer, bg=COLORS["gold"], height=4)
        accent.pack(fill="x")

        card_border = tk.Frame(outer, bg=COLORS["border"])
        card_border.pack(fill="both", expand=True, pady=(18, 0))

        content = ttk.Frame(card_border, style="Card.TFrame", padding=24)
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
            path = askopenfilename(
                title=f"Escoge el archivo .csv de {display_name}",
                initialdir="../INPUTS",
                filetypes=[("CSV files", "*.csv")],
            )

            if not path:
                return

            if file_type == "BG":
                self.state.set_bg_path(path)
                if self.bg_file_var is not None:
                    self.bg_file_var.set(self._selected_file_text(path))
                self._show_info("Éxito", "Se cargó el archivo del Balance General exitosamente")

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

    def _build_file_panel(
        self,
        parent,
        title: str,
        file_var: tk.StringVar,
        command,
    ) -> None:
        """Panel visual para selección de un archivo CSV."""
        ttk.Label(parent, text=title, style="Section.TLabel").pack(anchor="w")
        ttk.Label(parent, text="Archivo seleccionado", style="Muted.TLabel").pack(
            anchor="w", pady=(8, 4)
        )
        ttk.Label(
            parent,
            textvariable=file_var,
            style="Body.TLabel",
            wraplength=300,
            justify="left",
        ).pack(anchor="w", pady=(0, 16))
        ttk.Button(
            parent,
            text="Seleccionar CSV",
            command=command,
            bootstyle=PRIMARY,
        ).pack(anchor="w")

    def welcome_window(self) -> None:
        """Ventana de bienvenida al usuario."""
        try:
            content = self._build_window_shell(
                "Bienvenida",
                "Análisis de estados financieros",
                "Proyecto escolar con una interfaz más limpia, manteniendo la lógica actual.",
            )

            for col in range(4):
                content.columnconfigure(col, weight=1)

            title_label = ttk.Label(
                content,
                text="Bienvenido al programa",
                style="Title.TLabel",
            )

            info_label = ttk.Label(
                content,
                text=(
                    "Esta versión mantiene tu flujo de navegación por ventanas, "
                    "pero mejora la jerarquía visual con un encabezado, tarjeta central, "
                    "tipografía moderna y botones con estilo consistente."
                ),
                style="Body.TLabel",
                justify="left",
                wraplength=760,
            )

            separator = ttk.Separator(content, orient="horizontal")

            manual_note = ttk.Label(
                content,
                text="El botón de manual puede conectarse después con un PDF o una ventana de ayuda.",
                style="Muted.TLabel",
                justify="left",
            )

            user_manual_button = ttk.Button(
                content,
                text="Manual de usuario",
                command=lambda: self._show_info(
                    "Manual de usuario",
                    "Pendiente de implementar.",
                ),
                bootstyle=(WARNING, OUTLINE),
            )

            next_button = ttk.Button(
                content,
                text="Siguiente",
                command=self.start_window,
                bootstyle=PRIMARY,
            )

            title_label.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 8))
            info_label.grid(row=1, column=0, columnspan=4, sticky="w", pady=(0, 12))
            separator.grid(row=2, column=0, columnspan=4, sticky="ew", pady=(0, 16))
            manual_note.grid(row=3, column=0, columnspan=4, sticky="w", pady=(0, 24))
            user_manual_button.grid(row=4, column=2, sticky="e", padx=(0, 8))
            next_button.grid(row=4, column=3, sticky="e")

            self._start_loop_once()

        except Exception as e:
            self._show_error(f"Ocurrió un error en la ventana de bienvenida: {str(e)}")

    def start_window(self) -> None:
        """Ventana inicial - carga de archivos CSV."""
        try:
            content = self._build_window_shell(
                "Carga de archivos",
                "Carga de archivos CSV",
                "Selecciona el Balance General y el Estado de Resultados para continuar.",
            )

            content.columnconfigure(0, weight=1)
            content.columnconfigure(1, weight=1)
            content.rowconfigure(2, weight=1)

            ttk.Label(
                content,
                text="Archivos requeridos",
                style="Title.TLabel",
            ).grid(row=0, column=0, columnspan=2, sticky="w")

            ttk.Label(
                content,
                text="La lógica de carga se mantiene igual; aquí solo cambia la presentación.",
                style="Muted.TLabel",
                wraplength=760,
                justify="left",
            ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(6, 16))

            self.bg_file_var = tk.StringVar(value=self._selected_file_text(self.state.bg_csv_path))
            self.er_file_var = tk.StringVar(value=self._selected_file_text(self.state.er_csv_path))

            bg_border = tk.Frame(content, bg=COLORS["border"])
            bg_border.grid(row=2, column=0, sticky="nsew", padx=(0, 12), pady=(0, 24))

            bg_panel = ttk.Frame(bg_border, style="Card.TFrame", padding=18)
            bg_panel.pack(fill="both", expand=True, padx=1, pady=1)

            self._build_file_panel(
                bg_panel,
                "Balance General",
                self.bg_file_var,
                lambda: self._select_csv_file("BG"),
            )

            er_border = tk.Frame(content, bg=COLORS["border"])
            er_border.grid(row=2, column=1, sticky="nsew", padx=(12, 0), pady=(0, 24))

            er_panel = ttk.Frame(er_border, style="Card.TFrame", padding=18)
            er_panel.pack(fill="both", expand=True, padx=1, pady=1)

            self._build_file_panel(
                er_panel,
                "Estado de Resultados",
                self.er_file_var,
                lambda: self._select_csv_file("ER"),
            )

            back_button = ttk.Button(
                content,
                text="Regresar",
                command=self.welcome_window,
                bootstyle=(SECONDARY, OUTLINE),
            )

            next_button = ttk.Button(
                content,
                text="Siguiente",
                command=self.results_window,
                bootstyle=PRIMARY,
            )

            back_button.grid(row=3, column=0, sticky="w")
            next_button.grid(row=3, column=1, sticky="e")

            self._start_loop_once()

        except Exception as e:
            self._show_error(f"Error en la ventana inicial: {str(e)}")

    def results_window(self) -> None:
        """Visualización de resultados."""
        try:
            content = self._build_window_shell(
                "Resultados",
                "Razones financieras calculadas",
                "La misma información ahora se presenta en una tabla más legible.",
            )

            for col in range(4):
                content.columnconfigure(col, weight=1)
            content.rowconfigure(2, weight=1)

            ttk.Label(
                content,
                text="Resultados del cálculo",
                style="Title.TLabel",
            ).grid(row=0, column=0, columnspan=4, sticky="w")

            ttk.Label(
                content,
                text="Se usa el mismo diccionario de resultados, solo cambia el formato visual.",
                style="Muted.TLabel",
                wraplength=760,
                justify="left",
            ).grid(row=1, column=0, columnspan=4, sticky="w", pady=(6, 16))

            table_border = tk.Frame(content, bg=COLORS["border"])
            table_border.grid(row=2, column=0, columnspan=4, sticky="nsew", pady=(0, 24))

            table_frame = ttk.Frame(table_border, style="Card.TFrame", padding=0)
            table_frame.pack(fill="both", expand=True, padx=1, pady=1)
            table_frame.columnconfigure(0, weight=1)
            table_frame.rowconfigure(0, weight=1)

            tree = ttk.Treeview(
                table_frame,
                columns=("indicador", "valor"),
                show="headings",
                height=12,
            )
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

            back_button = ttk.Button(
                content,
                text="Regresar",
                command=self.start_window,
                bootstyle=(SECONDARY, OUTLINE),
            )

            next_button = ttk.Button(
                content,
                text="Siguiente",
                command=self.dashboard_window,
                bootstyle=PRIMARY,
            )

            back_button.grid(row=3, column=0, sticky="w")
            next_button.grid(row=3, column=3, sticky="e")

            self._start_loop_once()

        except Exception as e:
            self._show_error(f"Error en la ventana de resultados: {str(e)}")

    def dashboard_window(self) -> None:
        """Ventana temporal - representa el dashboard (no implementado aun)."""
        try:
            content = self._build_window_shell(
                "Dashboard",
                "Dashboard",
                "Vista temporal mientras se implementa la parte gráfica final.",
            )

            for col in range(2):
                content.columnconfigure(col, weight=1)

            ttk.Label(
                content,
                text="Dashboard",
                style="Title.TLabel",
            ).grid(row=0, column=0, columnspan=2, sticky="w")

            ttk.Label(
                content,
                text="No implementado aún.",
                style="Body.TLabel",
            ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(8, 24))

            back_button = ttk.Button(
                content,
                text="Regresar",
                command=self.results_window,
                bootstyle=(SECONDARY, OUTLINE),
            )
            back_button.grid(row=2, column=0, sticky="w")

            self._start_loop_once()

        except Exception as e:
            self._show_error(f"Error en la ventana del dashboard: {str(e)}")

    def get_paths(self) -> tuple:
        """Get file paths for processing by other modules."""
        return (self.state.bg_csv_path, self.state.er_csv_path)