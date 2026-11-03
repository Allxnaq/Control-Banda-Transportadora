# Plan de pruebas — 04-11-2026

**Estado:** plan para la sesión grupal; no equivale a resultados ejecutados.

## Propósito

Comparar la captura con smartphone y la alternativa de cuatro webcams sobre la banda montada. Verificar reconocimiento, estaciones, registro temporal y viabilidad del control.

## Protocolo

1. **Montaje:** fijar la cámara; medir largo útil, posiciones de estaciones y diámetro de polea. Registrar tipo de motor y fuente.
2. **Transmisión:** confirmar estabilidad de captura de smartphone durante una corrida; anotar resolución, FPS aproximados y fallos.
3. **Color:** desplazar el cubo desde inicio hasta el extremo; comprobar falsos positivos y pérdidas por distancia/iluminación.
4. **Dos estaciones:** validar marcador verde; comprobar que la clasificación cambia solo cuando el centroide cruza la división.
5. **Cuatro estaciones:** definir cuatro referencias y comprobar detección secuencial sin saltos.
6. **Registro temporal:** verificar si se puede guardar un evento por estación y evitar duplicación (pendiente de programar).
7. **Alternativa webcam:** si el teléfono no es confiable, conectar 1, 2 y luego 4 webcams; evaluar índices V4L2 y estabilidad simultánea.
8. **Motor y seguridad:** identificar corriente de trabajo y de arranque; no conectar el motor a la IdeaBoard hasta verificar la capacidad del puente H. Comprobar parada manual y condiciones de avance.
9. **Evidencia:** grabar material del sistema abierto/sin compensación y más adelante con compensador, según exige el proyecto.

## Tabla para completar durante la sesión

| Prueba | Responsable | Resultado | Evidencia | Problemas / acción |
| --- | --- | --- | --- | --- |
| Cámara teléfono | Por asignar | Pendiente | — | — |
| Seguimiento color a distancia | Por asignar | Pendiente | — | — |
| División en 2 estaciones | Por asignar | Pendiente | — | — |
| Clasificación en 4 estaciones | Por asignar | Pendiente | — | — |
| Webcams simultáneas (si aplica) | Por asignar | Pendiente | — | — |
| Motor + IdeaBoard | Por asignar | Pendiente | — | — |

## Criterios mínimos de éxito a definir con el equipo

- Frecuencia de captura suficiente para la velocidad real de la banda.
- Cada transición de estación se registra una sola vez y en orden.
- Ante pérdida de detección, no se autoriza avanzar ciegamente.
- La salida solo se habilita con E1, E2, E3 y E4 validadas.
- Los resultados se documentan con fecha, participantes y commit relevante.
