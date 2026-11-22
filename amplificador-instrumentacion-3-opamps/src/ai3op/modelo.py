"""Modelo del amplificador de instrumentación de tres op-amps (op-amps ideales).

Convención de nombres (coincide con el esquemático, docs/02-circuito.md):

* A1 (U1.1, pines 1-2-3) recibe V1 en su entrada no inversora y entrega O1.
* A2 (U1.2, pines 5-6-7) recibe V2 en su entrada no inversora y entrega O2.
* A3 (U1.3, pines 8-9-10) es el restador:
    - O1 -> R2a -> entrada NO inversora (pin 10), con R3a a GND.
    - O2 -> R2b -> entrada INVERSORA (pin 9), con R3b de realimentación (pin 8 -> 9).
"""

from __future__ import annotations

import math
from itertools import product


def db(razon: float) -> float:
    """Convierte una razón de tensiones a decibelios (20·log10)."""
    return 20.0 * math.log10(abs(razon))


# ---------------------------------------------------------------- ganancias
def ganancia_primera_etapa(r1a: float, r1b: float, rg: float) -> float:
    """G1 = 1 + (R1a + R1b)/Rg."""
    return 1.0 + (r1a + r1b) / rg


def razones_restador(r2a: float, r2b: float, r3a: float, r3b: float) -> tuple[float, float]:
    """ka = R3a/R2a (rama no inversora) y kb = R3b/R2b (rama inversora)."""
    return r3a / r2a, r3b / r2b


def ad_teorica(r: dict[str, float]) -> float:
    """Ecuación (3) del informe, con los valores *medidos*:

    Ad = [1 + (R1a+R1b)/Rg] · ½(R3a/R2a + R3b/R2b)
    """
    ka, kb = razones_restador(r["R2a"], r["R2b"], r["R3a"], r["R3b"])
    return ganancia_primera_etapa(r["R1a"], r["R1b"], r["Rg"]) * 0.5 * (ka + kb)


def ad_nominal(r1: float = 10e3, rg: float = 1e3, r2: float = 10e3, r3: float = 10e3) -> float:
    """Ecuación (2) con valores de diseño: (1 + 2R1/Rg)·(R3/R2) = 21."""
    return (1.0 + 2.0 * r1 / rg) * (r3 / r2)


# ------------------------------------------------------------ modo común
def acm_restador_informe(ka: float, kb: float) -> float:
    """Ecuación (5) tal como aparece en el informe: (kb − ka)/(1 + kb)."""
    return (kb - ka) / (1.0 + kb)


def acm_restador_exacta(ka: float, kb: float) -> float:
    """Ganancia de modo común del restador, deducida del análisis nodal.

    V+ = O·ka/(1+ka);  Vout = V+·(1+kb) − kb·O   (con O1 = O2 = O)
    =>  Acm = ka(1+kb)/(1+ka) − kb = (ka − kb)/(1 + ka)

    Difiere de la ecuación (5) del informe solo en el denominador (1+ka en vez de
    1+kb); para k ≈ 1 el resultado cambia menos de 0.2 % (0.001513 frente a 0.001510).
    """
    return ka * (1.0 + kb) / (1.0 + ka) - kb


def acm_peor_caso(tolerancia: float, nominal: float = 10e3) -> float:
    """Peor Acm del restador con R2a, R2b, R3a, R3b sin aparear.

    Evalúa las 16 combinaciones extremas ±t y devuelve la mayor |Acm|.
    """
    peor = 0.0
    for dv in product((-tolerancia, tolerancia), repeat=4):
        r2a, r2b, r3a, r3b = (nominal * (1.0 + d) for d in dv)
        ka, kb = razones_restador(r2a, r2b, r3a, r3b)
        peor = max(peor, abs(acm_restador_exacta(ka, kb)))
    return peor


# ------------------------------------------------------------- simulación
def vout_ideal(v1: float, v2: float, r: dict[str, float]) -> float:
    """Salida del circuito completo con op-amps ideales y resistencias reales.

    Etapa 1: la corriente por Rg es (V1 − V2)/Rg, de modo que
        O1 = V1 + R1a·(V1 − V2)/Rg      O2 = V2 − R1b·(V1 − V2)/Rg
    Etapa 2: restador con las razones ka y kb.
    """
    i_rg = (v1 - v2) / r["Rg"]
    o1 = v1 + r["R1a"] * i_rg
    o2 = v2 - r["R1b"] * i_rg
    ka, kb = razones_restador(r["R2a"], r["R2b"], r["R3a"], r["R3b"])
    v_mas = o1 * ka / (1.0 + ka)
    return v_mas * (1.0 + kb) - kb * o2


# ------------------------------------------------------------ otros cálculos
def divisor(vg: float, rd1: float, rd2: float) -> float:
    """Tensión en V1 para la Etapa B: Vg·RD2/(RD1+RD2)."""
    return vg * rd2 / (rd1 + rd2)
