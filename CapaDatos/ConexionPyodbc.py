   
import mysql.connector

try: 
# Configura la conexión
    conexion = mysql.connector.connect(
        host="localhost",  # host de la base de datos 
        user="root",  # nombre de usuario de MySQL
        password="",  # contraseña de MySQL
        database="sportcentergym"  #nombre de la base de datos 
    )
    print("Conexión exitosa a la base de datos")
    
except Exception as ex:
    print(ex)


