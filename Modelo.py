
from bd import*
from utils import *
from conexion import *

class Usuario():
    """Clase que representa a un usuario en el sistema.

    Atributos:
    ----------
    - __nombre (str): Nombre del usuario.
    - __id (int): Identificación del usuario.
    - __telef (int): Número de teléfono del usuario.
    - __email (str): Correo electrónico del usuario.
    - __usuario (str): Nombre de usuario.
    - __contras (str): Contraseña del usuario."""
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
        """Registra un nuevo usuario en el sistema."""
        CrearMedico(id,n,tel,em,us,con)
    def Verificar_usuario(self,usu,con):
        """Verifica si las credenciales del usuario son válidas."""
        cred=login(usu,con)
        if cred ==True:
            return True
        elif cred==False:
            return False



        



