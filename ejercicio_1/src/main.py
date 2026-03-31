import csv
import os
from utils import validate_phone

def process_dataset():
    # Definición de rutas relativas a la raíz del proyecto
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_dir = os.path.join(base_path, 'data', 'raw')
    output_dir = os.path.join(base_path, 'data', 'processed')
    
    input_file = os.path.join(input_dir, 'datos_prueba.csv')
    output_file = os.path.join(output_dir, 'resultado_validacion.csv')

    # Crear carpeta de salida si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Directorio creado: {output_dir}")

    success_list = []
    fail_list = []

    if not os.path.exists(input_file):
        print(f"Error: No se encontro el archivo en {input_file}")
        return

    with open(input_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Usamos la columna 'telefono' para validar, si no existe se asigna una cadena vacía
            tel_original = row.get('telefono', '')
            
            is_valid, result = validate_phone(tel_original)
            
            record = {
                "id": row.get('id_cliente', 'N/A'),
                "nombre": row.get('nombre', 'Desconocido'),
                "original": tel_original,
                "resultado": result,
                "estado": 'VALIDO' if is_valid else 'INVALIDO'
            }

            if is_valid:
                success_list.append(record)
            else:
                fail_list.append(record)

    # Escribir resultados
    with open(output_file, mode='w', encoding='utf-8', newline='') as file:
        fieldnames = ['id', 'nombre', 'original', 'resultado', 'estado']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(success_list)
        writer.writerows(fail_list)

    print(f"Procesamiento finalizado exitosamente.")
    print(f"Resultados guardados en: {output_file}")
    print("Hello world")

if __name__ == "__main__":
    process_dataset()