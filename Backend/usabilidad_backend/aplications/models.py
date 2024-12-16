from django.db import models
from django.utils import timezone
import uuid

# Modelo para representar a un usuario en la base de datos
class User(models.Model):
    id = models.AutoField(primary_key=True)  # Llave primaria que se genera automáticamente
    username = models.TextField(blank=False, null=False)  # Nombre de usuario (obligatorio)
    email = models.EmailField(blank=False, null=False)  # Dirección de correo electrónico (obligatorio)
    rol = models.CharField(max_length=15, choices=[('Administrador', 'Administrador'), ('Propietario', 'Propietario'), ('Evaluador', 'Evaluador')], blank=False, null=False)  # Rol del usuario (Administrador, Propietario, Evaluador),(obligatorio)
    experience = models.CharField(max_length=10, choices=[('Novato', 'Novato'), ('Experto', 'Experto')], blank=True, null=True)  # Nivel de experiencia del usuario (opcional, puede ser Novato o Experto)
    password = models.CharField(max_length=1024, blank=False, null=False)  # Contraseña del usuario (obligatorio)

    def __str__(self):
        """
        Devuelve una representación legible del modelo User.

        Returns:
            str: Una cadena que representa el usuario, incluyendo su ID, nombre, email, rol y experiencia.
        """
        return '%s:%s:%s:%s:%s' % (self.id, self.username, self.email, self.rol, self.experience)

#//////////////////////////////////////////////////////////////////////////////////////////////////
# Modelo para representar una heurística en la base de datos
class Heuristic(models.Model):
    code = models.CharField(max_length=10, unique=True)  # Código único de la heurística 
    title = models.CharField(max_length=255)  # Título de la heurística
    description = models.TextField()  # Descripción de la heurística

    def __str__(self):
        """
        Devuelve una representación legible del modelo Heuristic.

        Returns:
            str: El título de la heurística.
        """
        return self.title

# Modelo para representar un subprincipio relacionado con una heurística
class Subprinciple(models.Model):
    code = models.CharField(max_length=10)  # Código del subprincipio
    subtitle = models.CharField(max_length=255)  # Título del subprincipio
    description = models.TextField()  # Descripción del subprincipio
    example = models.TextField()  # Ejemplo del subprincipio
    heuristic_id = models.ForeignKey('Heuristic', related_name='subprinciples', on_delete=models.CASCADE)  # Relación con el modelo Heuristic (una heurística puede tener varios subprincipios)

    def __str__(self):
        """
        Devuelve una representación legible del modelo Subprinciple.

        Returns:
            str: El título del subprincipio.
        """
        return self.subtitle
    
# Modelo para representar una captura de pantalla en la base de datos
class Screenshot(models.Model):
    url = models.URLField(max_length=500)  # URL del prototipo a capturar pantalla (máximo 500 caracteres)
    image_path = models.CharField(max_length=255)  # Ruta del archivo de la imagen
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación de la captura de pantalla (automática)

    def __str__(self):
        """
        Devuelve una representación legible del modelo Screenshot.

        Returns:
            str: La URL de la captura de pantalla.
        """
        return self.url

#//////////////////////////////////////////////////////////////////////////////////////////////////

# Modelo para representar una prueba de diseño en la base de datos
class DesignTest(models.Model):
    test_id = models.AutoField(primary_key=True) # Llave primaria que se genera automaticamente
    user_name = models.CharField(max_length=150, null=True, blank=True) # Nombre de quien creó la prueba de diseño
    name = models.CharField(max_length=50, null=False) # Nombre de la prueba de diseño
    url = models.URLField(max_length=500, null=False) # URL (valida) de la prueba de diseño
    description = models.CharField(max_length=500, null=False, default='N/A') # Descripcion de la prueba de diseño
    test_type = models.CharField(max_length=6, choices=[('Movil', 'Movil'), ('Web', 'Web'), ('Tablet', 'Tablet')],null=False, blank=True) # Tipo de prueba
    has_heuristics = models.BooleanField(default=False) # Indica si la prueba tiene heuristicas (True/False)
    created_at = models.DateTimeField(default=timezone.now, editable=False) # Fecha y hora de la creacion de la prueba (automatico)
    code = models.CharField(max_length=12, unique=True, null=True, blank=True) # Codigo generado unicamente para la prueba de diseño


    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True) #Llave forence del id del usuario que creó la prueba

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save() para generar un código único si no se ha proporcionado.

        Esta implementación asegura que cada instancia de DesignTest tenga un código único,
        que se genera usando los primeros 10 caracteres de un UUID.

        Args:
            *args: Argumentos posicionales.
            **kwargs: Argumentos con nombre.
        """
        if not self.code:
            # Generar un código único utilizando un UUID
            self.code = str(uuid.uuid4())[:10]
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Devuelve una representación legible del modelo, incluyendo el nombre del creador si está disponible.
        """
        return f"{self.name} - Creador: {self.user.username if self.user else 'Desconocido'}"   

