# Pendientes antes de publicar  (borra este archivo al terminar)

Búscalos rápido con: `grep -rn "POR CONFIRMAR\|completar\|TU_USUARIO" .`

## 1. ⚠️ Fase de VOUT frente a V1 (importante)

El esquemático (Fig. 3, 8 y 9) conecta **O1 → R2a → pin 10 (+)** y **O2 → R2b → pin 9 (−)** de A3.
Con esa conexión, `Vout = +Ad·(V1 − V2)`: con V2 a GND la salida debería estar **en fase** con V1.
Pero el informe indica y la captura de la Fig. 6 muestra **contrafase (180°)**, y escribe `Vout = Ad·(V2 − V1)`
y que «la salida de A1 alimenta la entrada inversora de A3».

Revisen y resuelvan una de estas dos opciones:

- [ ] **El protoboard tiene A1 → pin 9 y A2 → pin 10** (intercambiado respecto al esquemático). Corregir los esquemáticos
      (Fig. 3, 8, 9), la tabla de nodos de `docs/02-circuito.md`, y los roles en `data/resistencias_medidas.csv`.
- [ ] **El protoboard coincide con el esquemático.** Entonces la inversión viene de otra causa (por ejemplo, el canal 2
      del osciloscopio con **«Inverso»** activado, o la punta invertida). Repetir la captura de la Etapa B y corregir
      la explicación de la sección 5.2 del informe.

Después actualicen la nota «⚠️ POR CONFIRMAR» de `docs/02-circuito.md` y de `docs/03-procedimiento.md`.

## 2. Datos que faltan

- [ ] Marca/modelo del protoboard, fuente dual y generador de funciones (`docs/01-materiales.md` y Tabla 8 del informe).
- [ ] Tabla 9 del informe (archivos y enlace al repositorio) y el enlace a fotos/videos: ahora puede llenarse con la URL de este repo.

## 3. Detalles menores del informe

- [ ] El esquemático rotula **TL084IN**; la lista de materiales dice **TL084N**. Unificar.
- [ ] Ecuación (5): el análisis nodal da `(ka − kb)/(1 + ka)`; el informe usa `(kb − ka)/(1 + kb)`. Numéricamente es igual (diferencia < 0.2 %).
- [ ] La fecha/hora del osciloscopio en las capturas (01/11/2026 02:33) no coincide con la fecha de la práctica (30/10/2026, 14:00–16:00): es solo el reloj del equipo, pero puede generar preguntas.
- [ ] Las cifras de datasheet de las preguntas 2 y 5 (CMRR del TL084, INA128, AD620) no fueron verificadas aquí contra los documentos de TI y Analog Devices; confírmenlas antes de difundir.
- [ ] Los «rangos razonables» de `docs/05-resultados-esperados.md` son criterios orientativos propios, no valores de la guía del curso.

## 4. Publicación

- [ ] Reemplazar `TU_USUARIO` en `README.md` y `CITATION.cff`.
- [ ] Confirmar la ortografía del nombre de la primera integrante («Solangch») y que todas aceptan figurar en un repositorio público.
- [ ] Los códigos de estudiante **no** se incluyeron a propósito (privacidad). Agréguenlos solo si quieren.
- [ ] Confirmar con la docente que se puede publicar el informe y las figuras.
