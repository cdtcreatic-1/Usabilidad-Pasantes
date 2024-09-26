from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from aplications.models import EvaluatorHeuristicResponse, EvaluatorAccess, Subprinciple, DesignTest, DesignQuestion

# Vista para gestionar las respuestas parciales de un evaluador en una prueba de diseño con heurísticas
@api_view(['GET', 'POST'])
def API_EvaluatorHeuristicResponse(request, test_id, evaluator_id):
    """
    GET: Recupera las respuestas parciales de un evaluador en una prueba de diseño con heurísticas.
    POST: Guarda respuestas parciales para un evaluador en una prueba de diseño con heurísticas.
    
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
        responses_data = request.data.get('heuristics', [])

        if not responses_data:
            return Response({"error": "No se proporcionaron respuestas para guardar."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Procesar cada heurística enviada
            for heuristic_data in responses_data:
                heuristic_code = heuristic_data.get('heuristic_code')
                comment = heuristic_data.get('comment', '')  # Comentario a nivel de heurística
                subprinciples_data = heuristic_data.get('subprinciples', [])

                if not heuristic_code or not subprinciples_data:
                    return Response({"error": "Faltan datos: se requiere 'heuristic_code' y al menos un subprincipio."}, status=status.HTTP_400_BAD_REQUEST)

                # Procesar cada subprincipio dentro de la heurística
                for subprinciple_data in subprinciples_data:
                    subprinciple_code = subprinciple_data.get('subprinciple_code')
                    response_value = subprinciple_data.get('response_value')

                    if not subprinciple_code or response_value is None:
                        return Response({"error": "Faltan datos: se requiere 'subprinciple_code' y 'response_value'."}, status=status.HTTP_400_BAD_REQUEST)

                    # Buscar el subprincipio usando el código proporcionado
                    try:
                        subprinciple = Subprinciple.objects.get(code=subprinciple_code)
                    except Subprinciple.DoesNotExist:
                        return Response({"error": f"No se encontró el subprincipio con código {subprinciple_code}."}, status=status.HTTP_404_NOT_FOUND)

                    # Guardar o actualizar las respuestas del subprincipio para el evaluador
                    EvaluatorHeuristicResponse.objects.update_or_create(
                        evaluator_id=evaluator_id,
                        test_id=test_id,
                        question_id=request.data.get('question_id'),
                        subprinciple=subprinciple,
                        defaults={
                            'score': response_value,
                            'comment': comment,  # Guardamos el comentario a nivel de heurística aquí
                            'is_complete': False,  # Sigue siendo respuesta parcial
                            'evaluator_access': access
                        }
                    )

            return Response({"message": "Respuestas guardadas correctamente."}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error": f"Ocurrió un error al procesar las respuestas: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # GET: Recuperar respuestas parciales guardadas
    elif request.method == 'GET':
        # Obtener todas las respuestas parciales del evaluador
        responses = EvaluatorHeuristicResponse.objects.filter(test_id=test_id, evaluator_id=evaluator_id)

        if not responses.exists():
            return Response({"message": "No hay respuestas guardadas para esta prueba de diseño."}, status=status.HTTP_200_OK)

        # Estructurar la respuesta que incluye las respuestas parciales y los subprincipios
        data = []
        for response in responses:
            heuristic = response.subprinciple.heuristic_id  # Obtener la heurística asociada al subprincipio
            subprinciple = response.subprinciple

            response_data = {
                "question_id": response.question_id,
                "heuristic_code": heuristic.code,
                "subprinciple_code": subprinciple.code,
                "response_value": response.score,
                "comment": response.comment  # Retorna el comentario a nivel de heurística
            }
            data.append(response_data)

        # Devolver las respuestas parciales
        return Response(data, status=status.HTTP_200_OK)


# Vista para finalizar las respuestas del evaluador en una prueba de diseño con heurísticas y bloquear el acceso
@api_view(['GET', 'POST'])
def API_FinalizeAndGetHeuristicResponses(request, test_id):
    """
    GET: Recupera todas las respuestas completas de los evaluadores que hayan finalizado una prueba de diseño con heurísticas.
    POST: Finaliza las respuestas de un evaluador y bloquea su acceso a la prueba de diseño con heurísticas.
    
    Parámetros:
    - test_id: ID de la prueba de diseño.
    """

    try:
        # Verificar si la prueba de diseño existe
        design_test = DesignTest.objects.get(test_id=test_id)
    except DesignTest.DoesNotExist:
        return Response({"error": "La prueba de diseño no existe."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Obtener todas las preguntas asociadas a la prueba de diseño
        questions = DesignQuestion.objects.filter(test_id=test_id)
        if not questions.exists():
            return Response({"error": "No hay preguntas asociadas a esta prueba de diseño."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener todos los evaluadores que han completado la prueba de diseño
        evaluator_accesses = EvaluatorAccess.objects.filter(test_id=test_id, acceso_bloqueado=True)
        if not evaluator_accesses.exists():
            return Response({"error": "No hay evaluadores que hayan completado esta prueba."}, status=status.HTTP_404_NOT_FOUND)

        # Estructurar los datos para la respuesta
        response_data = {
            "design_test": {
                "test_id": design_test.test_id,
                "user_id": design_test.user_id,
                "username": design_test.user_name,
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

        # Recorrer todos los evaluadores que han completado la prueba
        for access in evaluator_accesses:
            evaluator = access.evaluator_id

            # Obtener respuestas completas del evaluador
            responses = EvaluatorHeuristicResponse.objects.filter(
                test_id=test_id, evaluator_id=evaluator.id, is_complete=True
            )
            if not responses.exists():
                continue  # Si no hay respuestas, continuar con el siguiente evaluador

            # Estructurar los datos para el evaluador y sus respuestas
            evaluator_data = {
                "evaluator_id": evaluator.id,
                "username": evaluator.username,
                "email": evaluator.email,
                "responses": []
            }

            # Recorrer todas las preguntas y añadir las respuestas del evaluador
            for question in questions:
                question_data = {
                    "question_id": question.question_id,
                    "title": question.title,
                    "description": question.description,
                    "url_frame": question.url_frame,
                    "heuristics": []
                }

                # Agrupar las respuestas del evaluador por heurística
                heuristics_dict = {}
                for response in responses.filter(question=question):
                    heuristic_code = response.subprinciple.heuristic_id.code
                    subprinciple_data = {
                        "subprinciple_code": response.subprinciple.code,
                        "subprinciple_subtitle": response.subprinciple.subtitle,
                        "subprinciple_description": response.subprinciple.description,
                        "response_value": response.score,
                    }

                    if heuristic_code not in heuristics_dict:
                        heuristics_dict[heuristic_code] = {
                            "heuristic_code": heuristic_code,
                            "heuristic_title": response.subprinciple.heuristic_id.title,
                            "comment": response.comment,  # Comentario a nivel de heurística
                            "subprinciples": []
                        }
                    heuristics_dict[heuristic_code]["subprinciples"].append(subprinciple_data)

                question_data["heuristics"] = list(heuristics_dict.values())
                evaluator_data["responses"].append(question_data)

            # Añadir el evaluador y sus respuestas a la lista de evaluadores
            response_data["evaluators"].append(evaluator_data)

        # Devolver las respuestas completas de los evaluadores
        return Response(response_data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        evaluator_id = request.data.get('evaluator_id')

        if not evaluator_id:
            return Response({"error": "Falta el evaluator_id en la solicitud."}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si el evaluador tiene acceso
        access = EvaluatorAccess.objects.filter(test_id=test_id, evaluator_id=evaluator_id).first()
        if not access:
            return Response({"error": "El evaluador no tiene acceso a esta prueba de diseño."}, status=status.HTTP_403_FORBIDDEN)

        if access.acceso_bloqueado:
            return Response({"error": "El acceso ya está bloqueado. No puedes enviar más respuestas."}, status=status.HTTP_403_FORBIDDEN)

        # Procesar las respuestas finales del evaluador
        responses_data = request.data.get('responses', [])
        for response_data in responses_data:
            question_id = response_data.get('question_id')
            heuristics = response_data.get('heuristics', [])

            if not question_id or not heuristics:
                return Response({"error": "Faltan datos: se requiere 'question_id' y 'heuristics'."}, status=status.HTTP_400_BAD_REQUEST)

            # Procesar cada heurística y sus subprincipios
            for heuristic_data in heuristics:
                heuristic_code = heuristic_data.get('heuristic_code')
                comment = heuristic_data.get('comment', '')  # Asegurarse de que el comentario se guarde a nivel de heurística
                subprinciples = heuristic_data.get('subprinciples', [])

                if not heuristic_code or not subprinciples:
                    return Response({"error": "Faltan datos: se requiere 'heuristic_code' y 'subprinciples'."}, status=status.HTTP_400_BAD_REQUEST)

                # Procesar cada subprincipio
                for subprinciple_data in subprinciples:
                    subprinciple_code = subprinciple_data.get('subprinciple_code')
                    response_value = subprinciple_data.get('response_value')

                    if not subprinciple_code or response_value is None:
                        return Response({"error": "Faltan datos: se requiere 'subprinciple_code' y 'response_value'."}, status=status.HTTP_400_BAD_REQUEST)

                    # Obtener el subprincipio asociado
                    try:
                        subprinciple = Subprinciple.objects.get(code=subprinciple_code)
                    except Subprinciple.DoesNotExist:
                        return Response({"error": f"No se encontró el subprincipio con código {subprinciple_code}."}, status=status.HTTP_404_NOT_FOUND)

                    # Guardar o actualizar la respuesta del subprincipio, marcándola como completa
                    EvaluatorHeuristicResponse.objects.update_or_create(
                        evaluator_id=evaluator_id,
                        test_id=test_id,
                        question_id=question_id,
                        subprinciple=subprinciple,
                        defaults={
                            'score': response_value,
                            'comment': comment,  # Guardar el comentario a nivel de heurística aquí
                            'is_complete': True,
                            'evaluator_access': access
                        }
                    )

        # Bloquear el acceso al evaluador después de finalizar las respuestas
        access.acceso_bloqueado = True
        access.save()

        return Response({"message": "Respuestas finalizadas y acceso bloqueado."}, status=status.HTTP_200_OK)

    # Asegurarnos de que siempre devolvemos una respuesta válida
    return Response({"error": "Método no permitido."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
