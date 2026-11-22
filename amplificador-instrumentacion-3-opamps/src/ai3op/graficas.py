"""Figuras 12 y 13 del informe."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # sin pantalla: funciona en servidores y en CI
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from . import modelo  # noqa: E402

AZUL, DORADO, ROJO, VERDE, GRIS = "#1f3a5f", "#b8860b", "#b03a2e", "#2e7d6b", "#5b6770"


def figura_12(resumen: dict, ruta: Path) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))

    nombres = ["Nominal\n(diseño)", "Teórica\n(resist. medidas)", "Medida\n(Etapa B)"]
    valores = [resumen["ad_nominal"], resumen["ad_teorica"], resumen["ad_medida"]]
    barras = ax1.bar(nombres, valores, color=[GRIS, AZUL, DORADO])
    ax1.set_ylim(19.5, 21.5)
    ax1.set_ylabel("Ganancia diferencial $A_d$ (V/V)")
    ax1.set_title("(a) Ganancia diferencial")
    for b, v in zip(barras, valores):
        ax1.text(b.get_x() + b.get_width() / 2, v + 0.03, f"{v:.3f}", ha="center", fontsize=9)

    acm_ap_db = modelo.db(resumen["acm_restador_informe"])
    etiquetas = ["$A_d$ medida", "$A_{cm}$ medida", "$A_{cm}$ calculada\ncon resist. medidas"]
    vals_db = [resumen["ganancia_dif_dB"], resumen["ganancia_cm_dB"], acm_ap_db]
    barras = ax2.bar(etiquetas, vals_db, color=[DORADO, ROJO, VERDE])
    ax2.axhline(0, color="k", lw=0.8)
    ax2.set_ylabel("Ganancia (dB)")
    ax2.set_title("(b) Diferencial frente a modo común")
    for b, v in zip(barras, vals_db):
        va, dy = ("bottom", 1.0) if v >= 0 else ("top", -1.0)
        ax2.text(b.get_x() + b.get_width() / 2, v + dy, f"{v:.1f} dB", ha="center", va=va, fontsize=9)
    ax2.set_ylim(-68, 34)

    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


def figura_13(resumen: dict, ruta: Path) -> None:
    t = np.linspace(0.1, 6.0, 120)
    acm = [modelo.acm_peor_caso(x / 100) for x in t]

    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.plot(t, acm, color=AZUL, lw=2, label="Peor caso (4 resistencias del restador sin aparear)")
    ax.axhline(resumen["acm_medida"], color=ROJO, ls="--", label=f"$A_{{cm}}$ medida = {resumen['acm_medida']:.4f}")
    ax.axhline(
        resumen["acm_restador_informe"],
        color=VERDE,
        ls=":",
        label=f"$A_{{cm}}$ con resistencias medidas = {resumen['acm_restador_informe']:.4f}",
    )
    for tol in (1, 5):
        v = modelo.acm_peor_caso(tol / 100)
        ax.plot([tol], [v], "o", color=DORADO)
        ax.annotate(f"±{tol} %: {v:.3f}", (tol, v), textcoords="offset points", xytext=(8, -14), fontsize=9)
    ax.set_yscale("log")
    ax.set_xlabel("Tolerancia de las resistencias R2a, R2b, R3a, R3b (%)")
    ax.set_ylabel("Ganancia de modo común del restador $A_{cm}$")
    ax.grid(alpha=0.3, which="both")
    ax.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
