import os
import pyodbc
from configConn import CONN_STR

def ejec_procesarchivo(id_result, conexion, id_archivo):
    
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            EXEC py.sp_procesArchivos ?, ?
        """, id_archivo, id_result)
        conexion.commit()
        print(f"Actualizado correctamente: {id_archivo}, idResult={id_result}")
        return True
    except Exception as e:
        print(f"#Error al actualizar: idArchivo={id_archivo}, Error: {e}")
        return False
    finally:
        cursor.close()

def procesar_archivos_por_accion(id_accion):
    
    conexion = pyodbc.connect(CONN_STR)
    cursor = conexion.cursor()

    try:
        
        cursor.execute("EXEC py.sp_procesArchivos ?", id_accion)
        registros = cursor.fetchall()

        regProcesados = 0  
        regActualizados = 0 

        for registro in registros:
            id_archivo, rut_archivo = registro  # Suponiendo que el procedimiento devuelve estos dos campos

            # Verifica si el archivo existe
            if os.path.exists(rut_archivo):
                if id_accion == 90:  # Borrar archivo
                    try:
                        os.remove(rut_archivo)
                        id_result = 99  # Eliminación exitosa
                    except Exception as e:
                        print(f"Error al eliminar el archivo {rut_archivo}: {e}")
                        id_result = 94  # Error al intentar borrar
                elif id_accion == 92:  # Simular borrado
                    print(f"Simulación de borrado del archivo: {rut_archivo}")
                    id_result = 98  # Simulación exitosa
            else:
                id_result = 91  # Archivo no existe

            # Actualiza la tabla usando el procedimiento almacenado
            if ejec_procesarchivo(id_result, conexion, id_archivo):
                regActualizados += 1

            regProcesados += 1

        # Muestra el resumen del proceso
        print(f"Registros procesados: {regProcesados}")
        print(f"Registros actualizados: {regActualizados}")

    except Exception as e:
        print(f"#Error ejec: py.sp_procesArchivos: {e}")

    finally:
        # Cierra la conexión
        cursor.close()
        conexion.close()
