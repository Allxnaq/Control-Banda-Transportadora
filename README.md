# Control de banda transportadora mediante visión artificial

**Curso:** Control Automático · II Semestre 2026 · Tecnológico de Costa Rica  
**Proyecto:** Línea de producción con cuatro estaciones  
**Estado:** Prototipo de visión probado; control de banda e integración pendientes.

## Descripción

Proyecto académico de una banda transportadora de pequeña escala que desplaza una muestra (un cubo ligero) por **cuatro estaciones consecutivas**. El sistema debe localizar la muestra, registrar su paso por cada estación con fecha y hora y **autorizar la salida solo después de validar la secuencia completa 1 → 2 → 3 → 4**.

El profesor autorizó reemplazar la lectura de QR del planteamiento original por **detección por color**. La solución principal bajo evaluación usa una cámara Android fija sobre la banda y Python/OpenCV en una PC. También se contempla como alternativa utilizar cuatro webcams USB, una por estación. El registro y la lógica de autorización deben funcionar independientemente de la alternativa elegida.

**Alcance actual:** seguimiento visual de un solo cubo de color reconocible. Si más adelante se procesan varios cubos idénticos simultáneamente, la detección por color **no permite distinguir por sí sola el ID de cada muestra**: hará falta un mecanismo de identificación/seguimiento adicional, o procesar las muestras de una en una.

## Integrantes

- Santiago Chavarría Azofeifa
- Allan Arrieta Quirós
- Ennos Saldaña Caseres
- Jose Emanuel Varela Sobalvarro
- Esteban Vargas Fernández

## Arquitectura prevista

1. **Captura:** Samsung Android mediante scrcpy y cámara virtual V4L2 (`/dev/video9`) o webcams USB.
2. **Visión:** Python/OpenCV convierte fotogramas de BGR a HSV, filtra colores y calcula el centroide `(X, Y)`.
3. **Estaciones:** zonas de la imagen asociadas a estaciones de la banda (inicialmente dos para la prueba con marcador verde; objetivo: cuatro).
4. **Registro:** guardar identificador de muestra, estación, fecha, hora y orden de visita (**pendiente**).
5. **Control:** enviar órdenes por USB serial a una CRCibernética IdeaBoard (ESP32) que acciona un solo motor de banda (**pendiente**).
6. **Seguridad lógica:** impedir el avance final si falta alguna visita; detenerse ante pérdidas de seguimiento (**pendiente de implementación y pruebas**).

## Estado de avance (03-11-2026)

| Funcionalidad | Estado |
| --- | --- |
| Cámara Android → scrcpy → V4L2 → OpenCV | Probada con video en vivo |
| Segmentación HSV y centroide del objeto rojo | Probada en capturas compartidas |
| Ventana de detección ampliada | Probada |
| Detectar un marcador verde para dividir dos estaciones | Código preparado; **sin validación reportada** |
| Cuatro estaciones con registro cronológico | Pendiente |
| Movimiento de motor por IdeaBoard | Pendiente |
| Compensador, simulación y comparación sin/con control | Pendiente |
| Alternativa de cuatro webcams | Pendiente de prueba |

## Estructura

```text
src/
  detector_color_basico.py  # versión básica reconstruida del prototipo probado
  detector_cubo.py          # propuesta de detección de dos estaciones (sin validar)
docs/
  BITACORA.md              # cronología real y tareas por confirmar
  PLAN_PRUEBAS.md          # guía para sesión del 04-11-2026
pruebas/
  README.md                # formato para registrar resultados de pruebas
requirements.txt
.gitignore
```

## Preparar el entorno (CachyOS)

**Requisitos:** Python 3, OpenCV, NumPy, ADB, scrcpy, `v4l2loopback` y un Android compatible. En las pruebas iniciales se utilizaron OpenCV **5.0.0**, NumPy **2.5.4**, scrcpy **5.0.1** y `/dev/video9`.

En CachyOS/Arch, las bibliotecas pueden instalarse con:

```bash
sudo pacman -S python-opencv python-numpy scrcpy android-tools v4l-utils
```

Preparar la cámara virtual solo si todavía no está creada (evitar ejecutar `modprobe -r` mientras se está usando):

```bash
sudo modprobe v4l2loopback video_nr=9 card_label=AndroidCam exclusive_caps=0
adb devices
```

Con el teléfono conectado y autorizado, en la **primera terminal**:

```bash
scrcpy --video-source=camera --camera-facing=back \
  --no-audio --max-size=640 --v4l2-sink=/dev/video9
```

En la **segunda terminal**:

```bash
python src/detector_color_basico.py
# o probar la propuesta de dos estaciones:
python src/detector_cubo.py
```

La cámara virtual usa el índice `9` dentro de los programas. Si la webcam se enumera de otra manera, cambiar `CAMARA` en el archivo correspondiente.

Para terminar: cerrar los programas, ejecutar `adb kill-server` y desactivar la depuración USB en Android.

## Limitaciones conocidas

- La detección puede fallar cuando el cubo se aleja o cambia la iluminación.
- El umbral mínimo de área y los rangos HSV necesitan calibración sobre la banda final.
- La coordenada está en **píxeles**, todavía no convertida a distancia física.
- La captura del smartphone y el procesamiento visual introducen retardos aún no medidos.
- El código actual **no controla el motor** ni registra visitas de cuatro estaciones.
- El análisis de control debe actualizarse con los componentes físicos y tiempos de muestreo reales; no basta con reutilizar el modelo preliminar.

## Registro y entregables

El proyecto exige informe matemático (modelo y compensador), bitácora, repositorio Git con contribución de cada integrante, videos **sin control versus con control** y exposición final. Ver [`docs/BITACORA.md`](docs/BITACORA.md) para el historial y [`docs/PLAN_PRUEBAS.md`](docs/PLAN_PRUEBAS.md) para el plan de la sesión siguiente.

> Este repositorio documenta un **trabajo en progreso**: no se atribuyen como realizadas pruebas que el equipo todavía no ha confirmado.
