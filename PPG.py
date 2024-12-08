#Librerias
import os
import seaborn as sns
sns.set_style("darkgrid")
import pandas as pd
pd.set_option('display.max_columns', None)
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("darkgrid")
from scipy.signal import butter, filtfilt
from scipy import stats
from scipy.io import loadmat
from collections import Counter
import warnings
warnings.filterwarnings("ignore")
import wfdb

PPG=[]
class PPG:
    def __init__(self):
        # Inicializa los atributos de la clase.
        self.__señalppg = None  # Señal PPG sin procesar
        self.__señalppgdf = None  # Señal PPG convertida a DataFrame

    # Método para buscar y abrir archivos de datos de PPG
    def AbrirArchivo(self):
        directorio = r"C:/Users/josem/OneDrive/Documentos/Maria  Rosa/PPG/PPG_Dataset/brno-university-of-technology-smartphone-ppg-database-but-ppg-2.0.0"
        archivos_ppg = []  # Lista para almacenar las rutas de archivos PPG

        # Recorre los subdirectorios y archivos en el directorio
        for ruta_actual, subcarpetas, archivos in os.walk(directorio):
            for archivo in archivos:
                ruta_archivo = os.path.join(ruta_actual, archivo)
                if archivo.endswith('PPG.dat'):  # Filtra archivos con extensión .dat
                    archivos_ppg.append(ruta_archivo)

        return archivos_ppg  # Retorna la lista de archivos encontrados

    # Método para abrir archivos según su formato
    def openfile(self, file):
        if file.endswith(".csv"):
            print(f"Archivo CSV encontrado: {file}")
            contenido = pd.read_csv(file)  # Asegúrate de importar pandas como pd
            print(contenido.head())
            return contenido  # Devuelve el DataFrame
        elif file.endswith(".mat"):
            print(f"Archivo MAT encontrado: {file}")
            contenido = loadmat(file)
            print(contenido.keys())  # Muestra las claves del archivo MAT
            return contenido
        elif file.endswith("PPG.dat"):
            print(f"Archivo DAT encontrado: {file}")
            with open(file, 'r', encoding='utf8') as contenido:
                datos = contenido.readlines()
                print(datos[:5])  # Muestra las primeras 5 líneas
                return datos  # Retorna los datos leídos
        else:
            print("Formato de archivo no soportado.")
            return None


    # Asigna una señal al atributo de la clase y la convierte a DataFrame
    def Asignarseñal(self, señal):
        self.__señalppg = señal  # Asigna la señal cruda
        self.__señalppgdf = pd.DataFrame(señal)  # Crea un DataFrame
        return señal, self.__señalppgdf

    # Retorna el DataFrame de la señal
    def VerSeñalframe(self):
        return self.__señalppgdf

    # Retorna la señal cruda
    def VerSeñalPPG(self):
        return self.__señalppg

    # Imprime propiedades de la señal
    def VerPropiedades(self):
        if self.__señalppg is not None:
            print(f'La señal ingresada tiene {self.__señalppg.shape[0]} muestras.')

    # Grafica una fila específica de un archivo proporcionado
    def graficarseñal(self, archivo, fila):
        try:
            # Verifica que el archivo sea un DataFrame
            if isinstance(archivo, pd.DataFrame):
                if fila < len(archivo):
                    señal = archivo.iloc[fila, :-1]  # Excluye la última columna si no es parte de la señal
                    plt.plot(señal)
                    plt.title(f"Señal PPG - Paciente {fila}")
                    plt.xlabel("Tiempo (o índice de columna)")
                    plt.ylabel("Amplitud de la señal PPG")
                    plt.show()
                else:
                    print(f"Error: La fila {fila} está fuera del rango del archivo.")
            else:
                print("El archivo proporcionado no es un DataFrame.")
        except Exception as e:
            print(f"Error al procesar el archivo: {e}")


    # Genera los coeficientes para un filtro pasa-bajo de Butterworth
    @staticmethod
    def butter_lowpass(cutoff, fs, order=5):
        nyquist = 0.5 * fs  # Frecuencia de Nyquist
        normal_cutoff = cutoff / nyquist  # Normaliza la frecuencia de corte
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return b, a

    # Aplica el filtro pasa-bajo a los datos
    @staticmethod
    def butter_lowpass_filter(data, cutoff, fs, order=5):
        b, a = PPG.butter_lowpass(cutoff, fs, order)  # Obtiene los coeficientes del filtro
        y = filtfilt(b, a, data)  # Aplica el filtro a los datos
        return y

    # Calcula la frecuencia dominante de una señal
    @staticmethod
    def calculate_dominant_frequency(signal, fs, cutoff=3, order=5):
        """
        Calcula la frecuencia dominante de una señal después de aplicar un filtro pasa-bajo.

        Parámetros:
            signal (array-like): La señal a analizar.
            fs (float): Frecuencia de muestreo en Hz.
            cutoff (float): Frecuencia de corte del filtro en Hz (por defecto 3 Hz).
            order (int): Orden del filtro (por defecto 5).

        Retorna:
            float: Frecuencia dominante en Hz.
        """
        # Aplica un filtro pasa-bajo
        filtered_signal = PPG.butter_lowpass_filter(signal, cutoff, fs, order)
        
        # Realiza la Transformada de Fourier
        N = len(filtered_signal)
        T = 1 / fs  # Período de muestreo
        freqs = np.fft.fftfreq(N, T)  # Frecuencias
        fft_values = np.fft.fft(filtered_signal)  # FFT de la señal filtrada
        
        # Encuentra la frecuencia dominante
        positive_freqs = freqs[:N // 2]  # Frecuencias positivas
        positive_magnitude = np.abs(fft_values[:N // 2])  # Magnitudes
        dominant_frequency = positive_freqs[np.argmax(positive_magnitude)]  # Frecuencia dominante
        return dominant_frequency
    
    def obtener_frecuencia_muestreo(self, tiempo):
        """
        Calcula la frecuencia de muestreo a partir del número de muestras y el tiempo total de grabación.
        
        Parámetros:
        tiempo (float): El tiempo total de la grabación en segundos.
        
        Retorna:
        float: La frecuencia de muestreo en Hz.
        """
        if self.__señalppg is not None:
            # Obtiene el número de muestras (filas) en la señal
            num_muestras = len(self.__señalppg)
            
            # Calcula la frecuencia de muestreo
            frecuencia_muestreo = num_muestras / tiempo
            
            print(f"Frecuencia de muestreo: {frecuencia_muestreo} Hz")
            
            return frecuencia_muestreo
        else:
            print("No se ha cargado ninguna señal PPG.")
            return None

    def analizar_frecuencia_ppg_por_fila(df, fila, fs, umbral_baja=3, umbral_alta=5, ventana_tamaño=1024, solapamiento=512):
        """
        Analiza la frecuencia de una señal PPG específica contenida en una fila de un DataFrame.
        Detecta segmentos con frecuencias bajas y altas utilizando FFT.

        Parámetros:
            df (DataFrame): El DataFrame que contiene la señal PPG.
            fila (int): El índice de la fila que contiene la señal PPG.
            fs (float): La frecuencia de muestreo de la señal.
            umbral_baja (float): El límite superior de la frecuencia baja (Hz).
            umbral_alta (float): El límite inferior de la frecuencia alta (Hz).
            ventana_tamaño (int): El tamaño de la ventana para la FFT.
            solapamiento (int): El solapamiento de las ventanas.

        Retorna:
            rangos_bajos (list): Los índices de los segmentos con frecuencias bajas.
            rangos_altos (list): Los índices de los segmentos con frecuencias altas.
        """
        # Extraemos la señal de la fila seleccionada
        signal = df.iloc[fila].values
        n_muestras = len(signal)
        
        rangos_bajos = []
        rangos_altos = []
        
        # Iteramos sobre la señal con ventanas deslizantes
        for start in range(0, n_muestras - ventana_tamaño, ventana_tamaño - solapamiento):
            end = start + ventana_tamaño
            segmento = signal[start:end]
            
            # Calculamos la FFT del segmento
            fft_vals = np.fft.fft(segmento)
            fft_freqs = np.fft.fftfreq(len(fft_vals), 1 / fs)
            
            # Tomamos solo las frecuencias positivas
            fft_vals = np.abs(fft_vals[:len(fft_vals)//2])
            fft_freqs = fft_freqs[:len(fft_freqs)//2]
            
            # Encontramos la frecuencia dominante en este segmento
            idx_max = np.argmax(fft_vals)  # Índice de la frecuencia dominante
            frecuencia_dominante = fft_freqs[idx_max]  # Frecuencia dominante
            
            # Clasificamos el segmento según la frecuencia dominante
            if frecuencia_dominante < umbral_baja:
                rangos_bajos.append((start, end))  # Añadimos el rango de frecuencia baja
            elif frecuencia_dominante > umbral_alta:
                rangos_altos.append((start, end))  # Añadimos el rango de frecuencia alta

        # Graficamos toda la señal y marcamos las zonas
        plt.plot(signal, label="Señal PPG")
        for (start, end) in rangos_bajos:
            plt.axvspan(start, end, color='green', alpha=0.3, label='Frecuencia Baja')
        for (start, end) in rangos_altos:
            plt.axvspan(start, end, color='red', alpha=0.3, label='Frecuencia Alta')

        plt.legend()
        plt.xlabel('Tiempo (índice de muestra)')
        plt.ylabel('Amplitud')
        plt.title('Análisis de frecuencias en la señal PPG')
        plt.show()

        return rangos_bajos, rangos_altos
        def indicenormalidad(self, archivo, paciente):
            """
            Verifica si un paciente específico presenta anormalidad cardíaca basada en la última columna.

            Parámetros:
                archivo (pd.DataFrame): DataFrame con los datos del PPG.
                paciente (int): Índice del paciente (fila) en el DataFrame.
            """
            try:
                # Asegurarse de que 'archivo' sea un DataFrame
                if not isinstance(archivo, pd.DataFrame):
                    raise ValueError("El archivo proporcionado no es un DataFrame.")

                # Verificar que el índice del paciente esté dentro del rango
                if paciente < 0 or paciente >= len(archivo):
                    raise IndexError("El índice del paciente está fuera del rango del DataFrame.")

                # Acceder a la última columna y evaluar el valor
                etiqueta = archivo.iloc[paciente, -1]  # Obtiene el valor en la última columna para el paciente
                if etiqueta == 'MI':
                    print(f"El paciente {paciente} presenta anormalidad cardíaca.")
                elif etiqueta == 'N':
                    print(f"El paciente {paciente} no presenta anormalidad cardíaca.")
                else:
                    print(f"El paciente {paciente} tiene una etiqueta desconocida: {etiqueta}.")
            except Exception as e:
                print(f"Error al procesar el archivo: {e}")


            



paciente1=PPG()    
pacientefile = paciente1.openfile(r'C:/Users/joser/OneDrive/Documentos/Maria Rosa/Captura de pantalla 2024-12-06 121305/PPG_Dataset.csv')
if pacientefile is not None:
    pax = paciente1.Asignarseñal(pacientefile)
    Grafica = paciente1.graficarseñal(pacientefile, 3)
else:
    print("No se pudo abrir el archivo.")

#Obtener frecuencia de muestreo

tiempo = 2500  # Ajusta según el tiempo total de grabación
fs= paciente1.obtener_frecuencia_muestreo(tiempo)

if fs is not None:
    print(f"Frecuencia de muestreo: {fs} Hz")

    # Análisis de frecuencias bajas y altas
    columna_ppg = pax.columns[0]  # Usamos la primera columna como señal PPG
    rangos_bajos, rangos_altos = paciente1.analizar_frecuencia_ppg(pacientefile, columna_ppg, fs)
    print(f"Rangos con frecuencia baja: {rangos_bajos}")
    print(f"Rangos con frecuencia alta: {rangos_altos}")
else:
    print("No se pudo abrir el archivo.")

if pacientefile is not None:
    fr=paciente1.calculate_dominant_frequency(pacientefile)
else:
    print('No se pudo abrir el archivo')

# Ejemplo de uso

# fs = 1000  # Frecuencia de muestreo en Hz (ajústalo según tu archivo)
# columna_ppg = 'señal_ppg'  # Nombre de la columna que contiene la señal PPG

# rangos_bajos, rangos_altos = analizar_frecuencia_ppg(df, columna_ppg, fs)
# print(f"Rangos con frecuencia baja: {rangos_bajos}")
# print(f"Rangos con frecuencia alta: {rangos_altos}")


# for file1 in PPG:
#     try:
#         with open(file1, 'rb') as file:
#             data = np.fromfile(file, dtype=np.float32)  # Cambiar dtype si es necesario

#         # Graficar los datos
#         plt.figure(figsize=(10, 6))
#         plt.plot(data)
#         plt.title("Señal PPG")
#         plt.xlabel("Muestras")
#         plt.ylabel("Amplitud")
#         plt.show()

#     except Exception as e:
#         print(f"Error al procesar el archivo {file1}: {e}")

# pacientefile2=paciente1.openfile(file1)
# with open(pacientefile2, 'rb') as f:  # 'rb' para lectura binaria
#     datos = np.fromfile(f, dtype=np.float32)


# print(datos[:10]) 
# print(pacientefile2)
