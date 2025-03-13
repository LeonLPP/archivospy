# clsArchivo.py
import os
import hashlib
from datetime import datetime
from configConn import connectDB


class Archivo:
    def __init__(self, idArchivo=None, nombre=None, extension=None, tamano=None, ruta=None, hashArchivo=None, fecCreado=None, fecModif=None, fecAccess=None):
        self.idArchivo = idArchivo  # Clave primaria
        self.nombre = nombre
        self.extension = extension
        self.tamano = tamano
        self.ruta = ruta
        self.hashArchivo = hashArchivo
        self.fecCreado = fecCreado
        self.fecModif = fecModif
        self.fecAccess = fecAccess

    @staticmethod
    def calcularHash(rutaArchivo):
        hashSha256 = hashlib.sha256()
        try:
            with open(rutaArchivo, "rb") as f:
                for bloque in iter(lambda: f.read(4096), b""):
                    hashSha256.update(bloque)
            return hashSha256.hexdigest()
        except Exception as e:
            print(f"Error al calcular el hash del archivo: {e}")
            return None

    @staticmethod
    def cargaDB(idArchivo):
        
        conexion = connectDB()
        if not conexion:
            print("Error: No se pudo establecer conexión con la base de datos.")
            return None

        try:
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT idArchivo, Nombre, Extension, Tamano, Ruta, Hash, FechaCreado, FechaModificado, FechaAcceso
                FROM ListArchivos
                WHERE idArchivo = ?
            """, idArchivo)
            registro = cursor.fetchone()

            if registro:
                # Crear una instancia de Archivo con los datos devueltos
                return Archivo(
                    idArchivo=registro[0],
                    nombre=registro[1],
                    extension=registro[2],
                    tamano=registro[3],
                    ruta=registro[4],
                    hashArchivo=registro[5],
                    fecCreado=registro[6],
                    fecModif=registro[7],
                    fecAccess=registro[8]
                )
            else:
                print(f"No se encontró ningún archivo con idArchivo={idArchivo}.")
                return None
        except Exception as e:
            print(f"Error al cargar el archivo desde la base de datos: {e}")
            return None
        finally:
            conexion.close()

    def guardaDB(self):
        # Agregar info del Archivo
        conexion = connectDB()
        if not conexion:
            return "Error: No se pudo establecer conexión con la base de datos."

        try:
            cursor = conexion.cursor()
            cursor.execute("""
                EXEC py.sp_ListArchivosAdd ?, ?, ?, ?, ?, ?, ?, ?, ?
            """, self.fecCreado, self.nombre, self.extension, self.tamano,
                 os.path.dirname(self.ruta), self.ruta, self.fecModif, self.fecAccess, self.hashArchivo)
            conexion.commit()
            return f"Éxito: El archivo '{self.nombre}' fue guardado correctamente en la base de datos."
        except Exception as e:
            return f"Error al guardar el archivo '{self.nombre}': {e}"
        finally:
            conexion.close()
