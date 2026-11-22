# 4. Solución de problemas

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| VOUT en ≈ +11 V o −11 V con entradas a GND | Salida saturada: alimentación mal conectada, op-amp sin realimentación o resistencia mal colocada | Apaga. Revisa pines 4 y 11, que Rg/R1a/R1b estén en los nodos NA/NB y que R3b realimente de pin 8 a pin 9. |
| Offset de VOUT de cientos de mV | Cableado incorrecto o un op-amp dañado | Revisa que V1 y V2 estén realmente a GND y no flotando; prueba otro integrado. |
| No hay señal en VOUT en la Etapa B | Divisor mal conectado, generador desactivado o punta en la escala equivocada | Comprueba V1 en CH1. Con 1 Vpp y el divisor debe verse ≈ 10 mVpp. |
| La amplitud en V1 es la mitad o el doble de lo esperado | Carga del generador en 50 Ω en vez de **High-Z** | Cambia la carga a High-Z en el menú del generador. |
| Ganancia muy distinta de 21 (± más de 5 %) | Valor de Rg, R1 o R3/R2 equivocado; resistencias sin medir | Mide de nuevo. Con Rg = 1 kΩ y R1 = 10 kΩ la primera etapa debe dar ≈ 21. |
| Traza de V1 muy ruidosa (≈ 10 mV) | Señal pequeña, cables largos, red de 60 Hz acoplada | Usa el modo Promedio, cables cortos, tierra común y la punta con el resorte de tierra corto. |
| VOUT grande en la Etapa C (CMRR bajo) | R2a/R2b o R3a/R3b sin aparear; V1 y V2 no unidos de verdad | Reaparea las resistencias; confirma con el multímetro que V1 y V2 están al mismo nodo. |
| VOUT en la Etapa C se mezcla con ruido de 60 Hz | La señal de prueba tiene la misma frecuencia que la red; no se separa interferencia captada de fuga de modo común | Repite la medición a 100 Hz o 1 kHz y compara. |
| El osciloscopio muestra una oscilación de alta frecuencia en VOUT | Falta desacople o cables largos | Acerca C1 y C2 al integrado y acorta los cables. |
| La salida está invertida respecto a lo esperado | Las ramas inversora/no inversora de A3 están intercambiadas (o V1/V2) | Revisa qué salida (O1 u O2) llega a pin 9 y cuál a pin 10; ver `docs/02-circuito.md`. |
