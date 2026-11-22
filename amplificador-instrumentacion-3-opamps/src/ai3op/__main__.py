"""Uso:  python -m ai3op [--datos data] [--salida results]"""

from __future__ import annotations

import argparse
from pathlib import Path

from . import analisis, graficas


def main() -> None:
    p = argparse.ArgumentParser(description="Reproduce los cálculos y figuras del Lab 3 (IBI III).")
    p.add_argument("--datos", type=Path, default=Path("data"), help="carpeta con los CSV (por defecto: data)")
    p.add_argument("--salida", type=Path, default=Path("results"), help="carpeta de resultados (por defecto: results)")
    args = p.parse_args()

    res = analisis.calcular(args.datos)
    analisis.imprimir(res)
    analisis.guardar(res, args.salida)
    graficas.figura_12(res["resumen"], args.salida / "fig12_ganancias.png")
    graficas.figura_13(res["resumen"], args.salida / "fig13_peor_caso.png")
    print(f"\nResultados guardados en: {args.salida.resolve()}")


if __name__ == "__main__":
    main()
