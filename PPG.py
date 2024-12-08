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
            contenido = pd.read_csv(file)
            print(contenido.head())
        elif file.endswith(".mat"):
            print(f"Archivo MAT encontrado: {file}")
            contenido = loadmat(file)
            print(contenido.keys())  # Muestra las claves del archivo MAT
        elif file.endswith("PPG.dat"):
            print(f"Archivo DAT encontrado: {file}")
            with open(file, 'r', encoding='utf8') as contenido:
                datos = contenido.readlines()
                print(datos[:5])  # Muestra las primeras 5 líneas
                return datos

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
        """
        Grafica una fila específica de un archivo CSV.

        Parámetros:
            archivo (str): Ruta al archivo CSV.
            fila (int): Índice de la fila que deseas graficar.
        """
        try:
            # Leer el archivo como un DataFrame
            self.__señalppgdf = pd.read_csv(archivo)
            
            # Verificar que la fila solicitada exista
            if fila < len(self.__señalppgdf):
                señal = self.__señalppgdf.iloc[fila, :-1]  # Excluir la última columna si no es parte de la señal
                plt.plot(señal)
                plt.title(f"Señal PPG - Paciente {fila}")
                plt.xlabel("Tiempo (o índice de columna)")
                plt.ylabel("Amplitud de la señal PPG")
                plt.show()
            else:
                print(f"Error: La fila {fila} está fuera del rango del archivo.")
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
    
paciente1=PPG()  
pacientefile=paciente1.openfile('C:/Users/joser/OneDrive/Documentos/Maria Rosa\Captura de pantalla 2024-12-06 121305\PPG_Dataset.csv')
#print(PPG)
print(pacientefile)
pax=paciente1.Asignarseñal(pacientefile)
pax1=paciente1.graficarseñal(pacientefile, 3)

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
