import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def build_dashboard(parent, results_dict):
    """Genera el dashboard en el parent frame"""
    results = results_dict or {}

    for child in parent.winfo_children():    # Borramos cualquier widget en el parent frame
        child.destroy()

    # Definimos una libreta en el parent frame, asignando que rellene espacio horizontal y vertical
    notebook = ttk.Notebook(parent)
    notebook.pack(fill="both", expand=True)

    create_liquidez_tab(notebook, results)
    create_solvencia_tab(notebook, results)
    create_suficiencia_tab(notebook, results)
    create_reaseguro_tab(notebook, results)
    create_rentabilidad_tab(notebook, results)

    return notebook

def get_value(results, key):
    """Retorna el valor asociado a una llave en un diccionario"""
    try:
        return float(results.get(key, 0))
    except:
        return 0.0

def draw_figure(frame, fig):
    """Dibujamos un grafico en un frame de tkk"""
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    frame.canvas = canvas

def create_card(parent, title, value):
    """Crea una tarjeta de informacion"""
    card = tk.Frame(parent, bd=1, relief="solid", padx=10, pady=10)
    card.pack(side="left", fill="x", expand=True, padx=5)

    title_label = tk.Label(card, text=title, font=("Segoe UI", 10, "bold"))
    title_label.pack(anchor="w")

    value_label = tk.Label(card, text=f"{value:.2f}", font=("Segoe UI", 16, "bold"))
    value_label.pack(anchor="w", pady=(8, 0))

def create_horizontal_chart(frame, title, labels, values, color):
    """Crea un grafico de barras horizontales"""
    fig, ax = plt.subplots(figsize=(7, 4))

    bars = ax.barh(labels, values, color=color)
    ax.set_title(title)
    ax.set_xlabel("Valor")
    ax.grid(axis="x", alpha=0.3)
    ax.invert_yaxis()

    # Agregamos el texto del valor a la derecha de cada barra
    for bar, value in zip(bars, values):
        ax.text(value, bar.get_y() + bar.get_height() / 2, f" {value:.2f}", va="center")

    fig.tight_layout()
    draw_figure(frame, fig)


def create_vertical_chart(frame, title, labels, values, colors):
    """Crea un grafico de barras verticales"""
    fig, ax = plt.subplots(figsize=(7,4))

    positions = list(range(len(labels)))
    bars = ax.bar(positions, values, color=colors)
    ax.set_title(title)
    ax.set_ylabel("Valor")
    ax.set_xticks(positions)
    ax.set_xticklabels(labels)
    ax.grid(axis="y", alpha=0.3)

    # Agregamos el texto del valor encima de cada barra
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value, f"{value:.2f}", ha="center", va="bottom")

    fig.tight_layout()
    draw_figure(frame, fig)


def create_liquidez_tab(notebook, results):
    """Define una pestana de liquidez en la notebook"""
    tab = ttk.Frame(notebook, padding=10)
    notebook.add(tab, text="Liquidez")

    # Definimos el grafico de barras horizontales
    labels = [
        "Activo circ. / Pasivo circ.",
        "Activo disp. / Pasivo exig.",
        "Activo circ. / Pasivo exig.",
        "Activo circ. / Reserva técnica",
    ]
    values = [
        get_value(results, "liq_circulante"),
        get_value(results, "liq_disponibilidad"),
        get_value(results, "liq_exigibilidad"),
        get_value(results, "liq_reserva_tec"),
    ]
    colors = ["skyblue", "orange", "lightgreen", "lightcoral"]

    create_horizontal_chart(tab, "Razones de liquidez", labels, values, colors)


def create_solvencia_tab(notebook, results):
    "Define una pestana de solvencia en la notebook"
    tab = ttk.Frame(notebook, padding=10)
    notebook.add(tab, text="Solvencia y Apalancamiento")

    # Definimos el grafico de barras horizontales
    labels = [
        "Activos tot. / Pasivos tot.",
        "Razón depurada",
        "Pasivo total / Capital",
        "Reservas tec. / Capital",
    ]
    values = [
        get_value(results, "sya_activos_pasivos"),
        get_value(results, "sya_depurada"),
        get_value(results, "sya_pasivo_capital"),
        get_value(results, "sya_reserva_capital"),
    ]
    colors = ["skyblue", "orange", "lightgreen", "lightcoral"]
    create_horizontal_chart(tab, "Razones de solvencia y apalancamiento", labels, values, colors)


def create_suficiencia_tab(notebook, results):
    "Define una pestana de suficiencia en la notebook"
    tab = ttk.Frame(notebook, padding=10)
    notebook.add(tab, text="Suficiencia de la Prima")

    # Definimos las tarjetas de info
    cards_frame = ttk.Frame(tab)
    cards_frame.pack(fill="x", pady=(0, 10))

    indice_combinado = get_value(results, "suf_indice_combinado")
    suficiencia_prima = get_value(results, "suf_de_la_prima")

    create_card(cards_frame, "Índice combinado", indice_combinado)
    create_card(cards_frame, "Suficiencia de la prima", suficiencia_prima)

    # Definimos el grafico de barras verticales
    chart_frame = ttk.Frame(tab)
    chart_frame.pack(fill=tk.BOTH, expand=True)

    labels = [
            "De operacion",
            "De adquisicion",
            "De siniestralidad",
        ]
    values = [
        get_value(results, "suf_costo_operacion"),
        get_value(results, "suf_costo_adquisicion"),
        get_value(results, "suf_costo_siniestralidad"),
    ]
    colors = ["skyblue", "orange", "lightgreen"]

    create_vertical_chart(chart_frame, "Costos medios", labels, values, colors)

def create_reaseguro_tab(notebook, results):
    """Define una pestana de reaseguro en la notebook"""
    tab = ttk.Frame(notebook, padding=10)
    notebook.add(tab, text="Reaseguro")

    tab.columnconfigure(0, weight=1)
    tab.columnconfigure(1, weight=1)
    tab.rowconfigure(0, weight=1)

    # Se definen los frames de ambos graficos (pie y de barras)
    pie_frame = ttk.Frame(tab)
    pie_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

    bar_frame = ttk.Frame(tab)
    bar_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

    # Se construye el grafico de pie
    cedida = get_value(results, "rea_prima_cedida")
    retenida = get_value(results, "rea_prima_retenida")

    fig, ax = plt.subplots(figsize=(7, 4))

    ax.pie([cedida, retenida], labels=["Prima cedida", "Prima retenida"], autopct="%1.1f%%", startangle=90, colors=["skyblue", "orange"])
    ax.set_title("Prima cedida y retenida")
    fig.tight_layout()
    draw_figure(pie_frame, fig)

    # Definimos el grafico de barras
    comision = get_value(results, "rea_comision_reaseguro")
    create_vertical_chart(bar_frame, "Comisión del reaseguro cedido", ["Comisión"], [comision], ["lightgreen"])


def create_rentabilidad_tab(notebook, results):
    """Define una pestana de rentabilidad en la notebook"""
    tab = ttk.Frame(notebook, padding=10)
    notebook.add(tab, text="Rentabilidad")

    # Definimos el grafico de barras verticales
    labels = [
        "Utilidad / Capital contable",
        "Utilidad / Capital pagado",
        "Utilidad / Prima emitida",
    ]
    values = [
        get_value(results, "ren_utilidad_capital"),
        get_value(results, "ren_utilidad_patrimonio"),
        get_value(results, "ren_utilidad_prima"),
    ]
    colors = ["skyblue", "orange", "lightgreen"]

    create_vertical_chart(tab, "Razones de rentabilidad", labels, values, colors)