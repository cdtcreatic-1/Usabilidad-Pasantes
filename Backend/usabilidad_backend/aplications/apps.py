from django.apps import AppConfig

class AplicationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aplications'

    def ready(self):
        """
        Este método se ejecuta cuando la aplicación está lista.
        
        - Importa y ejecuta la función 'cargar_datos_heuristicos', que carga las heurísticas y subprincipios en la base de datos.
        - Esto asegura que, cada vez que la aplicación se inicia, los datos heurísticos estén disponibles y sincronizados en la base de datos.
        
        El método 'ready' se llama cuando la configuración de la aplicación está completa y es un buen lugar para realizar
        inicializaciones adicionales, como cargar datos iniciales, señales, etc.
        """
        # Importar y cargar los datos iniciales de heurísticas
        from .initial_data import cargar_datos_heuristicos
        cargar_datos_heuristicos()  # Llamada a la función que carga los datos heurísticos en la base de datos
