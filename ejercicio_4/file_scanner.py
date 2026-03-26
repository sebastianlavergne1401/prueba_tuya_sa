import os

class FileScanner:
    """Responsabilidad: Manejar la recursividad de directorios y listas de archivos."""
    
    def __init__(self, processor):
        self.processor = processor

    def get_html_files(self, paths: list) -> list:
        """Recorre carpetas y subcarpetas buscando archivos .html"""
        html_files = []
        for path in paths:
            if os.path.isfile(path) and path.endswith('.html') and not path.endswith('_b64.html'):
                html_files.append(path)
            elif os.path.isdir(path):
                # os.walk entra en todas las subcarpetas automáticamente
                for root, _, files in os.walk(path):
                    for file in files:
                        if file.endswith('.html') and not file.endswith('_b64.html'):
                            html_files.append(os.path.join(root, file))
        return html_files

    def run(self, input_paths: list):
        files = self.get_html_files(input_paths)
        for file in files:
            print(f"-> Procesando: {file}")
            self.processor.process_file(file)
        
        return self.processor.report