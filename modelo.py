# from Procesador_ECG import *
# from Procesador_PPG import *
# from Procesador_RX import *


class Usuario():
    def __init__(self):
        self.__nombre=""
        self.__id=0
        self.__telef=0
        self.__email=""
        self.__usuario=""
        self.__contras=""

    def Asignar_nomb (self,n):
        self.__nombre=n.capitalize()
    def Asignar_id(self,id):
        self.__id=id
    def Asignar_tel(self,tel):
        self.__telef=tel
    def Asignar_email(self,em):
        self.__email=em.lower
    def Asignar_usuario(self,us):
        self.__usuario=us
    def Asignar_contrasena(self,con):
        self.__contras=con

    def Agregar_usuario(self,n,id,tel,em,us,con):
        u=Usuario()
        u.Asignar_nomb(n)
        u.Asignar_id(id)
        u.Asignar_tel(tel)
        u.Asignar_email(em)
        u.Asignar_usuario(us)
        u.Asignar_contrasena(con)
    # def Verificar_usuario(self,usu,con):


class Archivo():
    def Cargar_archivo_rx(self,arch_rx):
        return arch_rx
    def Cargar_archivo_ecg(self,arch_ecg):
        return arch_ecg
    def Cargar_archivo_ppg(self,arch_ppg):
        return arch_ppg
    

        



