"""Aplicación Tkinter + ttkbootstrap para el dashboard standalone de MetLife."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk as tk_ttk

import pandas as pd
import ttkbootstrap as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator

from metlife_dashboard_data import DashboardData, format_delta, format_ratio, short_label


FONT_HEADER = ("Segoe UI Semibold", 18)
FONT_TITLE = ("Segoe UI Semibold", 12)
FONT_BODY = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)
COLOR_PRIMARY = "#0d6efd"
COLOR_SUCCESS = "#198754"
COLOR_DANGER = "#dc3545"
CHART_SIZE = (5.5, 3.1)


class MetLifeDashboardApp:
    """Interfaz sencilla para revisar razones financieras por categoría."""

    def __init__(self, data: DashboardData):
        self.data = data
        self.latest_year = max(self.data.years)
        self.base_year = min(self.data.years)
        self.root = ttk.Window(themename="cosmo")
        self.root.title("Dashboard Ejecutivo - MetLife")
        self.category_state: dict[str, dict[str, object]] = {}
        self._configure_window()
        self._build_ui()

    def _configure_window(self) -> None:
        # Solo ajustamos el tamaño inicial; quitamos el reacomodo complejo de gráficas.
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        width = max(1080, min(1420, int(screen_width * 0.9)))
        height = max(740, min(900, int(screen_height * 0.86)))
        self.root.geometry(f"{width}x{height}")
        self.root.minsize(980, 680)

    def run(self) -> None:
        self.root.mainloop()

    def _build_ui(self) -> None:
        outer = ttk.Frame(self.root, padding=14)
        outer.pack(fill="both", expand=True)

        header = ttk.Frame(outer)
        header.pack(fill="x", pady=(0, 8))
        ttk.Label(header, text="Dashboard Ejecutivo de Razones Financieras", font=FONT_HEADER).pack(anchor="w")
        ttk.Label(
            header,
            text="Empresa: MetLife | Período: 2021-2025 | Fuente: PIA_main_razones.xlsx",
            font=FONT_BODY,
        ).pack(anchor="w", pady=(2, 0))
        ttk.Label(
            header,
            text="Tendencia histórica, comparativo anual y tabla de detalles.",
            font=FONT_SMALL,
        ).pack(anchor="w", pady=(2, 0))

        notebook = ttk.Notebook(outer)
        notebook.pack(fill="both", expand=True)

        # Ya no hay resumen: cada pestaña es una categoría con el mismo formato.
        for category in self.data.categories:
            self._build_category_tab(notebook, category)

    @staticmethod
    def _clear_container(frame: tk.Misc) -> None:
        for child in frame.winfo_children():
            child.destroy()

    def _show_empty_state(self, frame: tk.Misc, message: str) -> None:
        self._clear_container(frame)
        ttk.Label(frame, text=message, font=FONT_BODY, justify="center").pack(expand=True)

    def _render_cards(self, frame: tk.Misc, cards: list[dict[str, str]]) -> None:
        # Las tarjetas muestran tres datos rápidos sin mucho adorno visual.
        self._clear_container(frame)
        for column, card in enumerate(cards):
            frame.columnconfigure(column, weight=1)
            card_frame = tk.Frame(frame, bd=1, relief="solid", padx=10, pady=8, bg="white")
            card_frame.grid(row=0, column=column, sticky="nsew", padx=5, pady=5)

            tk.Label(
                card_frame,
                text=card["title"],
                font=("Segoe UI", 10, "bold"),
                bg="white",
                anchor="w",
                justify="left",
                wraplength=180,
            ).pack(anchor="w")
            tk.Label(
                card_frame,
                text=card["value"],
                font=("Segoe UI Semibold", 16),
                bg="white",
                fg=card.get("color", "#212529"),
            ).pack(anchor="w", pady=(6, 0))

            detail_text = card.get("detail")
            if detail_text:
                tk.Label(
                    card_frame,
                    text=detail_text,
                    font=FONT_SMALL,
                    bg="white",
                    fg="#495057",
                    anchor="w",
                    justify="left",
                    wraplength=210,
                ).pack(anchor="w", pady=(4, 0))

    def _render_table(
        self,
        frame: tk.Misc,
        dataframe: pd.DataFrame,
        numeric_columns: set[str] | None = None,
        height: int = 9,
    ) -> None:
        # La tabla inferior permite comparar todos los años sin cambiar de vista.
        self._clear_container(frame)
        numeric_columns = numeric_columns or set()

        if dataframe.empty:
            self._show_empty_state(frame, "No hay datos para mostrar.")
            return

        host = ttk.Frame(frame)
        host.pack(fill="both", expand=True)

        columns = list(dataframe.columns)
        tree = tk_ttk.Treeview(host, columns=columns, show="headings", height=height)
        tree.grid(row=0, column=0, sticky="nsew")

        y_scroll = ttk.Scrollbar(host, orient="vertical", command=tree.yview)
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll = ttk.Scrollbar(host, orient="horizontal", command=tree.xview)
        x_scroll.grid(row=1, column=0, sticky="ew")
        tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        host.columnconfigure(0, weight=1)
        host.rowconfigure(0, weight=1)

        for column in columns:
            width = 155 if column not in numeric_columns else 90
            anchor = "center" if column in numeric_columns else "w"
            tree.heading(column, text=column)
            tree.column(column, width=width, minwidth=75, anchor=anchor, stretch=True)

        for row in dataframe.itertuples(index=False):
            values = []
            for column, value in zip(columns, row):
                if column in numeric_columns:
                    values.append(format_ratio(value))
                else:
                    values.append(value)
            tree.insert("", "end", values=values)

    def _draw_figure(self, frame: tk.Misc, figure: Figure) -> None:
        # Esta versión es más simple: redibuja solo cuando el usuario cambia filtros.
        self._clear_container(frame)
        canvas = FigureCanvasTkAgg(figure, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        frame.canvas = canvas

    def _apply_year_axis(self, axis) -> None:
        # Así evitamos etiquetas raras como 2.021 o saltos extraños del eje x.
        axis.set_xticks(self.data.years)
        axis.set_xticklabels([str(year) for year in self.data.years])
        axis.xaxis.set_major_locator(MaxNLocator(integer=True))
        axis.set_xlim(self.base_year - 0.2, self.latest_year + 0.2)

    def _build_category_tab(self, notebook: ttk.Notebook, category: str) -> None:
        # Cada categoría repite el mismo esquema: controles, tarjetas, gráficas y tabla.
        tab = ttk.Frame(notebook, padding=14)
        notebook.add(tab, text=category)
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(3, weight=1)
        tab.rowconfigure(4, weight=1)

        category_wide = self.data.ratios_wide.loc[self.data.ratios_wide["Categoria"] == category].copy()
        category_long = self.data.ratios_long.loc[self.data.ratios_long["Categoria"] == category].copy()
        ratio_list = category_wide["Razon"].tolist()

        title_frame = ttk.Frame(tab)
        title_frame.grid(row=0, column=0, sticky="ew")
        ttk.Label(title_frame, text=f"{category} - MetLife", font=FONT_TITLE).pack(anchor="w")
        ttk.Label(
            title_frame,
            text="Vista histórica enfocada en una razón destacada y en el comparativo anual de la categoría.",
            font=FONT_BODY,
        ).pack(anchor="w", pady=(3, 0))

        controls = ttk.Frame(tab)
        controls.grid(row=1, column=0, sticky="ew", pady=(10, 8))
        year_var = tk.StringVar(value=str(self.latest_year))
        ratio_var = tk.StringVar(value=ratio_list[0])

        ttk.Label(controls, text="Año de referencia", font=FONT_BODY).pack(side="left")
        year_combo = ttk.Combobox(
            controls,
            values=[str(year) for year in self.data.years],
            textvariable=year_var,
            width=10,
            state="readonly",
        )
        year_combo.pack(side="left", padx=(8, 18))

        ttk.Label(controls, text="Razón destacada", font=FONT_BODY).pack(side="left")
        ratio_combo = ttk.Combobox(
            controls,
            values=ratio_list,
            textvariable=ratio_var,
            width=48,
            state="readonly",
        )
        ratio_combo.pack(side="left", padx=(8, 0), fill="x", expand=True)

        cards_frame = ttk.Frame(tab)
        cards_frame.grid(row=2, column=0, sticky="ew")

        chart_row = ttk.Frame(tab)
        chart_row.grid(row=3, column=0, sticky="nsew", pady=(4, 8))
        chart_row.columnconfigure(0, weight=1)
        chart_row.columnconfigure(1, weight=1)
        chart_row.rowconfigure(0, weight=1)

        trend_section = ttk.Labelframe(chart_row, text="Tendencia de la razón seleccionada", padding=8)
        trend_section.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        ranking_section = ttk.Labelframe(chart_row, text="Comparativo de razones por año", padding=8)
        ranking_section.grid(row=0, column=1, sticky="nsew", padx=(6, 0))

        detail_section = ttk.Labelframe(tab, text="Detalle anual", padding=8)
        detail_section.grid(row=4, column=0, sticky="nsew")

        self.category_state[category] = {
            "wide": category_wide,
            "long": category_long,
            "year_var": year_var,
            "ratio_var": ratio_var,
            "cards_frame": cards_frame,
            "trend_section": trend_section,
            "ranking_section": ranking_section,
            "table_section": detail_section,
        }

        year_combo.bind("<<ComboboxSelected>>", lambda _event, selected_category=category: self._update_category_tab(selected_category))
        ratio_combo.bind("<<ComboboxSelected>>", lambda _event, selected_category=category: self._update_category_tab(selected_category))
        self._update_category_tab(category)

    def _update_category_tab(self, category: str) -> None:
        # Este método recalcula solo la pestaña activa cuando cambia año o razón.
        state = self.category_state[category]
        wide = state["wide"]
        category_long = state["long"]
        selected_year = int(state["year_var"].get())
        selected_ratio = state["ratio_var"].get()

        ratio_history = category_long.loc[category_long["Razon"] == selected_ratio].sort_values("Anio")
        selected_row = ratio_history.loc[ratio_history["Anio"] == selected_year]
        selected_value = selected_row["Valor"].iloc[0] if not selected_row.empty else None

        base_row = ratio_history.loc[ratio_history["Anio"] == self.base_year]
        base_value = base_row["Valor"].iloc[0] if not base_row.empty else None
        delta_value = selected_value - base_value if selected_value is not None and base_value is not None else None

        max_row = ratio_history.loc[ratio_history["Valor"].idxmax()] if not ratio_history.empty else None
        cards = [
            {
                "title": f"Valor en {selected_year}",
                "value": format_ratio(selected_value),
                "detail": short_label(selected_ratio, 52),
                "color": COLOR_PRIMARY,
            },
            {
                "title": f"Cambio vs {self.base_year}",
                "value": format_delta(delta_value),
                "detail": "Variación absoluta de la razón destacada.",
                "color": COLOR_DANGER if delta_value is not None and delta_value < 0 else COLOR_SUCCESS,
            },
            {
                "title": "Alto histórico",
                "value": format_ratio(max_row["Valor"] if max_row is not None else None),
                "detail": f"Año: {int(max_row['Anio'])}" if max_row is not None else "N/D",
                "color": COLOR_SUCCESS,
            },
        ]
        self._render_cards(state["cards_frame"], cards)

        trend_figure = self._make_ratio_trend_figure(ratio_history, selected_ratio)
        ranking_figure = self._make_category_year_figure(category_long, selected_year)
        self._draw_figure(state["trend_section"], trend_figure)
        self._draw_figure(state["ranking_section"], ranking_figure)

        detail = wide[["Razon", *[str(year) for year in self.data.years]]].copy()
        detail[f"Cambio {self.latest_year}-{self.base_year}"] = detail[str(self.latest_year)] - detail[str(self.base_year)]
        numeric_columns = set([str(year) for year in self.data.years] + [f"Cambio {self.latest_year}-{self.base_year}"])
        self._render_table(state["table_section"], detail, numeric_columns=numeric_columns, height=9)

    def _make_ratio_trend_figure(self, ratio_history: pd.DataFrame, selected_ratio: str) -> Figure:
        figure = Figure(figsize=CHART_SIZE, dpi=100, constrained_layout=True)
        axis = figure.add_subplot(111)
        axis.plot(ratio_history["Anio"], ratio_history["Valor"], marker="o", linewidth=2.2, color=COLOR_PRIMARY)
        self._apply_year_axis(axis)
        axis.set_title(short_label(selected_ratio, 56))
        axis.set_xlabel("Año")
        axis.set_ylabel("Valor")
        axis.grid(axis="y", alpha=0.3)
        return figure

    def _make_category_year_figure(self, category_long: pd.DataFrame, selected_year: int) -> Figure:
        figure = Figure(figsize=CHART_SIZE, dpi=100, constrained_layout=True)
        axis = figure.add_subplot(111)
        year_frame = category_long.loc[category_long["Anio"] == selected_year].sort_values("Valor")
        axis.barh([short_label(label, 34) for label in year_frame["Razon"]], year_frame["Valor"], color=COLOR_SUCCESS)
        axis.set_title(f"Comparativo en {selected_year}")
        axis.set_xlabel("Valor")
        axis.grid(axis="x", alpha=0.3)
        return figure
