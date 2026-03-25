import os
import re

class HTMLProcessor:
    """Responsabilidad: Parsear HTML y reemplazar tags de imagen."""
    
    def __init__(self, encoder):
        self.encoder = encoder
        self.report = {"success": {}, "fail": {}}

    def process_file(self, html_path: str) -> str:
        """Busca etiquetas <img>, extrae el src y lo reemplaza por Base64."""
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()

        directory = os.path.dirname(html_path)
        
        # Regex: Busca <img ... src="ruta" ...>
        # Captura lo que esté dentro de las comillas del src
        img_tag_pattern = re.compile(r'<img\s+[^>]*src=["\']([^"\']+)["\'][^>]*>')
        
        def replacement_func(match):
            original_src = match.group(1)
            # Resuelve la ruta de la imagen relativa al HTML
            full_img_path = os.path.join(directory, original_src)
            
            try:
                b64_data = self.encoder.to_base64(full_img_path)
                self.report["success"][original_src] = "Codificado con éxito"
                return match.group(0).replace(original_src, b64_data)
            except Exception as e:
                self.report["fail"][original_src] = str(e)
                return match.group(0) # Mantiene el src original si falla

        new_content = img_tag_pattern.sub(replacement_func, content)
        
        # Generar nombre para el nuevo archivo (ej. index_b64.html)
        base, ext = os.path.splitext(html_path)
        new_path = f"{base}_b64{ext}"
        
        with open(new_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        return new_path