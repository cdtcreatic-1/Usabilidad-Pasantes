from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from aplications.models import EvaluatorStandardResponse, EvaluatorAccess, DesignQuestion, DesignTest

# Vista para gestionar respuestas parciales o en curso de un evaluador en una prueba de diseño
@api_view(['GET', 'POST'])
def API_EvaluatorStandardResponse(request, test_id, evaluator_id):
    """
    GET: Recupera las respuestas parciales guardadas de un evaluador en una prueba de diseño específica.
    POST: Guarda respuestas parciales para un evaluador en una prueba de diseño específica.
    
    Parámetros:
    - test_id: ID de la prueba de diseño.
    - evaluator_id: ID del evaluador.
    """

    # Verificar si el evaluador tiene acceso a la prueba de diseño.
    access = EvaluatorAccess.objects.filter(test_id=test_id, evaluator_id=evaluator_id).first()
    if not access:
        return Response({"error": "El evaluador no tiene acceso a esta prueba de diseño."}, status=status.HTTP_403_FORBIDDEN)

    # POST: Guardar respuestas parciales
    if request.method == 'POST':
        # Obtener el cuerpo de la solicitud, que contiene una lista de respuestas.
        responses_data = request.data.get('responses', [])

        # Iterar a través de cada respuesta en los datos proporcionados.
        for response_data in responses_data:
            question_id = response_data.get('question')
            response_value = response_data.get('response_value')
            comment = response_data.get('comment', '')

            if not question_id or not response_value:
                return Response({"error": "Faltan datos: se requiere 'question' y 'response_value'."}, status=status.HTTP_400_BAD_REQUEST)

            # Intentar obtener la pregunta asociada para validar que existe y que pertenece a la prueba de diseño especificada.
            try:
                question = DesignQuestion.objects.get(question_id=question_id, test_id=test_id)
            except DesignQuestion.DoesNotExist:
                return Response({"error": f"No se encontró la pregunta con ID {question_id} para este test."}, status=status.HTTP_404_NOT_FOUND)

            # Usar update_or_create para guardar o actualizar la respuesta.
            # Si la respuesta ya existe, se actualiza; si no, se crea una nueva.
            response, created = EvaluatorStandardResponse.objects.update_or_create(
                evaluator_id=evaluator_id,
                test_id=test_id,
                question_id=question_id,
                defaults={
                    'response_type': question.response_type,
                    'response_value': response_value,
                    'comment': comment,
                    'is_complete': False,
                    'evaluator_access': access
                }
            )
        return Response({"message": "Respuestas guardadas correctamente."}, status=status.HTTP_201_CREATED)

    # GET: Recuperar respuestas parciales guardadas del evaluador
    elif request.method == 'GET':
        # Buscar todas las respuestas parciales del evaluador para la prueba de diseño.
        responses = EvaluatorStandardResponse.objects.filter(test_id=test_id, evaluator_id=evaluator_id)

        if not responses.exists():
            return Response({"message": "No hay respuestas guardadas para esta prueba de diseño."}, status=status.HTTP_200_OK)

        # Crear una lista con las respuestas guardadas, junto con la información de las preguntas.
        data = []
        for response in responses:
            question = response.question  # Obtener la pregunta asociada a cada respuesta.
            response_data = {
                "question": {
                    "question_id": question.question_id,
                    "title": question.title,
                    "description": question.description,  
                    "url_frame": question.url_frame,
                    "response_type": question.response_type
                },
                "response_value": response.response_value,
                "comment": response.comment
            }
            data.append(response_data)

        return Response(data, status=status.HTTP_200_OK)
    

