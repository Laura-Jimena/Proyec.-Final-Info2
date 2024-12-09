from Modelo import *
from Vista import *
import sys
from PyQt5.QtWidgets import QApplication

class Controlador():
    def __init__(self,vista,modelo):
        self.__mivista=vista
        self.__mimodelo=modelo

    def Recibir_nuev_cuenta(self,nomb,id,telef,email,usua,contras):
        self.__mimodelo.Agregar_usuario(nomb,id,telef,email,usua,contras)
    def Recibir_cred(self,usu,con):
        self.__mimodelo.Verificar_usuario(usu,con)
    def Mover_archivo_rx(self,archivo):
        self.__mimodelo.Cargar_archivo_rx(archivo)
    def Mover_archivo_ecg(self,archivo):
        self.__mimodelo.Cargar_archivo_ecg(archivo)
    def Mover_archivo_ppg(self,archivo):
        self.__mimodelo.Cargar_archivo_ppg(archivo)
