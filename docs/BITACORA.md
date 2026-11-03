# Bitácora de trabajo — Control de banda transportadora

**Curso:** Control Automático · II Semestre 2026  
**Equipo:** Santiago Chavarría Azofeifa, Allan Arrieta Quirós, Ennos Saldaña Caseres, Jose Emanuel Varela Sobalvarro y Esteban Vargas Fernández.

**Criterio:** registrar la fecha real, el responsable, la acción, la evidencia y los pendientes. Los eventos retrospectivos de esta primera versión se basan en el intercambio de desarrollo y deben ser ratificados por los integrantes. No inventar horas, reuniones ni aportes.

## Registro cronológico inicial

| Fecha | Responsable / fuente | Actividad | Resultado / evidencia | Estado |
| --- | --- | --- | --- | --- |
| 02-11-2026 | Emanuel (trabajo documentado en el chat) | Preparación de cámara Samsung Android por USB, ADB y scrcpy; cámara virtual `v4l2loopback` en `/dev/video9`. | Video visualizado desde OpenCV en CachyOS. | Probado |
| 02-11-2026 | Emanuel (trabajo documentado en el chat) | Creación de `detector_cubo.py`, segmentación HSV rojo/verde/azul, extracción de contornos, centroide y recuadro. | Capturas del cubo rojo detectado con coordenadas en tiempo real. | Probado, con fallos a distancia |
| 02-11-2026 | Emanuel (trabajo documentado en el chat) | Ajuste de la interfaz a pantalla de laptop. | Se muestra una ventana más grande con estado de detección y coordenadas. | Probado |
| 02-11-2026 | Emanuel / propuesta generada durante el trabajo | División inicial de dos estaciones mediante marcador verde y clasificación del cubo rojo. | Código preparado para prueba; no se informó ejecución satisfactoria. | Pendiente de validar |
| 03-11-2026 | Allan (organización documentada en este intercambio) | Revisión de entregables oficiales y organización del repositorio Git, README y bitácora. | Archivos iniciales preparados para publicación. | Preparado; publicación remota pendiente |
| 03-11-2026 | Grupo (decisión comunicada por Allan) | Plan de probar el teléfono con la banda física y considerar cuatro webcams como alternativa. | Sesión acordada para el 04-11-2026. | Programado, no ejecutado |

## Registro de tareas por integrante

| Integrante | Contribución registrada hasta ahora | Pendiente de confirmar/asignar |
| --- | --- | --- |
| Jose Emanuel Varela Sobalvarro | Prototipo de captura y detección por color; propuesta de dos estaciones. | Validación con banda real |
| Allan Arrieta Quirós | Recopilación de requisitos; organización inicial de README, bitácora y repositorio. | Publicar y compartir repositorio |
| Santiago Chavarría Azofeifa | No documentada en este registro inicial. | Registrar tareas efectivamente realizadas |
| Ennos Saldaña Caseres | No documentada en este registro inicial. | Registrar tareas efectivamente realizadas |
| Esteban Vargas Fernández | No documentada en este registro inicial. | Registrar tareas efectivamente realizadas |

## Para agregar una sesión nueva

**Fecha y hora:** __ / __ / ____ — __:__  
**Participantes:**  
**Objetivo:**  
**Actividades desarrolladas (quién hizo qué):**  
**Decisiones y razones:**  
**Resultados medibles / evidencia (captura, archivo, video, commit):**  
**Dificultades / fallos:**  
**Próximos pasos y responsables:**

## Criterio para el historial Git

Cada integrante debe crear sus propios commits con su cuenta y trabajo real. No fabricar commits ni adjudicarle a una persona aportes de otra; documentar contribuciones de montaje, electrónica, pruebas y redacción en la bitácora aunque no sean código.
