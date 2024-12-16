from django.http import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import ParseError
from aplications.models import DesignQuestion, DesignTest, Heuristic
from aplications.serializers import DesignQuestionSerializer, HeuristicSerializer
from django.db import IntegrityError

# Vista para obtener todas las heurísticas con sus subprincipios
@api_view(['GET'])
def API_GetHeuristics(request):
    """
    GET: Devuelve todas las heurísticas y sus subprincipios.
    """
    try:
        heuristics = Heuristic.objects.all()  # Obtener todas las heurísticas
        serializer = HeuristicSerializer(heuristics, many=True)  # Usar el nuevo serializer que incluye subprincipios
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": f"Ocurrió un error inesperado al obtener las heurísticas: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Vista para verificar si la prueba tiene heuristicas
@api_view(['GET'])
def API_CheckHeuristics(request, test_id):
    try:
        design_test = DesignTest.objects.get(pk=test_id)
        return JsonResponse({'hasHeuristics': design_test.has_heuristics})
    except DesignTest.DoesNotExist:
        return JsonResponse({"error": "La prueba de diseño no existe."}, status=404)


# Vista para obtener todas las preguntas de diseño
@api_view(['GET'])
def API_AllDesignQuestions(request):
    """
    GET: Devuelve todas las preguntas de diseño almacenadas en la base de datos.
    """
    try:
        questions = DesignQuestion.objects.all()  # Obtener todas las preguntas de diseño
        serializer = DesignQuestionSerializer(questions, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Exception as e:
        return Response({"error": "Ocurrió un error inesperado al obtener todas las preguntas de diseño."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Vista para manejar las preguntas de diseño asociadas a una prueba de diseño
@api_view(['GET', 'POST'])
def API_DesignQuestions(request, test_id):
    """
    GET: Devuelve todas las preguntas de diseño asociadas a una prueba de diseño específica.
    POST: Crea una nueva pregunta de diseño para una prueba de diseño específica.
    
    Parámetros:
    - test_id: ID de la prueba de diseño asociada.
    """
    try:
        design_test = DesignTest.objects.get(pk=test_id)  # Obtener la prueba de diseño por ID
    except DesignTest.DoesNotExist:
        return Response({"error": "La prueba de diseño no existe."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Ocurrió un error inesperado al buscar la prueba de diseño: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'GET':
        try:
            questions = DesignQuestion.objects.filter(test_id=design_test)  # Filtrar preguntas por prueba de diseño
            serializer = DesignQuestionSerializer(questions, many=True)
            return JsonResponse(serializer.data, safe=False)
        except Exception as e:
            return Response({"error": f"Ocurrió un error inesperado al obtener las preguntas de diseño: {str(e)}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'POST':
        try:
            data = JSONParser().parse(request)  # Parsear el cuerpo de la solicitud
        except ParseError:
            return JsonResponse({"error": "El cuerpo de la solicitud no es un JSON válido."}, status=status.HTTP_400_BAD_REQUEST)

        data['test_id'] = test_id  # Asociar la pregunta con la prueba de diseño correcta
        serializer = DesignQuestionSerializer(data=data)

        if serializer.is_valid():
            if design_test.has_heuristics:
                if serializer.validated_data.get('response_type'):
                    return JsonResponse(
                        {"error": "No se puede definir 'response_type' para una pregunta con heurísticas."}, status=status.HTTP_400_BAD_REQUEST)
                if not serializer.validated_data.get('heuristics'):
                    return JsonResponse(
                        {"error": "Debe proporcionar al menos una heurística cuando 'has_heuristics' es verdadero."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if serializer.validated_data.get('heuristics'):
                    return JsonResponse(
                        {"error": "No se pueden definir 'heuristics' para una pregunta sin heurísticas."}, status=status.HTTP_400_BAD_REQUEST)
                if serializer.validated_data.get('response_type') is None:
                    return JsonResponse(
                        {"error": "El campo 'response_type' no puede ser nulo para una pregunta sin heurísticas."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                question = serializer.save()  # Guardar la pregunta de diseño
                result_serializer = DesignQuestionSerializer(question)
                return JsonResponse(result_serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                return JsonResponse({"error": f"Error de integridad de datos: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return JsonResponse({"error": f"Ocurrió un error inesperado: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista para obtener, actualizar o eliminar una pregunta de diseño específica
@api_view(['GET', 'PUT', 'DELETE'])
def API_DesignQuestions_Details(request, test_id, question_id):
    """
    GET: Devuelve los detalles de una pregunta de diseño específica.
    PUT: Actualiza una pregunta de diseño existente.
    DELETE: Elimina una pregunta de diseño existente.
    
    Parámetros:
    - test_id: ID de la prueba de diseño asociada.
    - question_id: ID de la pregunta de diseño específica.
    """
    try:
        design_test = DesignTest.objects.get(pk=test_id)  # Obtener la prueba de diseño por ID
    except DesignTest.DoesNotExist:
        return Response({"error": "La prueba de diseño no existe."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Ocurrió un error inesperado al buscar la prueba de diseño: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        question = DesignQuestion.objects.get(pk=question_id, test_id=design_test)  # Obtener la pregunta de diseño
    except DesignQuestion.DoesNotExist:
        return Response({"error": "La pregunta de diseño no existe."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Ocurrió un error inesperado al buscar la pregunta de diseño: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'GET':
        try:
            serializer = DesignQuestionSerializer(question)
            return JsonResponse(serializer.data, safe=False)
        except Exception as e:
            return Response({"error": f"Ocurrió un error inesperado: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'PUT':
        try:
            data = JSONParser().parse(request)  # Parsear el cuerpo de la solicitud
        except ParseError:
            return JsonResponse({"error": "El cuerpo de la solicitud no es un JSON válido."}, status=status.HTTP_400_BAD_REQUEST)

        data['test_id'] = test_id  # Asegurar que se asocie con la prueba de diseño correcta
        serializer = DesignQuestionSerializer(question, data=data)

        if serializer.is_valid():
            if design_test.has_heuristics:
                if serializer.validated_data.get('response_type'):
                    return JsonResponse(
                        {"error": "No se puede definir 'response_type' para una pregunta con heurísticas."},status=status.HTTP_400_BAD_REQUEST)
            else:
                if serializer.validated_data.get('heuristics'):
                    return JsonResponse(
                        {"error": "No se pueden definir 'heuristics' para una pregunta sin heurísticas."},status=status.HTTP_400_BAD_REQUEST)

            try:
                question = serializer.save()  # Actualizar la pregunta de diseño
                result_serializer = DesignQuestionSerializer(question)
                return JsonResponse(result_serializer.data, status=status.HTTP_202_ACCEPTED)
            except IntegrityError as e:
                return JsonResponse({"error": f"Error de integridad de datos al actualizar: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return JsonResponse({"error": f"Ocurrió un error inesperado al actualizar la pregunta de diseño: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        try:
            question.delete()  # Eliminar la pregunta de diseño
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": f"Ocurrió un error inesperado al eliminar la pregunta de diseño: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
