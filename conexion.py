import mysql.connector
from mysql.connector import errorcode

def ConexionDB():
    '''
     Descripcion: Script que establece conexion con la base de datos

    Parametros:
        
    
    Return:
        None
    '''
    try:
            database=mysql.connector.connect(
            host='localhost',
            user='root',
           )
 
            return(database)
    except mysql.connector.Error as error:

        if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Nombre de usuario o contraseña incorrectos.")
        elif error.errno == errorcode.ER_BAD_DB_ERROR:
            print("La base de datos no existe.")
        else:
            print(f"Error al conectar a MySQL: {error}")


        
def CrearBd():
    '''
    Descripcion: Crea base de datos "informatica1" en localhost si esta no existe

    Parametros:
        Output: string que me indica si la base de datos fue creada
    
    Return:
        
    '''
    
    try:
        
        database=ConexionDB()
        cursor=database.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS EPI")
        print("Base de datos creada exitosamente")
    except mysql.connector.Error as error:

        if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Nombre de usuario o contraseña incorrectos.")
        elif error.errno == errorcode.ER_BAD_DB_ERROR:
            print("La base de datos no existe.")
        else:
            print(f"Error al conectar a MySQL: {error}")