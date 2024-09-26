from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from aplications.models import EvaluatorAccess, DesignTest, EvaluatorStandardResponse
from aplications.serializers import EvaluatorAccessSerializer
from django.utils import timezone
from django.shortcuts import get_object_or_404

# Vista para gestionar el acceso de los evaluadores a las pruebas de diseño
@api_view(['GET', 'POST'])
def API_Access_DesignTest(request, evaluator_id):
    """
    GET: Devuelve la lista de pruebas de diseño accesibles para un evaluador específico.
    POST: Crea o desbloquea el acceso de un evaluador a una prueba de diseño.
    
    Parámetros:
    - evaluator_id: ID del evaluador.
    """
    if request.method == 'POST':
        data = request.data
        code = data.get('code')

        # Buscar la prueba de diseño basada en el código proporcionado
        design_test = get_object_or_404(DesignTest, code=code)

        # Verificar si ya existe el acceso para el evaluador a esa prueba
        existing_access = EvaluatorAccess.objects.filter(evaluator_id=evaluator_id, test_id=design_test).first()

        if not existing_access:
            # Crear un nuevo acceso desbloqueado para el evaluador
            new_access = EvaluatorAccess.objects.create(
                evaluator_id_id=evaluator_id,
                test_id=design_test,
                accessed_at=timezone.now(),
                acceso_bloqueado=False  # Desbloquear acceso al crear
            )
            serializer = EvaluatorAccessSerializer(new_access)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Si el acceso ya existe, se asegura de que esté desbloqueado
            if existing_access.acceso_bloqueado:
                existing_access.acceso_bloqueado = False
                existing_access.accessed_at = timezone.now()  # Actualizar tiempo de acceso
                existing_access.save()

            # Devolver los datos del acceso existente
            serializer = EvaluatorAccessSerializer(existing_access)
            return Response(serializer.data, status=status.HTTP_200_OK)

    # Método GET para obtener todas las pruebas accesibles para el evaluador
    if request.method == 'GET':
        access_entries = EvaluatorAccess.objects.filter(evaluator_id=evaluator_id, is_hidden=False)

        if not access_entries:
            return Response([], status=status.HTTP_200_OK)

        tests_data = []
        # Iterar sobre cada acceso y construir la respuesta
        for access in access_entries:
            design_test = access.test_id  # Obtener el objeto DesignTest

            # Verificar si hay respuestas completadas para esta prueba
            responses_complete = EvaluatorStandardResponse.objects.filter(
                evaluator_id=evaluator_id, test_id=design_test, is_complete=True
            ).exists()

            # Construir los datos de cada prueba accesible
            tests_data.append({
                'access_id': access.access_id,
                'acceso_bloqueado': access.acceso_bloqueado,
                'accessed_at': access.accessed_at,
                'is_hidden': access.is_hidden,
                'is_complete': responses_complete,  # Verificar si la prueba está completa
                'evaluator_id': access.evaluator_id_id,
                'test_id': design_test.test_id,
                'code': design_test.code,
                'name': design_test.name,
                'url': design_test.url,
                'description': design_test.description,
                'test_type': design_test.test_type,
                'created_at': design_test.created_at,
                'has_heuristics': design_test.has_heuristics,
            })

        return Response(tests_data, status=status.HTTP_200_OK)

# Vista para ocultar el acceso de un evaluador a una prueba de diseño
@api_view(['POST'])
def HIDE_Access_DesignTest(request, test_id):
    """
    POST: Oculta el acceso de un evaluador a una prueba de diseño específica.
    
    Parámetros:
    - test_id: ID de la prueba de diseño.
    - evaluator_id: ID del evaluador (en el cuerpo de la solicitud).
    """
    evaluator_id = request.data.get('evaluator_id')

    try:
        # Buscar el acceso del evaluador a la prueba de diseño
        access = EvaluatorAccess.objects.get(test_id=test_id, evaluator_id=evaluator_id)
    except EvaluatorAccess.DoesNotExist:
        return Response({"message": "Acceso no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    # Actualizar el campo 'is_hidden' para ocultar el acceso
    serializer = EvaluatorAccessSerializer(access, data={'is_hidden': True}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Acceso ocultado exitosamente"}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista para mostrar nuevamente el acceso de un evaluador a una prueba de diseño
@api_view(['POST'])
def SHOW_Access_DesignTest(request, test_id):
    """
    POST: Muestra nuevamente el acceso de un evaluador a una prueba de diseño específica.
    
    Parámetros:
    - test_id: ID de la prueba de diseño.
    - evaluator_id: ID del evaluador (en el cuerpo de la solicitud).
    """
    evaluator_id = request.data.get('evaluator_id')

    try:
        access = EvaluatorAccess.objects.get(test_id=test_id, evaluator_id=evaluator_id)
    except EvaluatorAccess.DoesNotExist:
        return Response({"message": "Acceso no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    serializer = EvaluatorAccessSerializer(access, data={'is_hidden': False}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Acceso mostrado exitosamente"}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
