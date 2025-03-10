from leeRuta import procesar_ruta

import sys
from leeRuta import procesar_ruta
from depuraRuta import procesar_archivos

def main():
    # Verificar que se haya pasado un argumento
    if len(sys.argv) != 2:
        print("Uso: python main.py <opcion>")
        print("Opciones:")
        print("  1 - procesar_ruta")
        print("  2 - procesar_archivos")
        sys.exit(1)

    # Obtener la opción desde los argumentos
    opcion = sys.argv[1]

    if opcion == "1":
        # procesaRuta = "h:\\"
        # ExCarpetas = ['H:\\iomega\\movies', 'H:\\iomega\\tvshow', 'H:\\lenovo\\compartidos\\videos']
        procesaRuta = "C:\\Users\\LeonPP\\Documents"
        ExcluiCarpetas = ['C:\\Users\\LeonPP\\Documents\\espana', 'C:\\Users\\LeonPP\\Documents\\maletin']
        ExcluirExten = ['.mkv', '.avi', '.m4v', '.mp4'] # , '.mp3', '.pdf']

        print("Iniciando carga de rutas en la tabla py.ListArchivo...")
        procesar_ruta(procesaRuta, ExcluiCarpetas, ExcluirExten)
        print("Carga de rutas finalizada.")

    elif opcion == "2":
        
        id_accion = 92 # int(input("Introduce el idAccion (90 para borrar, 92 para simular borrado): "))

        print("Iniciando proceso de depuración de archivos...")
        procesar_archivos(id_accion)
        print("Proceso de depuración de archivos finalizado.")

    else:
        print(f"Opción inválida: {opcion}")
        print("Opciones válidas: 1 (procesar_ruta) o 2 (procesar_archivos)")
        sys.exit(1)

if __name__ == "__main__":
    main()

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