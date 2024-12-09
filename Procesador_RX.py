import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.figure import Figure 

class ProcesadorDeImagen:

    def __init__(self, ruta_imagen):
        self.imagen = cv2.imread(ruta_imagen)
        if self.imagen is None:
            raise ValueError("No se pudo cargar la imagen. Verifica la ruta.")
        self.imagen_procesada = self.imagen.copy()

    def mostrar_imagen(self, nombre_ventana="Imagen"):
        """Muestra la imagen procesada."""
        cv2.imshow(nombre_ventana, self.imagen_procesada)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def cambiarBC(self, brillo=0, contraste=0):
        """Cambia el brillo y el contraste de la imagen."""
        if self.imagen_procesada is None:
            raise ValueError("No hay imagen procesada disponible.")
        self.imagen_procesada = cv2.convertScaleAbs(
            self.imagen_procesada, alpha=1 + contraste / 100, beta=brillo
        )
        print("Brillo y contraste ajustados.")

    def aplicar_filtro(self, tipo="blur"):
        """Aplica un filtro a la imagen."""
        if tipo == "blur":
            self.imagen_procesada = cv2.GaussianBlur(self.imagen_procesada, (15, 15), 0)
        elif tipo == "edge":
            self.imagen_procesada = cv2.Canny(self.imagen_procesada, 100, 200)
        elif tipo == "sharpen":
            a = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            self.imagen_procesada = cv2.filter2D(self.imagen_procesada, -1, a)
        else:
            print("Filtro no reconocido. No se realizaron cambios.")
        print(f"Filtro '{tipo}' aplicado.")

    def cambiar_tamano(self, escala=0.5):
        """Cambia el tamaño de la imagen."""
        alto, ancho = self.imagen_procesada.shape[:2]
        nuevo_tamano = (int(ancho * escala), int(alto * escala))
        self.imagen_procesada = cv2.resize(self.imagen_procesada, nuevo_tamano)
        print(f"Imagen redimensionada a escala {escala}.")

    def anotar_en_imagen(self):
        """Permite al usuario dibujar anotaciones sobre la imagen."""
        def poner_circulo(a, x, y, b, c):
            if a == cv2.EVENT_LBUTTONDOWN:
                cv2.circle(self.imagen_procesada, (x, y), 10, (0, 0, 255), -1)
                cv2.imshow("Anotación", self.imagen_procesada)

        cv2.imshow("Anotación", self.imagen_procesada)
        cv2.setMouseCallback("Anotación", poner_circulo)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    # def crear_grafico(self,datos):

    def histograma(self):
        """Muestra el histograma de la imagen procesada."""
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        if len(self.imagen_procesada.shape) == 3:  # Imagen a color
            for i, color in enumerate(['b', 'g', 'r']):
                histograma = cv2.calcHist([self.imagen_procesada], [i], None, [256], [0, 256])
                ax.plot(histograma, color=color)
        else:  # Imagen en escala de grises
            histograma = cv2.calcHist([self.imagen_procesada], [0], None, [256], [0, 256])
            ax.plot(histograma, color='gray')

        ax.set_title("Histograma")
        ax.set_xlabel("Intensidad de píxel")
        ax.set_ylabel("Número de píxeles")
        return fig
    

    def rotar(self, angulo):
        """Rota la imagen por un ángulo dado."""
        alto, ancho = self.imagen_procesada.shape[:2]
        center = (ancho // 2, alto // 2)
        rotacion = cv2.getRotationMatrix2D(center, angulo, 1.0)
        self.imagen_procesada = cv2.warpAffine(self.imagen_procesada, rotacion, (ancho, alto))
        print(f"Imagen rotada {angulo}°.")

    def sobreponer(self, ruta2):
        """Superpone la imagen actual con otra imagen."""
        imagen2 = cv2.imread(ruta2)
        if imagen2 is None:
            raise ValueError("No se pudo cargar la segunda imagen.")
        if self.imagen_procesada.shape != imagen2.shape:
            print("Error: Las imágenes deben tener el mismo tamaño.")
            return
        sobrepuesta = cv2.addWeighted(self.imagen_procesada, 0.5, imagen2, 0.5, 0)
        self.imagen_procesada = sobrepuesta
        print("Imágenes superpuestas.")
    def guardar_imagen(self, ruta_salida):
        """Guarda la imagen procesada en la ruta especificada."""
        if self.imagen_procesada is not None:
            cv2.imwrite(ruta_salida, self.imagen_procesada)  # Guardar la imagen en la ruta dada
        else:
            raise ValueError("No hay una imagen cargada para guardar.")


def main():
    print("\nBienvenido al Procesador de Imágenes Médicas")
    archivo = input("\nIngresa la ruta de la imagen del corazón: ")
    try:
        procesador = ProcesadorDeImagen(archivo)  # Objeto tipo procesador de imágenes
    except ValueError as e:
        print(e)
        return

    while True:
        print("\nMenu:")
        print("1. Cambiar brillo y contraste")
        print("2. Aplicar filtro")
        print("3. Redimensionar imagen")
        print("4. Anotar imagen")
        print("5. Mostrar histograma")
        print("6. Rotar imagen")
        print("7. Superponer dos imágenes")
        print("8. Salir")

        menu = input("\nSelecciona una opción del menu anterior: ")

        if menu == "1":
            brillo = int(input("\nIntroduce el valor de brillo (-100 a 100): "))
            contraste = int(input("Introduce el valor de contraste (-100 a 100): "))
            procesador.cambiarBC(brillo, contraste)
            procesador.mostrar_imagen("Brillo y Contraste")
            continue

        elif menu == "2":
            print("\nFiltros disponibles: blur, edge, sharpen")
            tipo = input("Introduce el tipo de filtro: ")
            procesador.aplicar_filtro(tipo)
            procesador.mostrar_imagen("Filtro Aplicado")
            continue

        elif menu == "3":
            escala = float(input("\nIntroduce el factor de escala (ejemplo: 0.5 para reducir a la mitad): "))
            procesador.cambiar_tamano(escala)
            procesador.mostrar_imagen("Redimensionada")
            continue

        elif menu == "4":
            procesador.anotar_en_imagen()
            continue

        elif menu == "5":
            procesador.histograma()
            continue

        elif menu == "6":
            angulo = float(input("\nIntroduce el ángulo de rotación: "))
            procesador.rotar(angulo)
            procesador.mostrar_imagen(f"Rotación {angulo}°")
            continue

        elif menu == "7":
            other_path = input("\nIngresa la ruta de la segunda imagen: ")
            procesador.sobreponer(other_path)
            procesador.mostrar_imagen("Imágenes Superpuestas")
            continue

        elif menu == "8":
            print("\nSaliendo del programa...")
            break

        else:
            print("\nOpción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()

