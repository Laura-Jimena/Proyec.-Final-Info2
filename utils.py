from conexion import *
import mysql.connector
from mysql.connector import errorcode
import re

def validar_correo(correo):
    # Patrón para correos electrónicos
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(patron, correo):
        return True
    else:
        return False

def validar_documento(doc):
    '''
    Descripcion: Valida si el documento del medico  coincide con uno existente en la base de datos.

    Parametros:
        Input: documento de id
    
    Return:
         Existencia=True en caso de no coincidir, false en caso de coincidir.
    '''
    try:
        database = ConexionDB()
        if database is None:
            return False
            
        cursor = database.cursor()
        cursor.execute("USE epi")
        cursor.execute("SELECT documento FROM medico")
        medicos = cursor.fetchall()
        cursor.close()
        database.close()
        listam=[medico[0] for medico in medicos]

        if doc in listam:
          return False
           

        else :
          return True
        
    except mysql.connector.Error as error:
        print(f"Error al conectar a MySQL: {error}")

def validar_user(user):
    '''
    Descripcion: Valida si el user del medico  coincide con uno existente en la base de datos.

    Parametros:
        Input: user ingresado
    
    Return:
         True en caso de no coincidir, false en caso de coincidir.
    '''
    try:
        database = ConexionDB()
        if database is None:
            return False
            
        cursor = database.cursor()
        cursor.execute("USE epi")
        cursor.execute("SELECT user FROM medico")
        medicos = cursor.fetchall()
        cursor.close()
        database.close()
        listam=[medico[0] for medico in medicos]

        if user in listam:
          return False
           

        else :
          return True
        
    except mysql.connector.Error as error:
        print(f"Error al conectar a MySQL: {error}")
        
def login(user, password):
    '''
    Descripcion: Valida si el usuario y contraseña ingresados por consola corresponden a un regisro 
    dentro de la tabla medico de la base de datos.

    Parametros:
        Input: usuario y contraseña solicitados por consola.
        Output: string que me indica  si no esta en la base de datos.
    
    Return:
         True en caso de coincidir, false en caso de no coincidir con un registro 
    '''
    try:
        database = ConexionDB()
        if database is None:
            val=False

        cursor= database.cursor()
        cursor.execute("USE epi")
        sql= "SELECT COUNT(*) FROM medico WHERE user = %s AND password = %s"
        cursor.execute(sql, (user, password))
        resultado= cursor.fetchone()
        cursor.close()
        database.close()
        val=resultado[0] == 1
 
        return(val)
    except mysql.connector.Error as error:
        print(f"Error al conectar a MySQL: {error}")
        return False

