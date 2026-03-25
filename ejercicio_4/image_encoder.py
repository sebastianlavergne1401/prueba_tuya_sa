import os
import base64
import mimetypes

class ImageEncoder:
    """Responsabilidad: Convertir archivos físicos a strings Base64."""
    
    @staticmethod
    def to_base64(image_path: str) -> str:
        """
        Lee los bytes de una imagen y los convierte en un Data URI.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"No existe: {image_path}")
            
        # Adivina el tipo de archivo (image/jpeg, image/png, etc.)
        mime_type, _ = mimetypes.guess_type(image_path)
        if not mime_type or not mime_type.startswith('image'):
            mime_type = "image/png"  # Fallback por seguridad

        with open(image_path, "rb") as img_file:
            # b64encode devuelve bytes, .decode('utf-8') lo vuelve string
            encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
            return f"data:{mime_type};base64,{encoded_string}"