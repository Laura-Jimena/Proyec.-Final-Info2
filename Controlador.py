from Modelo import *
from Vista import *
import sys
from PyQt5.QtWidgets import QApplication7

class Controlador():
    def __init__(self,vista,modelo):
        self.__mivista=vista
        self.__mimodelo=modelo

    def Recibir_nuev_cuenta(self,nomb,id,telef,email,usua,contras):
        self.__mimodelo.Agregar_usuario(nomb,id,telef,email,usua,contras)
    def Recibir_cred(self,usu,con):
        self.__mimodelo.#Metdo en modelo para verificar existencia en base de datos