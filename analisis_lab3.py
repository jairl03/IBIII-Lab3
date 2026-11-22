#!/usr/bin/env python3
"""
Análisis del Laboratorio N.º 3 - Instrumentación Biomédica III (UNMSM)
Amplificador de instrumentación de tres op-amps y rechazo de modo común.

Reproduce las Tablas 5 y 6 y las Figuras 12 y 13 del informe.
Uso:   python analisis_lab3.py
Para usar TUS mediciones, edita la sección DATOS (valores en ohms y volts).
"""
import math
from itertools import product

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# =============================== DATOS ===============================
# Resistencias medidas con el multímetro (ohms)
R = {"R1a": 9870, "R1b": 9860, "Rg": 975,
     "R2a": 9950, "R2b": 9940, "R3a": 9810, "R3b": 9830,
     "RD1": 9990, "RD2": 97.7}

# Etapa B (señal diferencial): Vpp en V1 y en VOUT
V1_PP, VOUT_B_PP = 0.0113, 0.233
# Etapa C (modo común): Vpp en V1 = V2 y en VOUT
VCM_PP, VOUT_C_PP = 1.05, 0.019
# Offset de VOUT con V1 y V2 a GND (V) y amplitud nominal del generador (Vpp)
OFFSET_V, VGEN_PP = 0.015, 1.0
# =====================================================================


def db(x):
    return 20 * math.log10(abs(x))


def acm_restador(r2a, r2b, r3a, r3b):
    """Ganancia de modo común del restador (análisis nodal): ka(1+kb)/(1+ka) - kb."""
    ka, kb = r3a / r2a, r3b / r2b
    return abs(ka * (1 + kb) / (1 + ka) - kb)


def peor_caso(t, nominal=10e3):
    """Mayor |Acm| del restador con 4 resistencias de tolerancia t (16 combinaciones ±t)."""
    peor = 0.0
    for d in product((-t, t), repeat=4):
        peor = max(peor, acm_restador(*(nominal * (1 + x) for x in d)))
    return peor


def calcular():
    ka, kb = R["R3a"] / R["R2a"], R["R3b"] / R["R2b"]
    g1 = 1 + (R["R1a"] + R["R1b"]) / R["Rg"]
    ad_teo = g1 * 0.5 * (ka + kb)
    ad = VOUT_B_PP / V1_PP
    acm = VOUT_C_PP / VCM_PP
    # Ecuación (5) del informe: (kb - ka)/(1 + kb). El análisis nodal exacto da 0.001513
    # (diferencia < 0.2 %), por eso el CMRR esperado sería 82.8 dB en lugar de 82.9 dB.
    acm_rest = abs(kb - ka) / (1 + kb)
    return dict(
        g1=g1, ka=ka, kb=kb, ad_teo=ad_teo, ad=ad, dif_pct=100 * (ad - ad_teo) / ad_teo,
        acm=acm, cmrr=db(ad / acm), ad_db=db(ad), acm_db=db(acm),
        acm_rest=acm_rest, cmrr_ap=db(ad_teo / acm_rest),
        vcm_equiv=VCM_PP / (ad / acm),
        offset_ent=OFFSET_V / 21,
        v1_esperada=VGEN_PP * R["RD2"] / (R["RD1"] + R["RD2"]),
    )


def figuras(r):
    # Figura 12
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 4.2))
    v = [21.0, r["ad_teo"], r["ad"]]
    bars = a.bar(["Nominal\n(diseño)", "Teórica\n(resist. medidas)", "Medida\n(Etapa B)"], v,
                 color=["#5b6770", "#1f3a5f", "#b8860b"])
    a.set_ylim(19.5, 21.5); a.set_ylabel("Ganancia diferencial $A_d$ (V/V)")
    a.set_title("(a) Ganancia diferencial")
    for x, y in zip(bars, v):
        a.text(x.get_x() + x.get_width() / 2, y + 0.03, f"{y:.3f}", ha="center", fontsize=9)
    vals = [r["ad_db"], r["acm_db"], db(r["acm_rest"])]
    bars = b.bar(["$A_d$ medida", "$A_{cm}$ medida", "$A_{cm}$ calculada\ncon resist. medidas"],
                 vals, color=["#b8860b", "#b03a2e", "#2e7d6b"])
    b.axhline(0, color="k", lw=0.8); b.set_ylabel("Ganancia (dB)"); b.set_ylim(-68, 34)
    b.set_title("(b) Diferencial frente a modo común")
    for x, y in zip(bars, vals):
        b.text(x.get_x() + x.get_width() / 2, y + (1 if y >= 0 else -1), f"{y:.1f} dB",
               ha="center", va="bottom" if y >= 0 else "top", fontsize=9)
    fig.tight_layout(); fig.savefig("fig12_ganancias.png", dpi=150); plt.close(fig)

    # Figura 13
    t = np.linspace(0.1, 6, 120)
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.plot(t, [peor_caso(x / 100) for x in t], color="#1f3a5f", lw=2,
            label="Peor caso (4 resistencias sin aparear)")
    ax.axhline(r["acm"], color="#b03a2e", ls="--", label=f"$A_{{cm}}$ medida = {r['acm']:.4f}")
    ax.axhline(r["acm_rest"], color="#2e7d6b", ls=":",
               label=f"$A_{{cm}}$ con resist. medidas = {r['acm_rest']:.4f}")
    for tol in (1, 5):
        y = peor_caso(tol / 100)
        ax.plot([tol], [y], "o", color="#b8860b")
        ax.annotate(f"±{tol} %: {y:.3f}", (tol, y), textcoords="offset points", xytext=(8, -14), fontsize=9)
    ax.set_yscale("log"); ax.grid(alpha=0.3, which="both"); ax.legend(fontsize=8, loc="upper left")
    ax.set_xlabel("Tolerancia de R2a, R2b, R3a, R3b (%)"); ax.set_ylabel("$A_{cm}$ del restador")
    fig.tight_layout(); fig.savefig("fig13_peor_caso.png", dpi=150); plt.close(fig)


def main():
    r = calcular()
    print("=== TABLA 5 · Ganancias y CMRR ===")
    print(f"Ganancia 1.ª etapa            : {r['g1']:.3f}")
    print(f"Ad teórica (resist. medidas)  : {r['ad_teo']:.3f}")
    print(f"Ad medida                     : {r['ad']:.3f}  ({r['dif_pct']:+.1f} % vs teórica)")
    print(f"Acm medida                    : {r['acm']:.4f}")
    print(f"CMRR medido                   : {r['cmrr']:.2f} dB")
    print(f"Acm del restador (apareamiento): {r['acm_rest']:.5f}")
    print(f"CMRR esperado por apareamiento: {r['cmrr_ap']:.1f} dB")
    print(f"Vcm equivalente en la entrada : {1e3 * r['vcm_equiv']:.2f} mVpp")
    print(f"Offset referido a la entrada  : {1e3 * r['offset_ent']:.2f} mV")
    print(f"V1 esperada por el divisor    : {1e3 * r['v1_esperada']:.2f} mVpp")
    print("\n=== TABLA 6 · Peor caso de Acm (restador sin aparear) ===")
    for t in (0.05, 0.01):
        a = peor_caso(t)
        print(f"±{100 * t:.0f} %: Acm = {a:.4f} · CMRR = {db(21 / a):.1f} dB · {a / r['acm']:.1f}x la Acm medida")
    figuras(r)
    print("\nFiguras guardadas: fig12_ganancias.png, fig13_peor_caso.png")


if __name__ == "__main__":
    main()
