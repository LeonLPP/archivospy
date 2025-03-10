import os
import pyodbc
from configConn import CONN_STR
#
# Para grandes volumenes de datos
# Procesar por lotes
#
def ejec_processBig(id_result, conexion, id_archivo):
    # Llama al procedimiento almacenado py.sp_UpdtArchivos para actualizar el registro.
    try:
        with conexion.cursor() as curUpdt:
            curUpdt.execute("EXEC py.sp_UpdtArchivos ?, ?", id_archivo, id_result)
            conexion.commit()
            print(f"Actualizado correctamente: idArchivo={id_archivo}, idResult={id_result}")
            return True
    except Exception as e:
        print(f"#Error py.sp_UpdtArchivos: (idArchivo={id_archivo}, idResult={id_result})... Error: {e}")
        return False

def procesArchivBig(id_accion, batch_size=1000):
    # Procesa archivos según idAccion por lotes
    conexion = pyodbc.connect(CONN_STR)

    try:
        with conexion.cursor() as cursor:
            # Ejecuta el procedimiento almacenado para obtener registros
            cursor.execute("EXEC py.sp_procesArchivos ?", id_accion)

            recProcess = 0
            recUpdates = 0
            regNotfound = 0
            totSize = 0

            # Procesar en lotes
            while True:
                registros = cursor.fetchmany(batch_size)  # Obtén los registros por lotes
                if not registros:
                    break  # Sal del bucle si no hay más registros

                for registro in registros:
                    id_archivo, idResult, Nombre, rut_archivo, Tamano = registro

                    # Verifica si el archivo existe
                    if os.path.exists(rut_archivo):
                        if id_accion == 90:  # Borrar archivo
                            try:
                                os.remove(rut_archivo)
                                id_result = 99  # Eliminación exitosa
                                totSize += Tamano
                            except Exception as e:
                                print(f"#Error al eliminar el archivo {rut_archivo}: {e}")
                                id_result = 94  # Error al intentar borrar
                        elif id_accion == 92:  # Simular borrado
                            print(f"Borrado lógico del archivo: {rut_archivo}")
                            id_result = 98  # Simulación exitosa
                            totSize += Tamano
                    else:
                        id_result = 91  # Archivo no existe
                        regNotfound += 1

                    # Actualiza la tabla usando el procedimiento almacenado
                    if ejec_processBig(id_result, conexion, id_archivo):
                        recUpdates += 1

                    recProcess += 1

        # Muestra el resumen del proceso
        print(f"Procesados: {recProcess}")
        print(f"Actualizados: {recUpdates}")
        print(f"Archivos no encontrados: {regNotfound}")
        print(f"Tamaño total procesado: {totSize} bytes")

    except Exception as e:
        print(f"#Error durante la ejecución: py.sp_procesArchivos: {e}")

    finally:
        # Cierra la conexión
        conexion.close()
