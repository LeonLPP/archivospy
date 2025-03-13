# depuraRuta.py
import logging
import os
import time
from configConn import connectDB
from clsArchivo import Archivo

# Configuración del log
logging.basicConfig(
    filename='regDepura.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def ejecutarProcesoArchivo(idResult, idArchivo):
    # Actualiza.
    conexion = connectDB()
    if not conexion:
        print("Error: No se pudo establecer conexión con la base de datos.")
        return False

    try:
        with conexion.cursor() as cursor:
            cursor.execute("EXEC py.sp_UpdtArchivos ?, ?", idArchivo, idResult)
            conexion.commit()
            logging.info(f"Actualizado correctamente: idArchivo={idArchivo}, idResult={idResult}")
            return True
    except Exception as e:
        logging.error(f"#Error py.sp_UpdtArchivos: (idArchivo={idArchivo}, idResult={idResult})... Error: {e}")
        return False
    finally:
        conexion.close()

def procesarArchivos(idAccion):
    # Procesa los archivos idAccion 90 o 92, omite idResulto 0 o null
    inicio = time.time()
    conexion = connectDB()
    if not conexion:
        print("Error: No se pudo establecer conexión con la base de datos.")
        return

    logging.info("Conexión establecida para procesar archivos.")

    try:
        with conexion.cursor() as cursor:
            cursor.execute("EXEC py.sp_procesArchivos ?", idAccion)
            registros = cursor.fetchall()

        # Contadores para estadísticas
        recProcess, recUpdates, recErrDel, recNotFound, totalSize, recSkipped = 0, 0, 0, 0, 0, 0

        for registro in registros:
            idArchivo, idResult, _, rutaArchivo, tamano = registro

            if idResult not in (None, 0):
                logging.info(f"Omitido, Resultado: {idResult}, {rutaArchivo}")
                recSkipped += 1
                continue

            if os.path.exists(rutaArchivo):
                if idAccion == 90:
                    try:
                        os.remove(rutaArchivo)
                        idResult = 99
                        logging.info(f"ELIMINADO, Resultado: {idResult}, {rutaArchivo}")
                        totalSize += tamano
                    except Exception as e:
                        idResult = 94
                        recErrDel += 1
                        logging.error(f"#Error No Eliminado {idArchivo}, {rutaArchivo}: {e}")
                elif idAccion == 92:
                    idResult = 98
                    logging.info(f"Borrado lógico: {idResult}, {rutaArchivo}")
                    totalSize += tamano
            else:
                idResult = 91
                logging.info(f"Archivo NO encontrado: {idResult}, {rutaArchivo}")
                recNotFound += 1

            if ejecutarProcesoArchivo(idResult, idArchivo):
                recUpdates += 1

            recProcess += 1

        # Resumen del proceso (imprimir y registrar en el log)
        print(f"* Procesados: {recProcess}")
        print(f"* Actualizados: {recUpdates}")
        print(f"* Errores al eliminar: {recErrDel}")
        print(f"* Omitidos: {recSkipped}")
        print(f"* No encontrados: {recNotFound}")
        print(f"* Tamaño total procesado: {totalSize} bytes")

        logging.info(f"Archivos procesados: {recProcess}")
        logging.info(f"Registros actualizados: {recUpdates}")
        logging.info(f"Archivos con errores al eliminar: {recErrDel}")
        logging.info(f"Archivos omitidos: {recSkipped}")
        logging.info(f"Archivos no encontrados: {recNotFound}")
        logging.info(f"Tamaño total procesado: {totalSize} bytes")

    except Exception as e:
        logging.error(f"#Error durante la ejecución de py.sp_procesArchivos: {e}")
    finally:
        conexion.close()
        duracion = time.time() - inicio
        print(f"- Proceso finalizado en {duracion:.2f} segundos")
        logging.info(f"Proceso finalizado en {duracion:.2f} segundos")
