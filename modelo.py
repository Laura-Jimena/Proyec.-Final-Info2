import scipy.io as sio
import numpy as np
import pandas as pd
import scipy.signal as signal
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

class ECGSignal:

    '''Metodo que inicializa los atributos de la clase
       Parametros: ruta del archivo a cargar'''

    def __init__(self, rutaECG):
        self.rutaECG = rutaECG
        self.__datos = None
        self.__fs = None  # Frecuencia de muestreo (cantidad de muestras tomadas por segundo)
        self.unidades = "mV"  # microvoltios (unidad estándar ECG)
        self.__duracion = None
        self.__canales = None

    # Métodos getter y setter
    def AsignarDatos(self, datos):
        self.__datos = datos

    def MostrarDatos(self):
        return self.__datos

    def AsignarFs(self, fs):
        self.__fs = fs

    def MostrarFs(self):
        return self.__fs

    def AsignarDuracion(self, duracion):
        self.__duracion = duracion

    def MostrarDuracion(self):
        return self.__duracion

    def AsignarCanales(self, canales):
        self.__canales = canales

    def MostrarCanales(self):
        return self.__canales

    '''Metodo que permite la carga de archivos .mat y .csv correspondientes a señales ECG '''

    def load_data(self):
        try:
            if self.rutaECG.endswith('.mat'):
                contenido = sio.whosmat(self.rutaECG)
                clave = None

                for var in contenido:  # var es una tupla
                    nombre, dimensiones, _ = var
                    if len(dimensiones) == 2:  # Busca matriz 2D
                        clave = nombre
                        break

                if clave:
                    dataECG = sio.loadmat(self.rutaECG)[clave]  # Importa solo la clave que necesitamos
                    self.AsignarDatos(dataECG)
                    self.AsignarFs(500)  # Usamos 5000 Hz como la frecuencia de muestreo (información que está en la base de datos que estamos usando)
                    return True  # Carga exitosa
                else:
                    return False  # No encontró la clave adecuada

            elif self.rutaECG.endswith('.csv'):  # Cargar archivos .csv
                dataECG = pd.read_csv(self.rutaECG)
                self.AsignarDatos(dataECG.values)
                self.AsignarFs(500) # Asumimos la misma frecuencia de muestreo para CSV
                return True  # Carga exitosa
            else:
                return False  # Tipo de archivo no soportado
        except Exception as e:
            print(f"Error al cargar datos: {e}")  # imprime el error
            return False

    ''' Método para aplicar filtros específicos por derivación (Esto porque para cada derivación hay un rango que favorece lo que queremos analizar)

        Parametros: Derivacion a fitrar type: Str ('I','II' o 'V5)'''

    def filtrar_por_derivacion(self, derivacion):

        if self.__datos is None:
          print("No se han cargado datos.")
          return None

        '''Nyquist se calcula debido a que hay un teorema que dice que la frecuencia
        de muestreo de la señal original, debe ser por lo menos el doble de la frecuencia más alta registrada en la señal'''
        nyquist = 0.5 * self.__fs

        if derivacion == 'II':
           lowcut, highcut = 0.5, 40.0  # Frecuencias típicas para la derivación II

        elif derivacion == 'V5':
           lowcut, highcut = 0.5, 45.0  # Frecuencias para V5

        elif derivacion == 'I':
           lowcut, highcut = 0.5, 50.0  # Frecuencias para I

        '''En low y high se normalizan las frecuencias de corte para que estén en el dominio Nyquist (que va de 0 a 1)
           y puedan ser recibidas por el filtro'''

        low = lowcut / nyquist
        high = highcut / nyquist

        '''Butter se refiere a una operación matemática que arroja los coeficientes a y b que serán utilizados por el filtro Butterworth
          (b y a representan el numerador y denominador de la función de transferencia del filtro digital)'''

        b, a = signal.butter(1, [low, high], btype='band') #Se define el filtro que se utilizara (paso banda de orden 1)

        fila = 0 if derivacion == 'I' else (1 if derivacion == 'II' else (9 if derivacion == 'V5' else None))

        #verificacion de la implementacion del filtro
        try:
          print(f"Datos antes del filtro (primeros 10): {self.__datos[fila,:10]}")

          '''filtfilt aplica el filtro dos veces, hacia adelante y hacia atrás, para eliminar el desfase que puede dejar el filtro'''

          self.__datos[fila, :] = signal.filtfilt(b, a, self.__datos[fila, :])
          print(f"Datos después del filtro (primeros 10): {self.__datos[fila,:10]}")

        except Exception as e:
          print(f"Error al filtrar la señal de {derivacion}: {e}")

    '''Metodo que permite encontrar picos en la señal, indices que seran utilizados en otros calculos
       Parametros: Derivacion '''

    def EncontrarPicos(self,derivacion):
        fila = 0 if derivacion == 'I' else (1 if derivacion == 'II' else (9 if derivacion == 'V5' else None))
        data= self.__datos[fila, :]  # Segun los datos proporcionados, la fila 9 contiene los datos de la derivacion V5

            # Detectar picos R
        '''find_peaks es una funcion de la libreris scipy.signal que encuentra maximos locales en una señal,
            comparando cada punto con sus vecinos y definiendo si se trata de un maximo'''
        indices_picos, propiedades = find_peaks(
                data,
                height=0.5,         # Altura mínima del pico
                distance=200       # Distancia mínima entre picos consecutivos en ms(de acuerdo  datos de un latido promedio)
            )
        return indices_picos,data

    '''Metodos asociados a la grafica de cada una de las derivaciones tenidas en cuenta (I,II,V5)
       Paeametros: tiempo en ms hasta el que se desea graficar la señal, type: INT'''

    def graficar_derivacion_II(self,t):

      if self.__datos is not None:

        self.filtrar_por_derivacion('II')
        indices_picos,data=self.EncontrarPicos('II')
        # Calcular el rango dinámico de la señal(Para que el eje y se acomode al los valores maximos y minimos de la señal)

        signal_min = self.__datos[1, :].min()  # Fila 1 para derivación II
        signal_max = self.__datos[1, :].max()

        # Crear el gráfico
        plt.figure(figsize=(16, 4))  # Ajustar el ancho
        # Crear un array de tiempo en milisegundos
        tiempo = np.arange(self.__datos.shape[1]) # Tiempo en microegundos

        # Graficar la señal en función del tiempo
        plt.plot(tiempo, self.__datos[1,:], linewidth=0.5)  # Fila 1 = Derivación II
        plt.title('ECG - Derivación II')
        plt.plot(indices_picos, data[indices_picos], 'ro', label="Picos R") #señala los picos R en la grafica
        plt.xlabel('Tiempo (ms)')
        plt.ylabel('Amplitud (mV)')

        # Establecer límites de los ejes
        plt.xlim(0, tiempo[t])  # Limitar el eje X al rango de tiempo
        plt.ylim(signal_min, signal_max)  # Limitar el eje Y según los valores min/max de la señal

        plt.grid()
        plt.show()
      else:
        print("No hay datos disponibles para graficar derivación II")

    # Método para graficar la derivación v5
    def graficar_derivacion_V5(self,t):

     self.filtrar_por_derivacion('V5')
     indices_picos,data=self.EncontrarPicos('V5')

     if self.__datos is not None:

        # Calcular el rango dinámico de la señal (AMPLITUD)
        signal_min = self.__datos[9, :].min()  # Fila 9 para derivación V5
        signal_max = self.__datos[9, :].max()

        # Crear el gráfico
        plt.figure(figsize=(16, 4))

        tiempo = np.arange(self.__datos.shape[1]) # Tiempo en microsegundos

        # Graficar la señal en función del tiempo
        plt.plot(tiempo, self.__datos[9,:], linewidth=0.5)
        plt.title('ECG - Derivación V5')
        plt.plot(indices_picos, data[indices_picos], 'ro', label="Picos R")
        plt.xlabel('Tiempo (ms)')
        plt.ylabel('Amplitud (mV)')

        # Establecer límites de los ejes
        plt.xlim(0, tiempo[t])  # Limitar el eje X al rango de tiempo
        plt.ylim(signal_min, signal_max)  # Limitar el eje Y según los valores min/max de la señal

        plt.grid()
        plt.show()
     else:
        print("No hay datos disponibles para graficar derivación V5")

    # Método para graficar la derivación I
    def graficar_derivacion_I(self,t):

     if self.__datos is not None:

        self.filtrar_por_derivacion('I')
        indices_picos,data=self.EncontrarPicos('I')
        # Calcular el rango dinámico de la señal
        signal_min = self.__datos[0, :].min()
        signal_max = self.__datos[0, :].max()

        # Crear el gráfico
        plt.figure(figsize=(16, 4))  # Ajustar el ancho
        # Crear un array de tiempo en milisegundos
        tiempo = np.arange(self.__datos.shape[1]) # Tiempo en milisegundos

        # Graficar la señal en función del tiempo
        plt.plot(tiempo, self.__datos[0,:], linewidth=0.5)  # Fila 1 = Derivación I
        plt.title('ECG - Derivación I')
        plt.plot(indices_picos, data[indices_picos], 'ro', label="Picos R")
        plt.xlabel('Tiempo (ms)')
        plt.ylabel('Amplitud (mV)')

        # Establecer límites de los ejes
        plt.xlim(0, tiempo[t])  # Limitar el eje X al rango de tiempo
        plt.ylim(signal_min, signal_max)  # Limitar el eje Y según los valores min/max de la señal

        plt.grid()
        plt.show()
     else:
        print("No hay datos disponibles para graficar derivación I")

    '''Metodo  que permite calcular la frecuencia cardiaca media en bpm utilizanso la derivacion  I'''
    def CalculraHR(self):

       indices_picos,_=self.EncontrarPicos('I')

       # Calcular intervalos RR
       '''np.diff calcula la diferencia entre elementos consecutivos en un arreglo
        devuelve un arreglo que contiene las diferencias de los elementos adyacentes en el arreglo original.'''

       rr = np.diff(indices_picos)/ self.__fs # Convertir de ms a seg

       # Calcular frecuencia cardíaca en bpm
       frecuencias = 60 / rr  # En bpm(array xon todas las frecuencias)

       # Promedio de la frecuencia cardíaca
       frecuencia_media = np.mean(frecuencias)

       return frecuencia_media

    def calcularHRV(self):
    # Encontrar picos R
       indices_picos,_=self.EncontrarPicos('I')

    # Calcular intervalos RR
       rr = np.diff(indices_picos)/ self.__fs  # En segundos

    # Calcular HRV
       hrv = np.std(rr)
       return hrv


    def CalcularDesviacionEstandar(self):
    # Encontrar picos R
     indices_picos,_= self.EncontrarPicos('II')

    # Calcular intervalos RR y frecuencias
     rr= np.diff(indices_picos)/ self.__fs  # En segundos
     frecuencias = 60 / rr  # En bpm

    # Calcular desviación estándar
     desviacion = np.std(frecuencias)
     return desviacion

    def calcular_varianza_rr(self):
     # Encontrar picos R
     indices_picos, _ = self.EncontrarPicos('II')

      # Calcular intervalos RR
     rr= np.diff(indices_picos) / self.__fs # En segundos

     # Calcular varianza
     varianza = np.var(rr)
     return varianza