# Vista para finalizar las respuestas de un evaluador y bloquear el acceso a la prueba de diseño
@api_view(['GET', 'POST'])
def API_FinalizeAndGetStandardResponses(request, test_id):
    """
    GET: Recupera todas las respuestas completas de los evaluadores que hayan finalizado una prueba de diseño.
    POST: Finaliza las respuestas de un evaluador y bloquea su acceso a la prueba de diseño.
    
    Parámetros:
    - test_id: ID de la prueba de diseño.
    """

    # Verificar si el evaluador tiene acceso a la prueba de diseño.
    access = EvaluatorAccess.objects.filter(test_id=test_id).first()
    if not access:
        return Response({"error": "No tienes acceso a esta prueba de diseño."}, status=status.HTTP_403_FORBIDDEN)

    # POST: Finalizar las respuestas y bloquear el acceso del evaluador
    if request.method == 'POST':
        evaluator_id = request.data.get('evaluator_id')

        if not evaluator_id:
            return Response({"error": "Falta el evaluator_id en la solicitud."}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si el evaluador tiene acceso a la prueba de diseño.
        access = EvaluatorAccess.objects.filter(test_id=test_id, evaluator_id=evaluator_id).first()
        if not access:
            return Response({"error": "El evaluador no tiene acceso a esta prueba de diseño."}, status=status.HTTP_403_FORBIDDEN)

        if access.acceso_bloqueado:
            return Response({"error": "El acceso ya está bloqueado. No puedes enviar más respuestas."}, status=status.HTTP_403_FORBIDDEN)

        # Procesar cada respuesta enviada en el cuerpo de la solicitud.
        responses_data = request.data.get('responses', [])
        for response_data in responses_data:
            question_id = response_data.get('question')
            response_value = response_data.get('response_value')
            comment = response_data.get('comment', '')

            # Validar que se haya enviado la pregunta y la respuesta.
            if not question_id or response_value is None:
                return Response({"error": "Faltan datos: se requiere 'question' y 'response_value'."}, status=status.HTTP_400_BAD_REQUEST)

            # Verificar que la pregunta existe y pertenece a la prueba de diseño.
            try:
                question = DesignQuestion.objects.get(question_id=question_id, test_id=test_id)
            except DesignQuestion.DoesNotExist:
                return Response({"error": f"No se encontró la pregunta con ID {question_id} para este test."}, status=status.HTTP_404_NOT_FOUND)

            # Guardar o actualizar la respuesta, marcándola como completa.
            response, created = EvaluatorStandardResponse.objects.update_or_create(
                evaluator_id=evaluator_id,
                test_id=test_id,
                question_id=question_id,
                defaults={
                    'response_type': question.response_type,
                    'response_value': response_value,
                    'comment': comment,
                    'is_complete': True,
                    'evaluator_access': access
                }
            )

        # Bloquear el acceso del evaluador a la prueba de diseño después de finalizar las respuestas.
        access.acceso_bloqueado = True
        access.save()

        return Response({"message": "Respuestas finalizadas y acceso bloqueado."}, status=status.HTTP_200_OK)

    # GET: Recuperar respuestas completas de evaluadores que han terminado la prueba.
    elif request.method == 'GET':
        try:
            design_test = DesignTest.objects.get(test_id=test_id)
        except DesignTest.DoesNotExist:
            return Response({"error": "La prueba de diseño no existe."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener todas las preguntas asociadas a la prueba de diseño.
        questions = DesignQuestion.objects.filter(test_id=test_id)
        if not questions.exists():
            return Response({"error": "No hay preguntas asociadas a esta prueba de diseño."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener todos los evaluadores que han completado la prueba (acceso bloqueado).
        evaluator_accesses = EvaluatorAccess.objects.filter(test_id=test_id, acceso_bloqueado=True)

        # Estructurar los datos de las respuestas para cada evaluador.
        response_data = {
            "design_test": {
                "test_id": design_test.test_id,
                "name": design_test.name,
                "url": design_test.url,
                "description": design_test.description,
                "test_type": design_test.test_type,
                "has_heuristics": design_test.has_heuristics,
                "created_at": design_test.created_at,
                "code": design_test.code
            },
            "evaluators": []
        }

        # Recorrer cada evaluador que haya finalizado la prueba.
        for access in evaluator_accesses:
            evaluator = access.evaluator_id

            # Obtener todas las respuestas completas del evaluador.
            responses = EvaluatorStandardResponse.objects.filter(test_id=test_id, evaluator_id=evaluator.id, is_complete=True)

            # Estructurar los datos del evaluador y sus respuestas.
            evaluator_data = {
                "evaluator_id": evaluator.id,
                "username": evaluator.username,
                "email": evaluator.email,
                "responses": []
            }

            # Añadir cada pregunta y la respuesta del evaluador.
            for question in questions:
                response = responses.filter(question=question).first()

                question_data = {
                    "question": {
                        "question_id": question.question_id,
                        "title": question.title,
                        "description": question.description,
                        "url_frame": question.url_frame
                    },
                    "response": {
                        "response_type": response.response_type if response else None,
                        "response_value": response.response_value if response else None,
                        "comment": response.comment if response else None
                    }
                }

                evaluator_data["responses"].append(question_data)

            # Añadir el evaluador y sus respuestas a la lista general.
            response_data["evaluators"].append(evaluator_data)

        # Devolver las respuestas completas de los evaluadores.
        return Response(response_data, status=status.HTTP_200_OK)
