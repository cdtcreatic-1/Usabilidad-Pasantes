from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from aplications.models import Evaluation
from aplications.serializers import EvaluationSerializer


# Vista para obtener y crear evaluaciones por owner_id
@api_view(['GET', 'POST'])
def API_Evaluation(request, owner_id):
    if request.method == 'GET':
        try:
            evaluations = Evaluation.objects.filter(owner_id=owner_id)
            serializer_evaluations = EvaluationSerializer(evaluations, many=True)
            return Response(serializer_evaluations.data)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'POST':
        try:
            data = request.data
            for evaluation in data:
                evaluation['owner_id'] = owner_id  # Asegurar que el owner_id se asigne correctamente
                serializer = EvaluationSerializer(data=evaluation)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Guardado Correctamente"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Vista para manejar evaluaciones individuales
@api_view(['GET', 'PUT'])
def API_Evaluation_Details(request, pk):
    try:
        evaluation = Evaluation.objects.get(id=pk)
    except Evaluation.DoesNotExist:
        return Response({"detail": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer_evaluation = EvaluationSerializer(evaluation)
        return Response(serializer_evaluation.data)
    elif request.method == 'PUT':
        data = request.data
        serializer_evaluation = EvaluationSerializer(evaluation, data=data)
        if serializer_evaluation.is_valid():
            serializer_evaluation.save()
            return Response(serializer_evaluation.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer_evaluation.errors, status=status.HTTP_400_BAD_REQUEST)