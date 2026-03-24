import re

def clean_number(phone_str):
    """
    Elimina caracteres no numéricos y normaliza el formato.
    """
    if not phone_str or phone_str.lower() == 'null':
        return None
    
    # Eliminar todo lo que no sea un número
    cleaned = re.sub(r'\D', '', str(phone_str))
    
    # Manejar prefijo internacional de Colombia (57) si existe
    if len(cleaned) == 12 and cleaned.startswith('57'):
        cleaned = cleaned[2:]
    elif len(cleaned) == 13 and cleaned.startswith('0057'):
        cleaned = cleaned[4:]
        
    return cleaned

def validate_phone(phone_str):
    """
    Valida si el número tiene la estructura correcta (10 dígitos para móvil).
    Retorna (es_valido, numero_formateado)
    """
    cleaned = clean_number(phone_str)
    
    if not cleaned:
        return False, "Vacio o Nulo"
    
    # Regla: Debe tener exactamente 10 dígitos y empezar por 3 o 6
    # (Ajustable según las reglas de negocio)
    if len(cleaned) == 10 and (cleaned.startswith('3') or cleaned.startswith('6')):
        return True, f"+57{cleaned}"
    
    if len(cleaned) < 10:
        return False, "Longitud insuficiente"
    
    if len(cleaned) > 10:
        return False, "Exceso de dígitos"
    
    return False, "Formato no reconocido"