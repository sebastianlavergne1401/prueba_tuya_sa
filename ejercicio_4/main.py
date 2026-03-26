import json
from image_encoder import ImageEncoder
from html_processor import HTMLProcessor
from file_scanner import FileScanner

def main():
    # 1. Inicializar componentes
    encoder = ImageEncoder()
    processor = HTMLProcessor(encoder)
    scanner = FileScanner(processor)

    # 2. Definir rutas de entrada (pueden ser carpetas o archivos sueltos)
    paths_to_process = ["./ejercicio_4/data_html"] 

    print("Iniciando procesamiento de archivos HTML...\n")
    
    # 3. Ejecutar
    final_report = scanner.run(paths_to_process)
    
    # 4. Mostrar reporte final solicitado
    print("\n" + "="*30)
    print("REPORTE DE EJECUCIÓN")
    print("="*30)
    print(json.dumps(final_report, indent=4))

if __name__ == "__main__":
    main()