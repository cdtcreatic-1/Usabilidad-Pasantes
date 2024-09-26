from .models import Heuristic, Subprinciple
from .heuristics.heuristics_m import heuristics

# Función para cargar los datos heurísticos en la base de datos
def cargar_datos_heuristicos():
    """
    Carga los datos heurísticos y sus subprincipios en la base de datos a partir de un diccionario externo.
    
    Esta función recorre el diccionario 'heuristics' que contiene las heurísticas y sus subprincipios,
    y por cada entrada, crea o actualiza las instancias de los modelos Heuristic y Subprinciple en la base de datos.
    
    La función garantiza que:
    - Si la heurística o el subprincipio ya existen (basado en su código), se actualizan.
    - Si no existen, se crean nuevas instancias.

    El diccionario de heurísticas está importado desde 'heuristics_m.py' y tiene la siguiente estructura:
    {
        "heuristic_code": {
            "title": "Título de la heurística",
            "description": "Descripción de la heurística",
            "subprinciples": {
                "subprinciple_code": {
                    "subtitle": "Título del subprincipio",
                    "description": "Descripción del subprincipio",
                    "example": "Ejemplo asociado al subprincipio"
                }
            }
        }
    }
    
    Esta estructura permite que tanto las heurísticas como sus subprincipios se carguen de forma jerárquica.
    """

    # Recorrer todas las heurísticas en el diccionario importado
    for heuristic_code, heuristic_data in heuristics.items():
        # Crear o actualizar la instancia del modelo Heuristic basado en el código de la heurística
        heuristic, created = Heuristic.objects.get_or_create(
            code=heuristic_code,
            title=heuristic_data["title"],
            description=heuristic_data["description"]
        )

        # Recorrer todos los subprincipios asociados a esta heurística
        for subprinciple_code, subprinciple_data in heuristic_data["subprinciples"].items():
            # Crear o actualizar la instancia del modelo Subprinciple basado en el código del subprincipio
            Subprinciple.objects.get_or_create(
                code=subprinciple_code,
                subtitle=subprinciple_data["subtitle"],
                description=subprinciple_data["description"],
                example=subprinciple_data["example"],
                heuristic_id=heuristic
            )