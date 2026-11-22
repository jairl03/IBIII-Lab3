# 1. Materiales y equipos

## Componentes

| Ref. | Componente | Cant. | Notas |
|---|---|---|---|
| U1 | **TL084N** (cuádruple op-amp, entrada JFET, DIP-14) | 1 | Se usan 3 de los 4 amplificadores (A1, A2, A3). El cuarto se deja como seguidor con la entrada no inversora a GND para que no oscile. Cualquier cuádruple JFET equivalente (p. ej. TL074) sirve. |
| R1a, R1b | Resistencia 10 kΩ | 2 | Realimentación de la primera etapa |
| R2a, R2b | Resistencia 10 kΩ | 2 | Entradas del restador (**aparear por medición**) |
| R3a, R3b | Resistencia 10 kΩ | 2 | Divisor a GND y realimentación del restador (**aparear por medición**) |
| Rg | Resistencia 1 kΩ | 1 | Fija la ganancia de la primera etapa |
| RD1 | Resistencia 10 kΩ | 1 | Divisor de entrada, **solo Etapa B** |
| RD2 | Resistencia 100 Ω | 1 | Divisor de entrada, **solo Etapa B** |
| C1, C2 | Capacitor cerámico 100 nF | 2 | Desacople de alimentación: C1 de +12 V a GND, C2 de −12 V a GND, lo más cerca posible del integrado |
| — | Protoboard | 1 | Marca/modelo: *completar* |
| — | Cables jumper macho-macho | ≈ 20 | |
| — | Cable BNC–caimán | 1 | Generador → circuito |

> **Tolerancia.** En el informe las resistencias medidas se desvían hasta −2.5 % de su valor
> nominal (Rg) y −1.9 % (R3a), lo que indica componentes de **5 %**. Con resistencias de 1 % o mejor
> se obtiene un CMRR de peor caso mayor (ver `docs/05-resultados-esperados.md`). Para replicar el
> experimento tal cual, 5 % es suficiente **siempre que se aparee por medición** (paso 1 del procedimiento).

## Equipos

| Equipo | Modelo usado | Ajustes relevantes |
|---|---|---|
| Fuente de alimentación dual | *completar marca/modelo* | Modo dual (tracking) a **±12 V**, verificada en ±12.00 V con el multímetro |
| Generador de funciones | *completar marca/modelo* | Senoidal, **60 Hz**, **1 Vpp**, offset 0 V, carga **High-Z** |
| Osciloscopio | Keysight InfiniiVision DSOX1202G (2 canales, 200 MHz, 2 GSa/s) | Puntas en ×1; CH2 con acoplamiento CC |
| Multímetro | Fluke 179 True RMS | Medición de resistencias, alimentación y offset de VOUT |

## Software (solo para reproducir el análisis)

* Python ≥ 3.10 con `numpy` y `matplotlib` (ver `requirements.txt`).
* Opcional: [EasyEDA](https://easyeda.com/) para abrir/rehacer los esquemáticos (las imágenes están en `media/`).

## Precauciones

* Apaga la fuente antes de modificar el cableado.
* Verifica la polaridad de la alimentación **antes** de conectar el integrado: pin 4 = +12 V, pin 11 = −12 V.
* No superes ±18 V (límite absoluto del TL084).
