from conexion import *
import mysql.connector
from mysql.connector import errorcode
from utils import *

def CrearTablas():
    '''
    Descripcion: Crea tabla "Medico"

    Parametros:
        Output: string que me indica si la tabla fue creada 
    
    Return:
        None
    '''
    try:
        database = ConexionDB()
        cursor = database.cursor()
        cursor.execute("USE epi")
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS medico(
                        documento INT NOT NULL PRIMARY KEY,
                        nombre VARCHAR(100) NOT NULL,
                        telefono INT NOT NULL,
                        email VARCHAR(100) NOT NULL,
                        user VARCHAR(45),
                        password  INT
                       ) ENGINE=InnoDB''')
       
        database.commit()
        cursor.close()
        database.close()
        

    except mysql.connector.Error as error:

        if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Nombre de usuario o contraseña incorrectos.")
        elif error.errno == errorcode.ER_BAD_DB_ERROR:
            print("La base de datos no existe.")
        else:
            print(f"Error al conectar a MySQL: {error}")


def ValoresPredeterminados():
    '''
    Descripcion: Llena las tablas de la base de datos con valores predeterminados si estas se encuenttran vacias

    Parametros:
        None
    
    Return:
        None
    '''
    try:
        database = ConexionDB()
        cursor = database.cursor()
        cursor.execute("USE epi")
        # Verifica si la tabla medico  está vacía
        cursor.execute("SELECT COUNT(*) FROM medico")
        cont_medicos = cursor.fetchone()[0]


        if cont_medicos==0:


            sql="INSERT INTO medico (documento,nombre,telefono,email,user,password) VALUES (%s,%s,%s,%s,%s,%s)"
            values=[
                (1007373986,'Katerin Salazar','3242952101','katerin.salazara@udea.edu.co','ktsalazar',1234),
             
            ]
            cursor.executemany(sql, values)
            database.commit()

    except mysql.connector.Error as error:

        if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Nombre de usuario o contraseña incorrectos.")

        elif error.errno == errorcode.ER_BAD_DB_ERROR:
            print("La base de datos no existe.")

        else:
            print(f"Error al conectar a MySQL: {error}")


def DatosMedico(documento,nombre,telefono,email,user,password):

    '''
    Descripcion: Obtiene y valida datos de medicos

    Parametros:
        Output: nombre, apellido, documento, entidad que corresponden al proveedor
    
    Return:
         nombre, apellido, documento, entidad que corresponden al proveedor
    '''
    while True:

        try:
            doc=int(documento)
            clave=int(password)
            tel=int(telefono)

            #valida longitud de documento (son de 8 digitos antes de 2004)

            if len(str(doc))<8 or len(str(doc))>10:
             
                return False
                        
               
            # valida longitud del telefono ingresado

            if len(str(tel))<7 or len(str(tel))>12:
                
                return False
                 
            
            valEmail=validar_correo(email)

            if valEmail==False:
                return False 
                
            return doc,nombre,tel,email,user,clave
        
        
        except ValueError:
            print("=====INGRESE VALOR VALIDO PARA EL CAMPO=====")
            return False
            

def CrearMedico(documento,nombre,telefono,email,user,password):
    '''
    Descripcion: Crea un nuevo proveedor en la base de datos

    Parametros:
        input: codigo del nuevo proveedor ingresado por consola
        Output: string que indica que el proveedor fue creado
    
    Return:
        None
    '''
    try:
        database=ConexionDB()
        if database is None:
            return []

        cursor = database.cursor()
        cursor.execute("USE epi")
        documento,nombre,telefono,email,user,password=DatosMedico(documento,nombre,telefono,email,user,password)
        valdoc=validar_documento(documento)
        valuser=validar_user(user)
        if valdoc == True and valuser ==True:
           sql="INSERT INTO medico (documento,nombre,telefono,email,user,password) VALUES (%s,%s,%s,%s,%s,%s)"
           values=(documento,nombre,telefono,email,user,password)
           cursor.execute(sql, values)
           database.commit()
        else:
            return False


    except mysql.connector.Error as error:
        print(f"Error al conectar a MySQL: {error}")
        return False