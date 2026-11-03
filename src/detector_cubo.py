import cv2
import numpy as np

# ============================================================
# CONFIGURACION - Samsung conectado mediante scrcpy
# ============================================================
CAMARA = 9
AREA_MIN_ROJO = 100     # Bajar si se pierde el cubo cuando esta lejos
AREA_MIN_VERDE = 15     # El marcador es mucho mas pequeno
ALTURA_REFERENCIA = 0.35  # Buscar el marcador en el 35% superior
ANCHO_VENTANA = 1100
ALTO_VENTANA = 680
NOMBRE_VENTANA = "Seguimiento del cubo - 2 estaciones"

ROJO = [
    ((0, 80, 65), (15, 255, 255)),
    ((170, 80, 65), (179, 255, 255)),
]
VERDE = [((35, 65, 50), (90, 255, 255))]
KERNEL = np.ones((3, 3), np.uint8)


def mascara_color(hsv, rangos):
    mascara = np.zeros(hsv.shape[:2], dtype=np.uint8)
    for inferior, superior in rangos:
        mascara |= cv2.inRange(
            hsv,
            np.array(inferior, dtype=np.uint8),
            np.array(superior, dtype=np.uint8),
        )
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, KERNEL)
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, KERNEL)
    return mascara


def detectar_mayor(mascara, area_minima):
    contornos, _ = cv2.findContours(
        mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    if not contornos:
        return None
    contorno = max(contornos, key=cv2.contourArea)
    if cv2.contourArea(contorno) < area_minima:
        return None
    m = cv2.moments(contorno)
    if m["m00"] <= 0:
        return None
    x = int(m["m10"] / m["m00"])
    y = int(m["m01"] / m["m00"])
    return contorno, (x, y)


def main():
    cap = cv2.VideoCapture(CAMARA, cv2.CAP_V4L2)
    if not cap.isOpened():
        raise SystemExit("ERROR: No se pudo abrir /dev/video9. Verifica scrcpy.")

    cv2.namedWindow(NOMBRE_VENTANA, cv2.WINDOW_NORMAL)
    limite_x = None
    estacion_anterior = None
    tamano_ventana = None
    print("Seguimiento activo. El marcador verde separa las estaciones.")
    print("Q: salir")

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("No se pudo recibir video.")
                break

            alto, ancho = frame.shape[:2]
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Buscar el pequeno marcador VERDE cerca del borde superior.
            mask_verde = mascara_color(hsv, VERDE)
            mask_verde[int(alto * ALTURA_REFERENCIA):, :] = 0
            marcador = detectar_mayor(mask_verde, AREA_MIN_VERDE)
            if marcador is not None:
                _, (x_verde, y_verde) = marcador
                limite_x = (x_verde if limite_x is None
                            else round(0.7 * limite_x + 0.3 * x_verde))
            else:
                x_verde = y_verde = None

            # Buscar el cubo ROJO dentro de la imagen original.
            mask_rojo = mascara_color(hsv, ROJO)
            cubo = detectar_mayor(mask_rojo, AREA_MIN_ROJO)

            # Dibujar los DOS RECTANGULOS de estacion si hay referencia.
            if limite_x is not None:
                cv2.rectangle(frame, (1, 1), (limite_x - 1, alto - 2),
                              (0, 220, 255), 2)
                cv2.rectangle(frame, (limite_x, 1), (ancho - 2, alto - 2),
                              (255, 190, 0), 2)
                cv2.line(frame, (limite_x, 0), (limite_x, alto - 1),
                         (0, 255, 255), 2)
                cv2.putText(frame, "ESTACION 1", (12, 28),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 220, 255), 2)
                cv2.putText(frame, "ESTACION 2", (min(limite_x + 12, ancho - 160), 28),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 190, 0), 2)

            if marcador is not None:
                cv2.circle(frame, (x_verde, y_verde), 12, (0, 255, 0), 2)
                cv2.circle(frame, (x_verde, y_verde), 3, (255, 255, 255), -1)

            estacion = None
            posicion = "X: --   Y: --"
            if cubo is not None:
                contorno, (cx, cy) = cubo
                x, y, w, h = cv2.boundingRect(contorno)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.drawMarker(frame, (cx, cy), (255, 255, 255),
                               cv2.MARKER_CROSS, 18, 2)
                posicion = f"X: {cx}   Y: {cy}"
                if limite_x is not None:
                    estacion = 1 if cx < limite_x else 2

            if estacion != estacion_anterior:
                if estacion is not None:
                    print(f"Cubo en ESTACION {estacion}")
                estacion_anterior = estacion

            if cubo is None:
                estado = "CUBO ROJO NO DETECTADO"
            elif limite_x is None:
                estado = "BUSCANDO REFERENCIA VERDE"
            else:
                estado = f"CUBO EN ESTACION {estacion}"

            if limite_x is not None and marcador is None:
                estado += " | REFERENCIA VERDE TEMPORALMENTE PERDIDA"

            # Barra superior sin tapar el video, coordenadas del original.
            panel = np.full((alto + 68, ancho, 3), (29, 29, 29), dtype=np.uint8)
            panel[68:, :, :] = frame
            cv2.putText(panel, estado, (12, 24),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
            cv2.putText(panel, f"{posicion} px | Q: salir", (12, 52),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.54, (0, 255, 255), 2)

            # Agrandar sin alterar las coordenadas medidas.
            h_panel, w_panel = panel.shape[:2]
            factor = min(ANCHO_VENTANA / w_panel, ALTO_VENTANA / h_panel)
            nuevo_ancho = int(w_panel * factor)
            nuevo_alto = int(h_panel * factor)
            panel = cv2.resize(panel, (nuevo_ancho, nuevo_alto),
                               interpolation=cv2.INTER_LINEAR)
            if (nuevo_ancho, nuevo_alto) != tamano_ventana:
                cv2.resizeWindow(NOMBRE_VENTANA, nuevo_ancho, nuevo_alto)
                tamano_ventana = (nuevo_ancho, nuevo_alto)
            cv2.imshow(NOMBRE_VENTANA, panel)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Detector finalizado.")


if __name__ == "__main__":
    main()
