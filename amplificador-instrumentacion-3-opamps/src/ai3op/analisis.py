"""Reproduce las Tablas 5 y 6 del informe a partir de los CSV de data/."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from . import datos, modelo


def calcular(carpeta_datos: Path) -> dict:
    r = datos.cargar_resistencias(carpeta_datos)
    osc = datos.cargar_osciloscopio(carpeta_datos)
    dc = datos.cargar_dc(carpeta_datos)
    gen = datos.cargar_generador(carpeta_datos)

    # --- Tabla 5 ---------------------------------------------------------
    ad_nom = modelo.ad_nominal()
    ad_teo = modelo.ad_teorica(r)
    g1 = modelo.ganancia_primera_etapa(r["R1a"], r["R1b"], r["Rg"])
    ka, kb = modelo.razones_restador(r["R2a"], r["R2b"], r["R3a"], r["R3b"])

    b, c = osc["B"], osc["C"]
    ad_med = b["salida_Vpp_V"] / b["entrada_Vpp_V"]
    acm_med = c["salida_Vpp_V"] / c["entrada_Vpp_V"]
    cmrr_med = modelo.db(ad_med / acm_med)

    acm_rest = abs(modelo.acm_restador_informe(ka, kb))  # ecuación (5) del informe
    acm_rest_exacta = abs(modelo.acm_restador_exacta(ka, kb))  # deducción nodal
    cmrr_rest = modelo.db(1.0 / acm_rest)  # solo el restador (Ad ≈ 1)
    cmrr_esperado = modelo.db(ad_teo / acm_rest)  # circuito completo, solo por apareamiento

    # --- Otros valores citados en el informe -------------------------------
    v1_esperada = modelo.divisor(float(gen["amplitud_Vpp_nominal"]), r["RD1"], r["RD2"])
    equiv_entrada = c["entrada_Vpp_V"] / (ad_med / acm_med)  # modo común referido a la entrada

    resumen = {
        "ad_nominal": ad_nom,
        "ganancia_primera_etapa": g1,
        "ka": ka,
        "kb": kb,
        "ad_teorica": ad_teo,
        "ad_medida": ad_med,
        "ad_dif_vs_teorica_pct": 100.0 * (ad_med - ad_teo) / ad_teo,
        "ad_dif_vs_nominal_pct": 100.0 * (ad_med - ad_nom) / ad_nom,
        "acm_medida": acm_med,
        "cmrr_medido_dB": cmrr_med,
        "cmrr_medido_razon": ad_med / acm_med,
        "ganancia_dif_dB": modelo.db(ad_med),
        "ganancia_cm_dB": modelo.db(acm_med),
        "acm_restador_informe": acm_rest,
        "acm_restador_exacta": acm_rest_exacta,
        "cmrr_restador_dB": cmrr_rest,
        "cmrr_primera_etapa_dB": modelo.db(g1),
        "cmrr_esperado_por_apareamiento_dB": cmrr_esperado,
        "acm_medida_sobre_acm_apareamiento": acm_med / acm_rest,
        "v1_esperada_Vpp": v1_esperada,
        "v1_medida_Vpp": b["entrada_Vpp_V"],
        "modo_comun_equivalente_entrada_Vpp": equiv_entrada,
        "offset_salida_V": dc["offset_vout"],
        "offset_referido_a_entrada_V": dc["offset_vout"] / ad_nom,
        "salida_si_ganara_igual_Vpp": c["entrada_Vpp_V"] * ad_med,
        "factor_entrada_C_sobre_B": c["entrada_Vpp_V"] / b["entrada_Vpp_V"],
        "factor_salida_B_sobre_C": b["salida_Vpp_V"] / c["salida_Vpp_V"],
    }

    # --- Tabla 6: peor caso según la tolerancia ------------------------------
    peor_caso = []
    for t in (0.05, 0.01):
        acm = modelo.acm_peor_caso(t)
        peor_caso.append(
            {
                "tolerancia_pct": 100 * t,
                "acm_peor_caso": acm,
                "cmrr_peor_caso_dB": modelo.db(21.0 / acm),
                "veces_mayor_que_medida": acm / acm_med,
                "diferencia_dB_vs_medido": modelo.db(21.0 / acm) - cmrr_med,
            }
        )
    return {"resumen": resumen, "peor_caso": peor_caso}


def guardar(resultados: dict, salida: Path) -> None:
    salida.mkdir(parents=True, exist_ok=True)
    (salida / "resumen.json").write_text(
        json.dumps(resultados, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    with (salida / "tabla5_ganancias_cmrr.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["magnitud", "valor"])
        for k, v in resultados["resumen"].items():
            w.writerow([k, f"{v:.6g}"])
    with (salida / "tabla6_peor_caso.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(resultados["peor_caso"][0].keys()))
        w.writeheader()
        for fila in resultados["peor_caso"]:
            w.writerow({k: f"{v:.6g}" for k, v in fila.items()})


def imprimir(resultados: dict) -> None:
    s = resultados["resumen"]
    print("=" * 66)
    print(" TABLA 5 - Ganancias y razón de rechazo de modo común")
    print("=" * 66)
    filas = [
        ("Ganancia 1.ª etapa [1+(R1a+R1b)/Rg]", f"{s['ganancia_primera_etapa']:.3f}"),
        ("Ad teórica (resistencias medidas)", f"{s['ad_teorica']:.3f}"),
        ("Ad medida  (Vout/V1, Etapa B)", f"{s['ad_medida']:.3f}"),
        ("  diferencia medida vs teórica", f"{s['ad_dif_vs_teorica_pct']:+.1f} %"),
        ("Acm medida (Vout/Vcm, Etapa C)", f"{s['acm_medida']:.4f}"),
        ("CMRR medido", f"{s['cmrr_medido_dB']:.2f} dB"),
        ("Acm del restador (ec. 5 del informe)", f"{s['acm_restador_informe']:.5f}"),
        ("Acm del restador (deducción exacta)", f"{s['acm_restador_exacta']:.5f}"),
        ("CMRR esperado solo por apareamiento", f"{s['cmrr_esperado_por_apareamiento_dB']:.1f} dB"),
        ("Vcm equivalente en la entrada", f"{1e3 * s['modo_comun_equivalente_entrada_Vpp']:.2f} mVpp"),
        ("Offset de VOUT referido a la entrada", f"{1e3 * s['offset_referido_a_entrada_V']:.2f} mV"),
        ("V1 esperada por el divisor (1 Vpp)", f"{1e3 * s['v1_esperada_Vpp']:.2f} mVpp"),
    ]
    for etiqueta, valor in filas:
        print(f" {etiqueta:<42} {valor:>18}")
    print()
    print("=" * 66)
    print(" TABLA 6 - Peor caso de Acm (R2a, R2b, R3a, R3b sin aparear)")
    print("=" * 66)
    print(f" {'Tol.':>6} {'Acm peor caso':>14} {'CMRR (Ad=21)':>14} {'vs medida':>12}")
    for f in resultados["peor_caso"]:
        print(
            f" ±{f['tolerancia_pct']:>4.0f}% {f['acm_peor_caso']:>14.4f} "
            f"{f['cmrr_peor_caso_dB']:>11.1f} dB {f['veces_mayor_que_medida']:>9.1f}x"
        )
