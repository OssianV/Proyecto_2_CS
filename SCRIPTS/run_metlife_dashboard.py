"""Lanzador del dashboard standalone de MetLife."""

from __future__ import annotations

import argparse
from pathlib import Path

from metlife_dashboard_data import DashboardData, ExcelDashboardLoader


def parse_args() -> argparse.Namespace:
    # Si el usuario no pasa nada, usamos el Excel del proyecto actual.
    project_root = Path(__file__).resolve().parents[1]
    default_workbook = project_root / "INPUTS" / "PIA_main_razones.xlsx"

    parser = argparse.ArgumentParser(description="Dashboard standalone de MetLife usando Tkinter y ttkbootstrap.")
    parser.add_argument("--workbook", default=str(default_workbook), help="Ruta al workbook fuente.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Solo valida la carga del workbook y muestra un resumen sin abrir la interfaz.",
    )
    return parser.parse_args()


def print_summary(data: DashboardData) -> None:
    # Este modo es útil para probar la lectura del archivo desde terminal.
    print("Workbook:", data.workbook_path)
    print("Categorías:", data.categories)
    print("Años:", data.years)
    print("Razones:", len(data.ratios_wide))
    print("Cuentas:", len(data.accounts_wide))
    print("Columnas ratios:", list(data.ratios_wide.columns))
    print("Columnas cuentas:", list(data.accounts_wide.columns))


def main() -> int:
    args = parse_args()

    # Primero cargamos y validamos datos; si eso falla, la app ni siquiera intenta abrirse.
    data = ExcelDashboardLoader(Path(args.workbook).resolve()).load()
    if args.check:
        print_summary(data)
        return 0

    from metlife_dashboard_app import MetLifeDashboardApp

    app = MetLifeDashboardApp(data)
    app.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
