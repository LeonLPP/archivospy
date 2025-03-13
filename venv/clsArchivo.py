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
"""
Razones para usar @staticmethod
Independencia de la Instancia:

Métodos como calcularHash o cargaDB realizan tareas que no necesitan interactuar con los atributos de una instancia particular de Archivo.

Por ejemplo:

calcularHash simplemente toma una ruta de archivo como entrada, calcula su hash y retorna el valor; no depende de los atributos como idArchivo o ruta.

cargaDB accede directamente a la base de datos para obtener información basada en idArchivo, pero tampoco utiliza atributos específicos de una instancia de Archivo.

Organización del Código:

Agrupar estas funciones dentro de la clase Archivo tiene sentido desde el punto de vista conceptual, ya que están relacionadas con la lógica de archivos.

Sin embargo, como no requieren una instancia, el decorador @staticmethod comunica claramente esta independencia.

Eficiencia:

Al definir métodos como @staticmethod, evitamos crear objetos adicionales o asociarlos con una instancia específica, lo que puede ahorrar recursos cuando se realiza una operación repetidamente.

Claridad:

Ayuda a que el código sea más legible y entendible para otros desarrolladores. Al usar @staticmethod, queda explícito que los métodos son utilitarios y no interactúan con atributos específicos de la clase o de una instancia.

Cuándo usar @staticmethod en lugar de un método normal
Usa @staticmethod cuando:

El método no necesita acceder ni modificar los atributos de clase (cls) ni de instancia (self).

La funcionalidad tiene sentido como parte de la clase (por ejemplo, está directamente relacionada con la lógica de Archivo) pero no depende de atributos internos.

Por ejemplo, en calcularHash, no hay razón para crear una instancia de Archivo solo para calcular el hash de un archivo, ya que puedes pasar directamente la ruta como argumento y realizar la operación.
"""