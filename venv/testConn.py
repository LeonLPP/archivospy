import pyodbc
from configConn import CADENA_CONEXION

def probar_conexion():
    try:
        # Intentar conectarse al servidor
        miConn = CADENA_CONEXION
        conexion = pyodbc.connect(CADENA_CONEXION)        
        print(f"¡Conexión exitosa! {miConn}")
        
        # Cerrar la conexión
        conexion.close()
    except Exception as e:
        # Mostrar cualquier error que ocurra
        print(f"Error al conectar a SQL Server: {e}")

if __name__ == "__main__":
    probar_conexion()