# Modelo para representar una pregunta asociada a una prueba de diseño
class DesignQuestion(models.Model):
    question_id = models.AutoField(primary_key=True)  # Llave primaria que se genera automáticamente
    title = models.CharField(max_length=255)  # Título de la pregunta (máximo 255 caracteres)
    description = models.TextField()  # Descripción de la pregunta
    url_frame = models.URLField(max_length=500)  # URL de la pantalla de la pregunta (máximo 500 caracteres)
    response_type = models.CharField(max_length=12, choices=[('Calificacion', 'Calificación'), ('Legibilidad', 'Legibilidad'), ('Coherencia', 'Coherencia')], null=True, blank=True)  # Tipo de respuesta asociada a la pregunta (opcional)

    heuristics = models.ManyToManyField('Heuristic', blank=True)  # Relación con las heurísticas (opcional)
    test_id = models.ForeignKey('DesignTest', on_delete=models.CASCADE)  # Relación con la prueba de diseño asociada

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save() para eliminar heurísticas si la prueba de diseño no tiene heurísticas.

        Args:
            *args: Argumentos posicionales.
            **kwargs: Argumentos con nombre.
        """
        super().save(*args, **kwargs)  # Guarda primero la instancia

        # Si la prueba no tiene heurísticas, limpia las heurísticas asociadas
        if self.test_id and not self.test_id.has_heuristics:
            self.heuristics.clear()

    def __str__(self):
        """
        Devuelve una representación legible del modelo DesignQuestion.

        Returns:
            str: El título de la pregunta.
        """
        return self.title

# Modelo para representar el acceso a una prueba de diseño en la base de datos
class EvaluatorAccess(models.Model):
    access_id = models.AutoField(primary_key=True)  # Llave primaria que se genera automáticamente
    acceso_bloqueado = models.BooleanField(default=True)  # Indica si el acceso está bloqueado (True/False)
    accessed_at = models.DateTimeField(default=timezone.now)  # Fecha y hora de acceso a la prueba de diseño
    is_hidden = models.BooleanField(default=False)  # Indica si el acceso está oculto (True/False)

    evaluator_id = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)  # Relación con el usuario evaluador
    test_id = models.ForeignKey('DesignTest', on_delete=models.CASCADE, null=True, blank=True)  # Relación con la prueba de diseño

    def __str__(self):
        """
        Devuelve una representación legible del modelo EvaluatorAccess.

        Returns:
            str: Información sobre el acceso del evaluador a la prueba.
        """
        return f"Acceso del evaluador {self.evaluator_id} a la prueba {self.test_id}"


# Modelo para representar las respuestas estándar dadas por los evaluadores
class EvaluatorStandardResponse(models.Model):
    standard_response_id = models.AutoField(primary_key=True)  # Llave primaria que se genera automáticamente
    response_type = models.CharField(
        max_length=12,
        choices=[
            ('Calificacion', 'Calificación'),
            ('Legibilidad', 'Legibilidad'),
            ('Coherencia', 'Coherencia')
        ],
        null=False,
        blank=False
    )  # Tipo de respuesta (obligatorio)
    response_value = models.IntegerField(null=False, blank=False)  # Valor de la respuesta (obligatorio)
    comment = models.TextField(max_length=200, blank=True, null=True, default='')  # Comentario opcional
    created_at = models.DateTimeField(default=timezone.now)  # Fecha de creación de la respuesta
    is_complete = models.BooleanField(default=False)  # Indica si la respuesta está completa

    evaluator_access = models.ForeignKey('EvaluatorAccess', on_delete=models.SET_NULL, null=True, blank=True)  # Relación con el acceso del evaluador
    evaluator = models.ForeignKey('User', on_delete=models.CASCADE)  # Relación con el evaluador
    test = models.ForeignKey('DesignTest', on_delete=models.CASCADE)  # Relación con la prueba de diseño
    question = models.ForeignKey('DesignQuestion', on_delete=models.CASCADE)  # Relación con la pregunta

    def __str__(self):
        """
        Devuelve una representación legible del modelo EvaluatorStandardResponse.

        Returns:
            str: Información sobre la respuesta estándar del evaluador.
        """
        return f"Respuesta de -> {self.evaluator.username} para la prueba de diseño: {self.test.name}"


# Modelo para representar las respuestas con heurísticas dadas por los evaluadores
class EvaluatorHeuristicResponse(models.Model):
    heuristic_response_id = models.AutoField(primary_key=True)  # Llave primaria que se genera automáticamente
    score = models.IntegerField(null=False, blank=False)  # Puntaje asignado por el evaluador (obligatorio)
    comment = models.TextField(max_length=200, blank=True, null=True, default='')  # Comentario opcional sobre la respuesta
    created_at = models.DateTimeField(default=timezone.now)  # Fecha de creación de la respuesta (automatico)
    is_complete = models.BooleanField(default=False)  # Indica si la respuesta está completa

    evaluator_access = models.ForeignKey('EvaluatorAccess', on_delete=models.SET_NULL, null=True, blank=True)  # Relación con el acceso del evaluador
    test = models.ForeignKey('DesignTest', on_delete=models.CASCADE)  # Relación con la prueba de diseño
    question = models.ForeignKey('DesignQuestion', on_delete=models.CASCADE)  # Relación con la pregunta específica
    evaluator = models.ForeignKey('User', on_delete=models.CASCADE)  # Relación con el evaluador que dio la respuesta
    subprinciple = models.ForeignKey('Subprinciple', on_delete=models.CASCADE)  # Relación con el subprincipio evaluado

    def __str__(self):
        """
        Devuelve una representación legible del modelo EvaluatorHeuristicResponse.

        Returns:
            str: Información sobre la respuesta heurística del evaluador.
        """
        return f"Respuesta de -> {self.evaluator.username} para la prueba de diseño {self.test.name}"

    
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class HeuristicOwner(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=False, null=False)
    url = models.TextField(blank=False, null=False)
    description =models.TextField(blank=False, null=False)

class  HeuristicCheckList(models.Model):
    id = models.AutoField(primary_key=True)
    owner= models.ForeignKey(HeuristicOwner, on_delete=models.CASCADE)
    H01P01 = models.BooleanField( null=False)
    H01P02 = models.BooleanField( null=False)
    H01P03 = models.BooleanField( null=False)
    H01P04 = models.BooleanField( null=False)
    H01P05 = models.BooleanField( null=False)
    H01P06 = models.BooleanField( null=False)
    H01P07 = models.BooleanField( null=False)

    H02P01 = models.BooleanField( null=False)
    H02P02 = models.BooleanField( null=False)
    H02P03 = models.BooleanField( null=False)
    H02P04 = models.BooleanField( null=False)
    H02P05 = models.BooleanField( null=False)
    H02P06 = models.BooleanField( null=False)
    H02P07 = models.BooleanField( null=False)
    H02P08 = models.BooleanField( null=False)

    H03P01 = models.BooleanField( null=False)
    H03P02 = models.BooleanField( null=False)
    H03P03 = models.BooleanField( null=False)
    H03P04 = models.BooleanField( null=False)
    H03P05 = models.BooleanField( null=False)
    H03P06 = models.BooleanField( null=False)
    H03P06 = models.BooleanField( null=False)
    H04P01 = models.BooleanField( null=False)
    H04P02 = models.BooleanField( null=False)
    H04P03 = models.BooleanField( null=False)
    H04P04 = models.BooleanField( null=False)
    H04P05 = models.BooleanField( null=False)
    H04P06 = models.BooleanField( null=False)
    H04P07 = models.BooleanField( null=False)
    H04P08 = models.BooleanField( null=False)
    H04P09 = models.BooleanField( null=False)
    H04P10 = models.BooleanField( null=False)
    H04P11 = models.BooleanField( null=False)
    H04P12 = models.BooleanField( null=False)
    H04P13 = models.BooleanField( null=False)
    H05P01 = models.BooleanField( null=False)
    H05P02 = models.BooleanField( null=False)
    H05P03 = models.BooleanField( null=False)
    H05P04 = models.BooleanField( null=False)
    H05P05 = models.BooleanField( null=False)
    H06P01 = models.BooleanField( null=False)
    H06P02 = models.BooleanField( null=False)
    H06P03 = models.BooleanField( null=False)
    H07P01 = models.BooleanField( null=False)
    H07P02 = models.BooleanField( null=False)
    H07P03 = models.BooleanField( null=False)
    H07P04 = models.BooleanField( null=False)
    H07P05 = models.BooleanField( null=False)
    H07P06 = models.BooleanField( null=False)
    H07P07 = models.BooleanField( null=False)
    H08P01 = models.BooleanField( null=False)
    H08P02 = models.BooleanField( null=False)
    H08P03 = models.BooleanField( null=False)
    H08P04 = models.BooleanField( null=False)
    H08P05 = models.BooleanField( null=False)
    H08P06 = models.BooleanField( null=False)
    H08P07 = models.BooleanField( null=False)
    H08P08 = models.BooleanField( null=False)
    H08P09 = models.BooleanField( null=False)
    H08P10 = models.BooleanField( null=False)
    H08P11 = models.BooleanField( null=False)
    H09P01 = models.BooleanField( null=False)
    H09P02 = models.BooleanField( null=False)
    H09P03 = models.BooleanField( null=False)
    H09P04 = models.BooleanField( null=False)
    H09P05 = models.BooleanField( null=False)
    H09P06 = models.BooleanField( null=False)
    H10P01 = models.BooleanField( null=False)
    H10P02 = models.BooleanField( null=False)
    H10P03 = models.BooleanField( null=False)
    H10P04 = models.BooleanField( null=False)
    H10P05 = models.BooleanField( null=False)
    H10P06 = models.BooleanField( null=False)
    H10P07 = models.BooleanField( null=False)
    H10P08 = models.BooleanField( null=False)
    H10P09 = models.BooleanField( null=False)
    OBSERVACIONH1 = models.TextField( max_length=300, null=False)
    OBSERVACIONH2 = models.TextField( max_length=300, null=False)
    OBSERVACIONH3 = models.TextField( max_length=300, null=False)
    OBSERVACIONH4 = models.TextField( max_length=300, null=False)
    OBSERVACIONH5 = models.TextField( max_length=300, null=False)
    OBSERVACIONH6 = models.TextField( max_length=300, null=False)
    OBSERVACIONH7 = models.TextField( max_length=300, null=False)
    OBSERVACIONH8 = models.TextField( max_length=300, null=False)
    OBSERVACIONH9 = models.TextField( max_length=300, null=False)
    OBSERVACIONH10 = models.TextField( max_length=300, null=False)
   
class HeuristicEvaluations(models.Model):
    owner= models.ForeignKey(HeuristicOwner, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=False)
    description = models.CharField(max_length=250, null=False)
    hi = models.CharField(max_length=250, null=False)
    incidents = models.IntegerField(null=False)
    severity = models.IntegerField(null=False)
    frequency = models.IntegerField(null=False)
    criticism = models.IntegerField(null=False)

    def __str__(self):
        return '%s:%s:%s:%s:%s:%s:%s:%s'%(self.owner, self.name, self.description,  self.hi, self.incidents, self.severity,self.frequency ,self.criticism)

class HeuristicDescriptions(models.Model):
     id = models.AutoField(primary_key=True)
     name = models.TextField(blank=False, null=False)
     description = models.TextField(blank=False, null=False)

    
class PorcentajeCheckList(models.Model):
    id = models.AutoField(primary_key=True)
    user_username = models.ForeignKey(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=50)
    suma_si = models.IntegerField(null=True, blank=True)
    suma_no = models.IntegerField(null=True, blank=True)
    porcentaje_si = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    porcentaje_no = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


class EvaluatorInfo(models.Model):
    evaluator_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, null=False)
    age = models.IntegerField(null=True, blank=True)
    profession = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    technological_experience = models.CharField(max_length=255, null=True, blank=True)
    personality_description = models.CharField(max_length=255, null=True, blank=True)
    goals = models.CharField(max_length=255, null=True, blank=True)
    habits = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return self.username