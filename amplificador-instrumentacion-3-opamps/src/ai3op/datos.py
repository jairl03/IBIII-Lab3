"""Lectura de los CSV de la carpeta data/."""

from __future__ import annotations

import csv
from pathlib import Path


def _filas(ruta: Path) -> list[dict[str, str]]:
    with ruta.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def cargar_resistencias(carpeta: Path) -> dict[str, float]:
    """Devuelve {componente: valor medido en ohms}."""
    return {f["componente"]: float(f["medido_ohm"]) for f in _filas(carpeta / "resistencias_medidas.csv")}


def cargar_nominales(carpeta: Path) -> dict[str, float]:
    return {f["componente"]: float(f["nominal_ohm"]) for f in _filas(carpeta / "resistencias_medidas.csv")}


def cargar_osciloscopio(carpeta: Path) -> dict[str, dict[str, float | None]]:
    """Devuelve {'B': {...}, 'C': {...}} con los valores numéricos."""
    salida: dict[str, dict[str, float | None]] = {}
    for f in _filas(carpeta / "mediciones_osciloscopio.csv"):
        salida[f["etapa"]] = {
            k: (float(v) if v not in ("", None) else None)
            for k, v in f.items()
            if k not in ("etapa", "descripcion")
        }
    return salida


def cargar_dc(carpeta: Path) -> dict[str, float]:
    return {f["magnitud"]: float(f["valor_V"]) for f in _filas(carpeta / "mediciones_dc.csv")}


def cargar_generador(carpeta: Path) -> dict[str, str]:
    return {f["parametro"]: f["valor"] for f in _filas(carpeta / "configuracion_generador.csv")}
