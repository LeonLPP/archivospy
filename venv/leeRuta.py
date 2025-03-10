import os
import hashlib
import logging
import time
import pyodbc
from configConn import CADENA_CONEXION
from datetime import datetime

# Listas de exclusión
ExCarpetas = ['H:\\iomega\\movies', 'H:\\iomega\\tvshow', 'H:\\lenovo\\compartidos\\videos'] 
ExExten = ['.mkv', '.avi', '.m4v', '.mp4'] # , '.mp3', '.pdf'] 

# Log del proceso
logging.basicConfig(
    filename='reg_leeRuta.log',  # Nombre del archivo de log
    level=logging.INFO,  # Nivel del log (INFO, DEBUG, WARNING, etc.)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formato del log
)

# Conectar a la BBDD
conexion = pyodbc.connect(CADENA_CONEXION)

# Calcular el hash SHA256 como lo hace en PowerShell
def calcular_hash(archivo):
    hash_sha256 = hashlib.sha256()
    with open(archivo, "rb") as f:
        for bloque in iter(lambda: f.read(4096), b""):
            hash_sha256.update(bloque)
    return hash_sha256.hexdigest()

def procesar_ruta(ruta):    
    start_time = time.time()  # Inicio del cronómetro
    iniTime = datetime.now()
    numArchivos=0
    logging.info(f"Conexion Cursor: {iniTime}")
    cursor = conexion.cursor()
    logging.info(f"Procesar ruta: {ruta}")
    for carpeta, subcarpetas, archivos in os.walk(ruta):
        #Excluir carpetas
        #subcarpetas[:] = [d for d in subcarpetas if d not in ExCarpetas]
        # Excluir carpetas o subcarpetas cuyo nombre comienza por la lista de ExCarpetas
        if any(carpeta.lower().startswith(os.path.join(ruta, excluida).lower()) for excluida in ExCarpetas):
            logging.info(f"Excluir carpeta: {carpeta}")
            subcarpetas[:] = []  # Detener la exploración en esta carpeta
            continue

        for archivo in archivos:
            try:
                # Validar que el archivo no tenga una extensión excluida
                if any(archivo.lower().endswith(ext) for ext in ExExten):                    
                    logging.info(f"Excluir archivo: {archivo}")
                    continue
                
                ruta_archivo = os.path.join(carpeta, archivo)
                info = os.stat(ruta_archivo)

                # Obtener metadatos del archivo
                fe_creado = datetime.fromtimestamp(info.st_ctime)
                nombre, extension = os.path.splitext(archivo)
                tamano = info.st_size
                ruta_relativa = carpeta
                fec_modif = datetime.fromtimestamp(info.st_mtime)
                fec_access = datetime.fromtimestamp(info.st_atime)
                hash_archivo = calcular_hash(ruta_archivo)

                # Insertar en SQL Server
                cursor.execute("""
                    INSERT INTO py.ListArchivosTest (FeCreado, Nombre, Exten, Tamano, Ruta, RutArchivo, FecModif, FecAccess, idHash, idDupli, idAccion)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, NULL)
                """, fe_creado, nombre, extension, tamano, ruta_relativa, ruta_archivo, fec_modif, fec_access, hash_archivo)
                conexion.commit()
                
                # print(f"Archivo procesado: {ruta_archivo}")
                numArchivos += 1
                #logging.info(f"Archivo procesado: {ruta_archivo}")

            except Exception as e:
                # print(f"Error procesando {ruta_archivo}: {e}")
                #logging.info(f"#Error procesando: {ruta_archivo}: {e}")
                logging.info(f"#Error: {e}") # la excepcion ya incluye el nombre del archivo

    # Cerrar conexion
    cerrar_conexion()
    logging.info(f"Conexion Cerrada")
    # Finalizar el cronómetro
    end_time = time.time()
    finTime = datetime.now()
    elapsed_time = end_time - start_time
    logging.info(f"Fin Ruta... {ruta}")
    logging.info(f"Archivos procesados: {numArchivos}")
    logging.info(f"Ruta procesada. Inicio: {iniTime}, Fin: {finTime} ... duración {elapsed_time:.2f}")    
    print(f"Procesados: {numArchivos}... Ruta... {ruta}")
    print(f"Ruta procesada. Inicio: {iniTime}, Fin: {finTime} ... duración {elapsed_time:.2f}")

# Cerrar conexión cuando sea necesario
def cerrar_conexion():
    conexion.close()
