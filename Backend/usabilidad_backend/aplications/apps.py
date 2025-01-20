from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class AplicationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aplications'

    def ready(self):
        """
        Este método se ejecuta cuando la aplicación está lista.
        """
        # Conectar la señal post_migrate para cargar los datos después de las migraciones
        post_migrate.connect(cargar_datos_heuristicos, sender=self)

# La función que carga los datos heurísticos
def cargar_datos_heuristicos(sender, **kwargs):
    """
    Cargar los datos heurísticos en la base de datos
    """
    # Aquí puedes realizar la lógica para cargar los datos a la base de datos.
    print("Cargando datos heurísticos...")
    # Lógica para cargar los datos heurísticos.
