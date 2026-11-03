"""Prototipo básico de detección por color (código de referencia).

Reconstrucción de la versión mostrada y probada durante las sesiones del
2 de noviembre; no sustituye el archivo original del equipo.
"""
import cv2
import numpy as np

CAMARA = 9
AREA_MINIMA = 400
ANCHO_MAXIMO = 1080
ALTO_MAXIMO = 600
COLOR_INICIAL = "rojo"
COLORES = {
    "rojo": [((0, 100, 70), (10, 255, 255)),
             ((170, 100, 70), (179, 255, 255))],
    "verde": [((35, 70, 60), (85, 255, 255))],
    "azul": [((95, 80, 60), (130, 255, 255))],
}
KERNEL = np.ones((5, 5), dtype=np.uint8)
NOMBRE = "Detector de cubos - prueba basica"


def main():
    cap = cv2.VideoCapture(CAMARA, cv2.CAP_V4L2)
    if not cap.isOpened():
        raise SystemExit("No se pudo conectar con la camara virtual /dev/video9")
    color = COLOR_INICIAL
    cv2.namedWindow(NOMBRE, cv2.WINDOW_NORMAL)
    print("R: rojo | G: verde | B: azul | Q: salir")
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("No se pudo recibir video")
                break
            alto, ancho = frame.shape[:2]
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mascara = np.zeros((alto, ancho), dtype=np.uint8)
            for inferior, superior in COLORES[color]:
                parcial = cv2.inRange(hsv, np.array(inferior, np.uint8),
                                           np.array(superior, np.uint8))
                mascara = cv2.bitwise_or(mascara, parcial)
            mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, KERNEL)
            mascara = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, KERNEL)
            contornos, _ = cv2.findContours(
                mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            detectado = False
            etiqueta = "X: --  Y: --"
            if contornos:
                objeto = max(contornos, key=cv2.contourArea)
                if cv2.contourArea(objeto) >= AREA_MINIMA:
                    momento = cv2.moments(objeto)
                    if momento["m00"] > 0:
                        cx = int(momento["m10"] / momento["m00"])
                        cy = int(momento["m01"] / momento["m00"])
                        x, y, w, h = cv2.boundingRect(objeto)
                        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
                        cv2.drawMarker(frame, (cx,cy), (255,255,255),
                                       cv2.MARKER_CROSS, 12, 2)
                        etiqueta = f"X: {cx}  Y: {cy}"
                        detectado = True
            cv2.rectangle(frame, (0,0), (ancho, min(85,alto)), (35,35,35), -1)
            cv2.putText(frame, f"COLOR: {color.upper()}", (10,23),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
            cv2.putText(frame, etiqueta, (10,49), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (0,255,255), 2)
            cv2.putText(frame, "OBJETO DETECTADO" if detectado else "BUSCANDO OBJETO",
                        (10,75), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0,255,0) if detectado else (0,0,255), 1)
            escala = min(ANCHO_MAXIMO/ancho, ALTO_MAXIMO/alto)
            tamano = (max(1,int(ancho*escala)), max(1,int(alto*escala)))
            cv2.resizeWindow(NOMBRE, *tamano)
            cv2.imshow(NOMBRE, cv2.resize(frame, tamano))
            tecla = cv2.waitKey(1) & 0xFF
            if tecla == ord("q"):
                break
            if tecla == ord("r"):
                color = "rojo"
            elif tecla == ord("g"):
                color = "verde"
            elif tecla == ord("b"):
                color = "azul"
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
