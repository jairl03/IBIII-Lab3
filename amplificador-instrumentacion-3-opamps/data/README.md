# Datos medidos

Todos los valores provienen del Informe de Laboratorio N.º 3 (30/10/2026).
Las tensiones están en **volts** y las resistencias en **ohms**, sin prefijos,
para que los scripts los lean sin conversiones.

| Archivo | Contenido |
|---|---|
| `resistencias_medidas.csv` | Valor nominal y valor medido (Fluke 179) de cada resistencia. |
| `mediciones_osciloscopio.csv` | Vpp de entrada y salida en las Etapas B y C, frecuencia leída y escalas del osciloscopio. |
| `mediciones_dc.csv` | Tensiones de alimentación y offset de VOUT con las entradas a GND. |
| `configuracion_generador.csv` | Ajustes del generador de funciones. |

## Cómo usar tus propios datos

1. Copia esta carpeta (`cp -r data data_mia`).
2. Reemplaza los valores por los que **tú mediste** con tu protoboard. No cambies los nombres de columnas ni de componentes.
3. Ejecuta `python -m ai3op --datos data_mia --salida results_mia`.

Si dejas vacía la columna `fase_salida_vs_V1_deg` el script simplemente la ignora.
