import os
import pyodbc
from configConn import CONN_STR


def ejec_procesarchivo(id_result, conexion, id_archivo):
    try:
        with conexion.cursor() as curUpdt:
            curUpdt.execute("EXEC py.sp_UpdtArchivos ?, ?", id_archivo, id_result)
            conexion.commit()
            print(f"Actualizado correctamente: idArchivo={id_archivo}, idResult={id_result}")
            return True
    except Exception as e:
        print(f"#Error py.sp_UpdtArchivos: (idArchivo={id_archivo}, idResult={id_result})... Error: {e}")
        return False


def procesar_archivos(id_accion):
    conexion = pyodbc.connect(CONN_STR)

    try:
        with conexion.cursor() as cursor:
            cursor.execute("EXEC py.sp_procesArchivos ?", id_accion)
            registros = cursor.fetchall() # Cargamos todos los registros

        recProcess = 0
        recUpdates = 0
        recNotfound = 0
        totSize = 0
        recSkiped=0

        for registro in registros:
            id_archivo, idResult, Nombre, rut_archivo, Tamano = registro

            if idResult not in (None, 0):
                print(f"Omitido {id_archivo} tiene idResult: {idResult}")
                recSkiped +=1
                continue

            # Verifica si el archivo existe
            if os.path.exists(rut_archivo):
                if id_accion == 90:  # Borrar archivo
                    try:
                        os.remove(rut_archivo)
                        id_result = 99  # Eliminación exitosa
                        totSize += Tamano
                    except Exception as e:
                        print(f"#Error No Eliminado {id_archivo}, {rut_archivo}: {e}")
                        id_result = 94  # Error al intentar borrar
                elif id_accion == 92:  # Simular borrado
                    print(f"Simula Borrado: {id_archivo}, {rut_archivo}")
                    id_result = 98  # Simulación exitosa
                    totSize += Tamano
            else:
                id_result = 91  # Archivo no existe
                recNotfound += 1

            # Actualiza la tabla usando el procedimiento almacenado
            if ejec_procesarchivo(id_result, conexion, id_archivo):
                recUpdates += 1

            recProcess += 1

        # Muestra el resumen del proceso
        print(f"Procesados: {recProcess}")
        print(f"Actualizados: {recUpdates}")
        print(f"Omitidos: {recSkiped}")
        print(f"Archivos no encontrados: {recNotfound}")
        print(f"Tamaño total procesado: {totSize} bytes")

    except Exception as e:
        print(f"#Error durante la ejecución: py.sp_procesArchivos: {e}")

    finally:
        # Cierra la conexión
        conexion.close()
