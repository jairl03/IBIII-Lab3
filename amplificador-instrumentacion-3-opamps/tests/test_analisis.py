"""Comprueba que el código reproduce las cifras publicadas en el informe."""

from pathlib import Path

import pytest

from ai3op import analisis, datos, modelo

DATOS = Path(__file__).resolve().parents[1] / "data"


@pytest.fixture(scope="module")
def res():
    return analisis.calcular(DATOS)


@pytest.fixture(scope="module")
def r():
    return datos.cargar_resistencias(DATOS)


# ----------------------------------------------------------- Tabla 5
def test_ganancia_primera_etapa(res):
    assert res["resumen"]["ganancia_primera_etapa"] == pytest.approx(21.236, abs=5e-4)


def test_razones_restador(res):
    assert res["resumen"]["ka"] == pytest.approx(0.98593, abs=5e-6)
    assert res["resumen"]["kb"] == pytest.approx(0.98893, abs=5e-6)


def test_ad_teorica(res):
    assert res["resumen"]["ad_teorica"] == pytest.approx(20.969, abs=5e-4)


def test_ad_medida(res):
    assert res["resumen"]["ad_medida"] == pytest.approx(20.619, abs=5e-4)
    assert res["resumen"]["ad_dif_vs_teorica_pct"] == pytest.approx(-1.7, abs=0.05)


def test_acm_y_cmrr_medidos(res):
    s = res["resumen"]
    assert s["acm_medida"] == pytest.approx(0.0181, abs=5e-5)
    assert s["cmrr_medido_dB"] == pytest.approx(61.13, abs=0.01)
    assert s["ganancia_dif_dB"] == pytest.approx(26.3, abs=0.05)
    assert s["ganancia_cm_dB"] == pytest.approx(-34.8, abs=0.05)


def test_apareamiento(res):
    s = res["resumen"]
    assert s["acm_restador_informe"] == pytest.approx(0.00151, abs=5e-6)
    assert s["cmrr_esperado_por_apareamiento_dB"] == pytest.approx(82.9, abs=0.1)
    assert s["cmrr_restador_dB"] + s["cmrr_primera_etapa_dB"] == pytest.approx(82.9, abs=0.1)


def test_ecuacion_exacta_coincide_con_la_del_informe(res):
    s = res["resumen"]
    assert s["acm_restador_exacta"] == pytest.approx(s["acm_restador_informe"], rel=5e-3)  # el informe redondea (kb - ka) a 0.00300


def test_valores_secundarios(res):
    s = res["resumen"]
    assert s["modo_comun_equivalente_entrada_Vpp"] * 1e3 == pytest.approx(0.92, abs=0.01)
    assert s["offset_referido_a_entrada_V"] * 1e3 == pytest.approx(0.7, abs=0.05)
    assert s["factor_entrada_C_sobre_B"] == pytest.approx(93, abs=1)
    assert s["factor_salida_B_sobre_C"] == pytest.approx(12.3, abs=0.1)


# ----------------------------------------------------------- Tabla 6
def test_peor_caso(res):
    pc = {round(f["tolerancia_pct"]): f for f in res["peor_caso"]}
    assert pc[5]["acm_peor_caso"] == pytest.approx(0.105, abs=1e-3)
    assert pc[5]["cmrr_peor_caso_dB"] == pytest.approx(46.0, abs=0.1)
    assert pc[1]["acm_peor_caso"] == pytest.approx(0.0202, abs=2e-4)
    assert pc[1]["cmrr_peor_caso_dB"] == pytest.approx(60.3, abs=0.1)


# ----------------------------------------------------------- modelo
def test_modelo_nominal():
    assert modelo.ad_nominal() == 21.0


def test_modelo_ideal_resistencias_perfectas():
    ideal = {k: v for k, v in zip(["R1a", "R1b", "Rg", "R2a", "R2b", "R3a", "R3b"], [10e3, 10e3, 1e3, 10e3, 10e3, 10e3, 10e3])}
    # La diferencia V1 - V2 se amplifica 21 veces y el modo común se anula por completo.
    assert abs(modelo.vout_ideal(0.010, 0.0, ideal)) == pytest.approx(0.21, rel=1e-9)
    assert modelo.vout_ideal(0.5, 0.5, ideal) == pytest.approx(0.0, abs=1e-12)


def test_modelo_ideal_con_resistencias_medidas(r):
    ad = abs(modelo.vout_ideal(0.001, 0.0, r)) / 0.001
    acm = abs(modelo.vout_ideal(1.0, 1.0, r)) / 1.0
    assert ad == pytest.approx(20.97, abs=0.02)
    assert acm == pytest.approx(0.00151, abs=5e-5)


def test_divisor_etapa_b(res):
    assert res["resumen"]["v1_esperada_Vpp"] * 1e3 == pytest.approx(9.69, abs=0.01)
