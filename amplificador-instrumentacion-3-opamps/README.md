# Amplificador de instrumentación de tres op-amps y rechazo de modo común

[![CI](https://github.com/TU_USUARIO/amplificador-instrumentacion-3-opamps/actions/workflows/ci.yml/badge.svg)](https://github.com/JairL03/amplificador-instrumentacion-3-opamps/actions/workflows/ci.yml)
[![Licencia: MIT](https://img.shields.io/badge/licencia-MIT-blue.svg)](LICENSE)

Repositorio del **Informe de Laboratorio N.º 3** de *Instrumentación Biomédica III*
(Escuela Profesional de Ingeniería Biomédica, Universidad Nacional Mayor de San Marcos, 2026).

Contiene todo lo necesario para **replicar el experimento en tu propio laboratorio**: lista de
materiales, esquemático y lista de conexiones, procedimiento paso a paso con puntos de control,
datos medidos, y el código que reproduce todos los cálculos y figuras del informe.

## ¿Qué se hace en esta práctica?

Se arma sobre protoboard un amplificador de instrumentación de **tres amplificadores operacionales**
(TL084N, ±12 V) con ganancia diferencial de diseño **21** (R1 = R2 = R3 = 10 kΩ, Rg = 1 kΩ) y se
comprueba, a 60 Hz, que:

1. **Amplifica** una señal diferencial pequeña (≈ 10 mVpp, comparable a un biopotencial).
2. **Rechaza** una señal de modo común grande (≈ 1 Vpp, como la interferencia de la red eléctrica).
3. La razón de rechazo de modo común (**CMRR**) medida es coherente con lo esperado.

| Resultado | Valor |
|---|---|
| Ganancia diferencial teórica (resistencias medidas) | 20.969 |
| Ganancia diferencial medida | **20.619** (−1.7 %) |
| Ganancia de modo común medida | 0.0181 |
| CMRR medido | **61.13 dB** (cota inferior) |
| CMRR esperado solo por apareamiento de resistencias | ≈ 82.9 dB |

![Resultados](results/fig12_ganancias.png)

## Empieza aquí

| Quiero… | Ve a |
|---|---|
| Saber qué comprar/conseguir | [`docs/01-materiales.md`](docs/01-materiales.md) |
| Ver el esquemático y las conexiones pin a pin | [`docs/02-circuito.md`](docs/02-circuito.md) |
| Armar y medir paso a paso | [`docs/03-procedimiento.md`](docs/03-procedimiento.md) |
| Resolver un problema en el montaje | [`docs/04-solucion-de-problemas.md`](docs/04-solucion-de-problemas.md) |
| Comparar mis resultados con los del informe | [`docs/05-resultados-esperados.md`](docs/05-resultados-esperados.md) |
| Leer el informe completo | [`informe/Informe_Laboratorio_3-IBI_III.pdf`](informe/Informe_Laboratorio_3-IBI_III.pdf) |

## Replicación en 4 pasos

1. **Consigue** los componentes y equipos de [`docs/01-materiales.md`](docs/01-materiales.md) (≈ 10 resistencias, 1 TL084N, 2 capacitores, protoboard, fuente dual, generador, osciloscopio y multímetro).
2. **Mide y aparea** las resistencias R2a/R2b y R3a/R3b, y arma el circuito siguiendo [`docs/02-circuito.md`](docs/02-circuito.md).
3. **Mide** offset, Etapa B (diferencial) y Etapa C (modo común) siguiendo [`docs/03-procedimiento.md`](docs/03-procedimiento.md).
4. **Calcula** ganancias y CMRR con el código de este repositorio (siguiente sección).

## Reproducir los cálculos y figuras

Requiere Python ≥ 3.10.

```bash
git clone https://github.com/TU_USUARIO/amplificador-instrumentacion-3-opamps.git
cd amplificador-instrumentacion-3-opamps

python -m venv .venv
source .venv/bin/activate          # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .

python -m ai3op                    # tablas 5 y 6 + figuras 12 y 13 en results/
pytest                             # comprueba que se reproducen las cifras del informe
```

Para usar **tus propias mediciones**:

```bash
cp -r data data_mia                # edita los CSV con tus valores (ver data/README.md)
python -m ai3op --datos data_mia --salida results_mia
```

## Estructura del repositorio

```
├── README.md
├── PENDIENTES.md                  ← lista de revisión previa a publicar (borrar al terminar)
├── informe/                       Informe en PDF
├── docs/                          Materiales, circuito, procedimiento, problemas, resultados esperados
├── data/                          Mediciones en CSV (resistencias, osciloscopio, DC, generador)
├── src/ai3op/                     Modelo del circuito, análisis y gráficas
├── tests/                         Pruebas que verifican las cifras del informe
├── results/                       Tablas y figuras generadas por el código
├── media/                         Esquemáticos, fotos del montaje y capturas del osciloscopio
└── .github/                       Integración continua y plantilla de issues
```

## ¿Replicaste el experimento?

Nos interesa comparar resultados. Abre un [issue de replicación](../../issues/new?template=replicacion.md)
con tus valores de Ad y CMRR, el tipo de resistencias que usaste (tolerancia) y, si puedes, una foto o
captura del osciloscopio.

## Limitaciones

* La señal de prueba (60 Hz) coincide con la frecuencia de red, así que no se separa interferencia captada de fuga real de modo común; el CMRR medido es una **cota inferior**.
* Un CMRR de ≈ 61 dB **no es suficiente para un electrocardiógrafo**; se requieren mayor rechazo, blindaje y circuito de pierna derecha.
* Esto es una práctica didáctica, **no un dispositivo médico** y no debe conectarse a personas.

## Autores

* Sotomayor Villanueva, Genny Solangch
* Lázaro Canales, Jair Renato
* Arroyo Ramos, Rosbeth Nayelhy

Grupo L12-A · Docente: Dra. María Elisa Armas Alvarado · Fecha de la práctica: 30/10/2026.

## Licencia y cita

Código, datos y documentación bajo licencia [MIT](LICENSE). Si usas este material, cita
con el archivo [`CITATION.cff`](CITATION.cff) (GitHub muestra el botón «Cite this repository»).
