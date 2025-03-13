import sys
import os
from datetime import datetime
from leeRuta import procesarRuta
from depuraRuta import procesarArchivos
from processBackup import validarRespaldo

def main():
    """
    Punto de entrada principal del proyecto.
    """
    # Verificar que se haya pasado un argumento
    if len(sys.argv) != 2:
        print("Uso: python main.py <opcion>")
        print("Opciones:")
        print("  1 - procesarRuta")
        print("  2 - procesarArchivos")
        print("  3 - validarRespaldo")
        sys.exit(1)

    # Obtener la opción desde los argumentos
    opcion = sys.argv[1]

    if opcion == "1":
        rutaPrincipal = os.path.expanduser("~")
        rutaPrincipal = os.path.join(rutaPrincipal, "Documents")

        excluirCarpetas = ['espana', 'maletin']
        excluirExtensiones = ['.mkv', '.avi', '.m4v', '.mp4']  # Agrega más extensiones si es necesario

        print(f"Carga de ruta {rutaPrincipal} en la tabla py.ListArchivo...")
        procesarRuta(rutaPrincipal, excluirCarpetas, excluirExtensiones)

    elif opcion == "2":
        idAccion = 92  # Cambia según tu necesidad (90: borrar, 92: simular borrado)
        print(f"{idAccion} - Proceso depuración de archivos...")
        procesarArchivos(idAccion)

    elif opcion == "3":
        rutaBackup = "h:\\llp16gb\\docs_capgemini\\datos\\Bankia\\Control Riesgo Operativo en Adeudos"
        if not os.path.exists(rutaBackup):
            print(f"La ruta no existe: {rutaBackup}")
            return
        print(f"Validar Respaldos: {rutaBackup}")
        validarRespaldo(rutaBackup)

    else:
        print(f"Opción inválida: {opcion}")
        print("Opciones válidas: 1 (procesarRuta), 2 (procesarArchivos), 3 (validarRespaldo)")
        sys.exit(1)

if __name__ == "__main__":
    inicio = datetime.now()
    print("+ - - - - - - - +")
    print(f"Inicio: {inicio}")
    print("+ - - - - - - - +")
    main()
    fin = datetime.now()
    print("+ - - - - - - - +")
    print(f"Fin: {fin}")


"""
if __name__ == "__main__":
    # Ruta que deseas analizar
    # procesaRuta = "h:\\"
    procesaRuta = "C:\\Users\\LeonPP\\Documents"
    
    # Listas de exclusión
    # ExCarpetas = ['H:\\iomega\\movies', 'H:\\iomega\\tvshow', 'H:\\lenovo\\compartidos\\videos'] 
    ExcluiCarpetas = ['C:\\Users\\LeonPP\\Documents\\espana', 'C:\\Users\\LeonPP\\Documents\\maletin']
    ExcluirExten = ['.mkv', '.avi', '.m4v', '.mp4'] # , '.mp3', '.pdf'] 

    print(f"Procesando la ruta: {procesaRuta}")
    
    # Llamar a la función del módulo leeRuta
    procesar_ruta(procesaRuta, ExcluiCarpetas, ExcluirExten)

"""