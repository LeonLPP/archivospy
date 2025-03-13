# leeRuta.py
import os
import logging
import time
from datetime import datetime
from clsArchivo import Archivo

# Configuración del log
logging.basicConfig(
    filename='regLeeRuta.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def procesarRuta(ruta, excluirCarpetas, excluirExtensiones):
    """
    Procesa una ruta, excluye carpetas y extensiones, y guarda información en la base de datos.
    """
    startTime = time.time()
    inicio = datetime.now()
    numArchivos = 0
    logging.info(f"Inicio del procesamiento de la ruta: {ruta}")

    for carpeta, subcarpetas, archivos in os.walk(ruta):
        if any(carpeta.lower().startswith(os.path.join(ruta, excluida).lower()) for excluida in excluirCarpetas):
            logging.info(f"Excluir carpeta: {carpeta}")
            subcarpetas[:] = []
            continue

        for archivo in archivos:
            try:
                if any(archivo.lower().endswith(ext) for ext in excluirExtensiones):
                    logging.info(f"Excluir archivo: {archivo}")
                    continue

                rutaArchivo = os.path.join(carpeta, archivo)
                info = os.stat(rutaArchivo)

                archivoNuevo = Archivo(
                    nombre=os.path.splitext(archivo)[0],
                    extension=os.path.splitext(archivo)[1],
                    tamano=info.st_size,
                    ruta=rutaArchivo,
                    hash_archivo=Archivo.calcular_hash(rutaArchivo),
                    fec_creado=datetime.fromtimestamp(info.st_ctime),
                    fec_modif=datetime.fromtimestamp(info.st_mtime),
                    fec_access=datetime.fromtimestamp(info.st_atime),
                )

                resultado = archivoNuevo.guardaDB()
                logging.info(resultado)
                numArchivos += 1

            except Exception as e:
                logging.error(f"Error procesando {archivo} en {carpeta}: {e}")

    elapsedTime = time.time() - startTime
    fin = datetime.now()
    logging.info(f"Ruta procesada. Inicio: {inicio}, Fin: {fin}, Duración: {elapsedTime:.2f} segundos")
    print(f"Procesados: {numArchivos} archivos en la ruta {ruta}")
