import pyodbc
from configConn import CONN_STR

def probar_conexion():
    try:
        # Intentar conectarse al servidor
        miConn = CONN_STR
        conexion = pyodbc.connect(CONN_STR)
        print(f"¡Conexión exitosa! {miConn}")
        
        # Cerrar la conexión
        conexion.close()
    except Exception as e:
        # Mostrar cualquier error que ocurra
        print(f"Error al conectar a SQL Server: {e}")

if __name__ == "__main__":
    probar_conexion()
