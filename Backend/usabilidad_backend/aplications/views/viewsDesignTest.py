from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from aplications.models import DesignTest
from aplications.serializers import DesignTestSerializer
from django.core.exceptions import ValidationError

# Vista para listar todas las pruebas de diseño o crear una nueva
@api_view(['GET', 'POST'])
def API_DesignTest(request):
    """
    GET: Devuelve una lista de todas las pruebas de diseño.
    POST: Crea una nueva prueba de diseño con los datos proporcionados.
    """
    try:
        if request.method == 'GET':
            # Obtener todas las pruebas de diseño
            design_tests = DesignTest.objects.all()
            serializer = DesignTestSerializer(design_tests, many=True)
            return JsonResponse(serializer.data, safe=False)
        
        elif request.method == 'POST':
            # Crear una nueva prueba de diseño
            data = JSONParser().parse(request)

            # Asegurarse de que tanto el ID como el nombre de usuario estén presentes en los datos
            user_id = data.get('user')
            user_name = data.get('user_name')

            if not user_id or not user_name:
                return JsonResponse({"error": "Faltan los campos 'user' o 'user_name'."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = DesignTestSerializer(data=data)

            if serializer.is_valid():
                # Guardar la prueba de diseño con el user y el user_name enviados desde el frontend
                serializer.save(user_id=user_id, user_name=user_name)
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except ValidationError as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"Error: {str(e)}")  # Esto te ayudará a depurar en la consola de Django
        return JsonResponse({"error": "Ocurrió un error inesperado. Por favor, inténtalo de nuevo más tarde."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Vista para listar todas las pruebas de diseño por evaluador
@api_view(['GET'])
def API_DesignTests_ByUser(request, user):
    """
    GET: Devuelve una lista de todas las pruebas de diseño que pertenecen a un usuario específico.
    
    Parámetros:
    - user_id: ID del usuario.
    """
    try:
        # Obtener todas las pruebas de diseño del usuario
        design_tests = DesignTest.objects.filter(user_id=user)
        serializer = DesignTestSerializer(design_tests, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({"error": "Ocurrió un error al obtener las pruebas de diseño."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Vista para obtener, actualizar o eliminar una prueba de diseño por su ID
@api_view(['GET', 'PUT', 'DELETE'])
def API_DesignTest_Details(request, pk):
    """
    GET: Devuelve los detalles de una prueba de diseño específica.
    PUT: Actualiza una prueba de diseño existente.
    DELETE: Elimina una prueba de diseño existente.
    
    Parámetros:
    - pk: ID de la prueba de diseño.
    """
    try:
        # Buscar la prueba de diseño por su ID
        design_test = DesignTest.objects.get(test_id=pk)
    except DesignTest.DoesNotExist:
        return JsonResponse({"error": "La prueba de diseño no existe."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({"error": "Ocurrió un error al buscar la prueba de diseño."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        if request.method == 'GET':
            # Devolver los detalles de la prueba de diseño
            serializer = DesignTestSerializer(design_test)
            return JsonResponse(serializer.data, safe=False)
        
        elif request.method == 'PUT':
            # Actualizar la prueba de diseño
            data = JSONParser().parse(request)
            serializer = DesignTestSerializer(design_test, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_202_ACCEPTED)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            # Eliminar la prueba de diseño
            design_test.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    except ValidationError as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({"error": "Ocurrió un error inesperado. Por favor, inténtalo de nuevo más tarde."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Vista para verificar si el codigo ya está en uso
@api_view(['GET'])
def API_CheckCodeAvailability(request, code):
    """
    Verifica si el código ya está en uso.
    """
    try:
        # Buscar si existe una prueba con ese código
        exists = DesignTest.objects.filter(code=code).exists()
        return JsonResponse({'exists': exists})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({"error": "Ocurrió un error al verificar el código."}, status=500)
