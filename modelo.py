import scipy.io as sio
import numpy as np
import pandas as pd
import scipy.signal as signal
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

class ECGSignal:

    def __init__(self, rutaECG):
        '''Metodo que inicializa los atributos de la clase
        Parametros: ruta del archivo a cargar'''
        self.rutaECG = rutaECG
        self.__datos = None
        self.__fs = None  # Frecuencia de muestreo (cantidad de muestras tomadas por segundo)
        self.__indicesPicos= [ ]
        self.__HR = 0
        self.__HRV= 0
        self.__SD = 0
        self.__Varianza= 0
        self.__RMSSD = 0
        self.__SD1 = 0
        self.__SD2 = 0
        self.__AmplitudR = 0
        self.__AmplitudS = 0

        self.__RelacionRS = 0


    # Métodos getter y setter
    def AsignarDatos(self, datos):
        self.__datos = datos

    def MostrarDatos(self):
        return self.__datos

    def AsignarFs(self, fs):
        self.__fs = fs

    def MostrarFs(self):
        return self.__fs

    def AsignarIndicesPicos(self,Ip):
        self.__indicesPicos=Ip

    def MostrarIndicesPicos(self):
        return self.__indicesPicos

    def AsignarHR(self,HR):
        self.__HR = HR

    def MostrarHR(self):
        return self.__HR

    def AsignarHRV(self,HRV):
        self.__HRV = HRV

    def MostrarHRV(self):
        return self.__HRV

    def AsignarSD(self,SD):
        self.__SD= SD

    def MostrarSD(self):
        return self.__SD

    def AsignarVarianza(self,v):
        self.__Varianza= v

    def MostrarVarianza(self):
        return self.__Varianza

    def AsignarRMSSD(self,rmssd):
        self.__RMSSD= rmssd

    def MostrarRMSSD(self):
        return self.__RMSSD
    def AsignarSD1(self,sd1):
        self.__SD1= sd1

    def MostrarSD1(self):
        return self.__SD1

    def AsignarSD2(self,sd2):
        self.__SD2= sd2

    def MostrarSD2(self):
        return self.__SD2

    def AsignarAmplitudR(self,R):
        self.__AmplitudR= R

    def MostrarAmplitudR(self):
        return self.__AmplitudR

    def AsignarAmplitudS(self,S):
        self.__AmplitudS= S

    def MostrarAmplitudS(self):
        return self.__AmplitudS

    def AsignarRelacionRS(self,RS):
        self.__RelacionRS= RS

    def MostrarRelacionRS(self):
        return self.__RelacionRS





    def load_data(self):

        '''
        Metodo que permite la carga de archivos .mat y .csv correspondientes a señales ECG
        '''
        try:
            if self.rutaECG.endswith('.mat'):
                contenido = sio.whosmat(self.rutaECG)
                clave = None

                for var in contenido:
                    nombre, dimensiones, _ = var
                    if len(dimensiones) == 2:  # Busca matriz 2D
                        clave = nombre
                        break

                if clave:
                    dataECG = sio.loadmat(self.rutaECG)[clave]  # Importa solo la clave que necesitamos
                    self.AsignarDatos(dataECG)
                    self.AsignarFs(500)  # Usamos 500 Hz como la frecuencia de muestreo (información que está en la base de datos que estamos usando)
                    return True  # Carga exitosa
                else:
                    return False  # No encontró la clave adecuada

             # Cargar archivos .csv
            elif self.rutaECG.endswith('.csv'):
                dataECG = pd.read_csv(self.rutaECG)
                self.AsignarDatos(dataECG.values)
                self.AsignarFs(500) # Asumimos la misma frecuencia de muestreo para CSV
                return True  # Carga exitosa
            else:
                return False  # Tipo de archivo no soportado
        except:

            print(f"Error al cargar datos")  # imprime el error
            return False


    def obtener_fila(self, derivacion):
            '''Metodo que permite determinar la fila dependiendo la derivacion a trabajar
             parametros: derivacion que se desa utilizar type: str
          '''
            if derivacion == 'V2':
               return 7
            elif derivacion == 'II':
               return 1
            elif derivacion == 'V5':
               return 9
            else:
                raise ValueError(f"Derivación desconocida: {derivacion}")

    def filtrar_por_derivacion(self, derivacion):

        '''
         Método para aplicar filtros específicos por derivación (Esto porque para cada derivación hay un rango que favorece lo que queremos analizar)

         Parametros: Derivacion a fitrar type: Str ('II','V2' o 'V5)
      '''

        datos=self.MostrarDatos()
        if datos is None:
          print("No se han cargado datos.")
          return None

        '''Nyquist se calcula debido a que hay un teorema que dice que la frecuencia
        de muestreo de la señal original, debe ser por lo menos el doble de la frecuencia más alta registrada en la señal'''
        nyquist = 0.5 * self.MostrarFs()

        if derivacion == 'II':
           lowcut, highcut = 1.0, 40.0  # Frecuencias típicas para la derivación II

        elif derivacion == 'V2':
           lowcut, highcut = 1.0, 60.0  # Frecuencias para V5

        elif derivacion == 'V5':
           lowcut, highcut = 1.0, 50.0  # Frecuencias para I

        '''En low y high se normalizan las frecuencias de corte para que estén en el dominio Nyquist (que va de 0 a 1)
           y puedan ser recibidas por el filtro'''

        low = lowcut / nyquist
        high = highcut / nyquist

        '''Butter se refiere a una operación matemática que arroja los coeficientes a y b que serán utilizados por el filtro Butterworth
          (b y a representan el numerador y denominador de la función de transferencia del filtro digital)'''

        b, a = signal.butter(1, [low, high], btype='band') #Se define el filtro que se utilizara (paso banda de orden 1)

        fila =self.obtener_fila(derivacion)

        #verificacion de la implementacion del filtro
        try:
         # print(f"Datos antes del filtro (primeros 10): {datos[fila,:10]}")

          '''filtfilt aplica el filtro dos veces, hacia adelante y hacia atrás, para eliminar el desfase que puede dejar el filtro'''

          self.__datos[fila, :] = signal.filtfilt(b, a, datos[fila, :])
          #print(f"Datos después del filtro (primeros 10): {datos[fila,:10]}")

        except Exception as e:
          print(f"Error al filtrar la señal de {derivacion}: {e}")



    def EncontrarPicos(self,derivacion):

        '''Metodo que permite encontrar picos en la señal, indices que seran utilizados en otros calculos
        Parametros: Derivacion '''

        fila =self.obtener_fila(derivacion)
        data= self.MostrarDatos()[fila, :]

            # Detectar picos R
        '''find_peaks es una funcion de la libreris scipy.signal que encuentra maximos locales en una señal,
            comparando cada punto con sus vecinos y definiendo si se trata de un maximo'''
        indices_picos, propiedades = find_peaks(
                data,
                height=0.5,         # Altura mínima del pico
                distance=300       # Distancia mínima entre picos consecutivos en ms(de acuerdo  datos de un latido promedio)
            )

        self.AsignarIndicesPicos(indices_picos)

        return data


    def graficar_derivacion(self,t,derivacion):

      '''Metodos asociado a la grafica de cada una de la derivacion II (vision general)
         Parametros: tiempo en ms hasta el que se desea graficar la señal, type: INT'''

      if self.MostrarDatos() is not None:

        self.filtrar_por_derivacion(derivacion)
        data=self.EncontrarPicos(derivacion)
        fila =self.obtener_fila(derivacion)

        # Calcular el rango dinámico de la señal(Para que el eje 'y' se acomode al los valores maximos y minimos de la señal)

        signal_min = self.MostrarDatos()[fila, :].min()  # Fila 1 para derivación II
        signal_max = self.MostrarDatos()[fila, :].max()

        # Crear el gráfico

        plt.figure(figsize=(16, 4))  # Ajustar el ancho

        # Crear un array de tiempo en milisegundos
        tiempo = np.arange(self.MostrarDatos().shape[1])

        # Graficar la señal en función del tiempo
        plt.plot(tiempo, self.MostrarDatos()[fila,:], linewidth=0.5)
        plt.title(f'ECG - Derivación {derivacion}')
        plt.plot(self.MostrarIndicesPicos(), data[self.MostrarIndicesPicos()], 'ro', label="Picos R") #señala los picos R en la grafica
        plt.xlabel('Tiempo (ms)')
        plt.ylabel('Amplitud (mV)')

        # Establecer límites de los ejes

        plt.xlim(0, tiempo[t])  # Limitar el eje X al rango de tiempo
        plt.ylim(signal_min, signal_max)  # Limitar el eje Y según los valores min/max de la señal
        plt.grid()
        plt.show()
      else:
        print(f"No hay datos disponibles para graficar derivación  {derivacion}")

    # Método para graficar la derivación v5
    def graficar_derivacion_V5(self,t):
     self.graficar_derivacion(t,'V5')

    # Método para graficar la derivación V2
    def graficar_derivacion_V2(self,t):
     self.graficar_derivacion(t,'V2')

    # Método para graficar la derivación II
    def graficar_derivacion_II(self,t):
     self.graficar_derivacion(t,'II')


    def calcularHR(self):

       '''
       Metodo que permite calcular la frcuencia cardiaca media utilizando la derivacion II

      '''
       self.EncontrarPicos('II')


       # Calcular intervalos RR
       '''np.diff calcula la diferencia entre elementos consecutivos en un arreglo
        devuelve un arreglo que contiene las diferencias de los elementos adyacentes en el arreglo original.'''

       rr = np.diff(self.MostrarIndicesPicos())/ self.MostrarFs()

       # Calcular frecuencia cardíaca en bpm
       frecuencias = 60 / rr  # En bpm(array xon todas las frecuencias)

       # Promedio de la frecuencia cardíaca
       frecuencia_media = round(np.mean(frecuencias),3)
       self.AsignarHR(frecuencia_media)


    def calcularHRV(self):

       '''
       Metodo que permite calcular la variabilidad de la Frecuencia cardiaca, utilizando la derivacion II
       '''

       self.EncontrarPicos('II')
      # Calcular intervalos RR
       rr = np.diff(self.MostrarIndicesPicos())/ self.MostrarFs()  # En segundos

    # Calcular HRV
       hrv = round(np.std(rr)*1000,3)
       self.AsignarHRV(hrv)



    def CalcularDesviacionEstandar(self):
      '''
      Metodo que permite encontrar la Desviacion estandar utilizando la derivacion II

      '''
      self.EncontrarPicos('II')

    # Calcular intervalos RR y frecuencias
      rr= np.diff(self.MostrarIndicesPicos())/ self.MostrarFs()  # En segundos
      frecuencias = 60 / rr  # En bpm

    # Calcular desviación estándar
      desviacion =round(np.std(frecuencias)*1000,3)
      self.AsignarSD(desviacion)


    def calcular_varianza_rr(self):

      '''
      Metodo que permite calcular la varianza de picos R en la derivacion II

      '''
      self.EncontrarPicos('II')

      # Calcular intervalos RR
      rr= np.diff(self.MostrarIndicesPicos()) / self.MostrarFs() # En segundos

     # Calcular varianza
      varianza = round(np.var(rr)*1000,3)
      self.AsignarVarianza(varianza)


    def CalcularRMSSD(self):
      '''
      Metodo que permite calcular la variabilidad de la frecuencia cardiaca

      '''

      self.EncontrarPicos('II')


      rr = np.diff(self.MostrarIndicesPicos()) / self.__fs

    # Calcular RMSSD
      diferencias_rr = np.diff(rr)  # Diferencias entre intervalos consecutivos

      rmssd = round(np.sqrt(np.mean(diferencias_rr ** 2))*1000,3)
      self.AsignarRMSSD(rmssd)


    def calcular_indices_poincare(self,derivacion):
      '''
      Metodo que permite calcular los indices de poncaire en una derivacion dada como parametro
      Parametros: derivacion de la cual se desea calcular los indices type:Str
      '''
      self.EncontrarPicos('II')

      # Calcular intervalos RR
      rr= np.diff(self.MostrarIndicesPicos()) / self.MostrarFs()

    # Crear pares (RR_n, RR_{n+1})
      rr_n = rr[:-1]
      rr_n1 = rr[1:]

    # Calcular diferencias
      diferencias = rr_n1 - rr_n

    # Calcular SD1 y SD2
      SD1 = round(np.sqrt(np.var(diferencias) / 2),3)
      SD2 = round(np.sqrt(2 * np.var(rr) - (np.var(diferencias) / 2)),3)

      self.AsignarSD1(SD1)
      self.AsignarSD2(SD2)

      return SD1, SD2, rr_n, rr_n1



    def calcular_amplitud_media(self, derivacion):
      """
      Metodo que permite calcular la amplitud media de los picos R y S en la señal de la derivación dada y sus relaciones
      Parametros: derivacion a la que se le desea calcular las amplitudes
      """
      # Encontrar los picos R
      señal = self.EncontrarPicos(derivacion)

      amplitudesR = []
      amplitudesS = []

      for i in range(1, len(self.MostrarIndicesPicos())):  # Itera sobre los picos R

        # Para cada pico R, encontrar el pico S (mínimo entre R y el siguiente pico R)
        inicio = self.MostrarIndicesPicos()[i-1]
        fin = self.MostrarIndicesPicos()[i]

        # Buscar el pico S en este intervalo (mínimo)
        intervalo = señal[inicio:fin]
        pico_S = np.min(intervalo)

        '''
        La amplitud de R es la diferencia entre el pico R y la línea base antes de R
        La amplitud de S es la diferencia entre el pico R y el pico S'''

        amplitudesR.append(señal[self.MostrarIndicesPicos()[i-1]] - np.mean(señal[inicio-50:inicio]))  # Pico R - Línea base
        amplitudesS.append(señal[self.MostrarIndicesPicos()[i-1]] - pico_S)  # Pico R - Pico S

    # Calcular la amplitud media de los picos R y S (ajuste de unidades)
      amplitud_media_R = round(np.mean(amplitudesR)/1000,3)
      amplitud_media_S = round(np.mean(amplitudesS)/1000,3)

      #Relacion picos R y S
      relacion_r_s = round(amplitud_media_R / abs(amplitud_media_S),3)

      self.AsignarAmplitudR(amplitud_media_R)
      self.AsignarAmplitudS(amplitud_media_S)
      self.AsignarRelacionRS(relacion_r_s)

    def CalcularEstadisticasII(self):
      '''Metodo para calcular estadisiticas asociadas especificamente asociadas a la derivacion II'''
      self.calcularHR()
      self.calcularHRV()
      self.calcular_varianza_rr()
      self.CalcularDesviacionEstandar()
      self.CalcularRMSSD()
      self.calcular_amplitud_media('II')

    def CalcularEstadisticasV5(self):
      '''Metodo para calcular estadisiticas asociadas especificamente asociadas a la derivacion V5'''
      self.calcular_indices_poincare('V5')
      self.calcular_amplitud_media('V5')

    def CalcularEstadisticasV2(self):
      '''Metodo para calcular estadisiticas asociadas especificamente asociadas a la derivacion V2'''
      self.calcular_indices_poincare('V2')
      self.calcular_amplitud_media('V2')


    def imprimir_estadisticas(self,derivacion):
       """
       Método para imprimir las estadísticas calculadas de manera organizada
       Parametros: derivacion STR
       """
      # Definimos un diccionario para almacenar las métricas por derivación
       estadisticas = {
         'II': {
            'Frecuencia cardíaca media (HR)': f"{self.MostrarHR()} bpm",
            'Variabilidad de la frecuencia cardíaca (HRV)': f"{self.MostrarHRV()} ms",
            'Desviación estándar (SD)': f"{self.MostrarSD()} ms",
            'Varianza RR': f"{self.MostrarVarianza()} ms" ,
            'RMSSD': f"{self.MostrarRMSSD()} ms" ,
            'Amplitud R': f"{self.MostrarAmplitudR()} mV",
            'Amplitud S': f"{self.MostrarAmplitudS()} mV",
            'Relación R/S': self.MostrarRelacionRS()
         },
         'V2': {
            'Amplitud R': f"{self.MostrarAmplitudR()} mV",
            'Amplitud S': f"{self.MostrarAmplitudS()} mV",
            'Relación R/S': self.MostrarRelacionRS(),
            'Indice de Poncaire SD1': self.MostrarSD1(),
            'Indice de Poncaire SD2': self.MostrarSD2()

         },

        'V5': {


            'Amplitud R': f"{self.MostrarAmplitudR()} mV",
            'Amplitud S': f"{self.MostrarAmplitudS()} mV",
            'Relación R/S': self.MostrarRelacionRS(),
            'Indice de Poncaire SD1': self.MostrarSD1(),
            'Indice de Poncaire SD2': self.MostrarSD2()
         },

         }



       print("=" * 50)
       print(f"Estadísticas calculadas para la derivacion {derivacion}")
       print("=" * 50)


       for i,valor in  estadisticas[derivacion].items():
         print(f"{i}: {valor if valor is not None else 'No calculado'}")
       print("=" * 50)


    def graficar_todas_las_derivaciones(self, t):
      '''
      Método para graficar las tres derivaciones en un solo gráfico con desplazamiento en el eje Y
      Parametros: tiempo hasta el que se graficara las muestras
      '''
      if self.MostrarDatos() is not None:

        # Filtrar y obtener los datos de las tres derivaciones
        self.filtrar_por_derivacion('II')
        data_II = self.MostrarDatos()[self.obtener_fila('II'), :]

        self.filtrar_por_derivacion('V2')
        data_V2 = self.MostrarDatos()[self.obtener_fila('V2'), :]

        self.filtrar_por_derivacion('V5')
        data_V5 = self.MostrarDatos()[self.obtener_fila('V5'), :]

        # Crear el gráfico
        plt.figure(figsize=(16, 12))

        # Crear un array de tiempo en milisegundos
        tiempo = np.arange(self.MostrarDatos().shape[1])

        # desplazamientos en Y para separar las señales
        desplazamiento_II = 0
        desplazamiento_V2 = -900  # Desplazar V2 hacia arriba
        desplazamiento_V5 = 900  # Desplazar V5 hacia arriba

        # Graficar las tres derivaciones con desplazamientos
        plt.plot(tiempo, data_II + desplazamiento_II, label="Derivación II", linewidth=0.5)
        plt.plot(tiempo, data_V2 + desplazamiento_V2, label="Derivación V2", linewidth=0.5)
        plt.plot(tiempo, data_V5 + desplazamiento_V5, label="Derivación V5", linewidth=0.5)


        plt.title('ECG - Derivaciones II, V2 y V5')
        plt.xlabel('Tiempo (ms)')
        plt.ylabel('Amplitud (mV)')

        plt.legend()

        plt.grid(True)

        # Limitar el eje X hasta el tiempo t
        plt.xlim(0, tiempo[t])

        plt.show()
      else:
        print("No hay datos disponibles para graficar.")






