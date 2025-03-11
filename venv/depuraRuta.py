import logging.config
import os
import pyodbc
import logging
import time
from configConn import CONN_STR

logging.basicConfig(
    filename='regDepura.log',
    level=logging.INFO, #I NFO, DEBUG, WARNING, etc.
    format='%(asctime)s - %(levelname)s - %(message)s'
)


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
    iniTime = time.time()    
    conexion = pyodbc.connect(CONN_STR)
    logging.info(f"Conexion Cursor")

    try:
        with conexion.cursor() as cursor:
            cursor.execute("EXEC py.sp_procesArchivos ?", id_accion)
            registros = cursor.fetchall() # Cargamos todos los registros

        recProcess = 0
        recUpdates = 0
        recErrDel = 0
        recNotfound = 0
        totSize = 0
        recSkiped=0

        for registro in registros:
            id_archivo, idResult, Nombre, rut_archivo, Tamano = registro

            if idResult not in (None, 0):
                # print(f"Omitido {id_archivo} tiene idResult: {idResult}")
                logging.info(f"Omitido, Resultado: {idResult}, {rut_archivo}")
                recSkiped +=1
                continue

            # Verifica si el archivo existe
            if os.path.exists(rut_archivo):
                if id_accion == 90:  # Borrar archivo
                    try:
                        os.remove(rut_archivo)
                        id_result = 99  # Eliminación exitosa
                        logging.info(f"ELIMINADO, Resultado: {id_result}, {rut_archivo}")
                        totSize += Tamano
                    except Exception as e:
                        id_result = 94  # Error al intentar borrar
                        recErrDel +=1
                        print(f"#Error No Eliminado {id_archivo}, {rut_archivo}: {e}")
                        logging.info(f"#Error No Eliminado: {id_result}, {rut_archivo}: {e}")                        
                elif id_accion == 92:  # Simular borrado
                    id_result = 98  # Simulación exitosa
                    #print(f"Simula Borrado: {id_archivo}, {rut_archivo}")
                    logging.info(f"Borrado lógico: {id_result} , {rut_archivo}")
                    totSize += Tamano
            else:
                id_result = 91  # Archivo no existe
                logging.info(f"Fichero NO encontrado: {id_result} , {rut_archivo}")
                recNotfound += 1

            # Actualiza la tabla usando el procedimiento almacenado
            if ejec_procesarchivo(id_result, conexion, id_archivo):
                recUpdates += 1

            recProcess += 1

        # Muestra el resumen del proceso
        print(f"* Procesados: {recProcess}")
        print(f"* Actualizados: {recUpdates}")
        print(f"* Err: No Eliminados: {recErrDel}")
        print(f"* Omitidos: {recSkiped}")
        print(f"* No encontrados: {recNotfound}")
        print(f"* Tamaño total procesado: {totSize} bytes")
        logging.info(f"Archivos Procesados: {recProcess}")
        logging.info(f"Registros actualizados: {recUpdates}")
        logging.info(f"Archivos que no se han podido eliminar: {recErrDel}")
        logging.info(f"Archivos Omitidos, ya con resultados: {recSkiped}")
        logging.info(f"Archivos NO encontrados: {recNotfound}")

    except Exception as e:
        print(f"#Error durante la ejecución: py.sp_procesArchivos: {e}")
        logging.info(f"#Error durante la ejecución procesar_archivos({id_accion}): {e}")

    finally:
        # Cierra la conexión
        conexion.close()
        finTime = time.time()
        elapTime = finTime - iniTime
        print(f"- Proceso finalizado, duración: {elapTime:.2f}")
        logging.info(f"Proceso finalizado, duración: {elapTime:.2f}")
