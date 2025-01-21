from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from aplications.models import Heuristics
from aplications.serializers import HeuristicsSerializer

@api_view(['GET', 'POST'])
def API_Heuristics(request):
    if request.method == 'GET':
        try:
            
            Datos_Heuristics = Heuristics.objects.all()
            serializer_Heuristics = HeuristicsSerializer(Datos_Heuristics, many=True)
            return Response(serializer_Heuristics.data)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        data_Heuristics = request.data
        serializer_Heuristics = HeuristicsSerializer(data=data_Heuristics)
        if serializer_Heuristics.is_valid():
            serializer_Heuristics.save()
            return Response(serializer_Heuristics.data, status=status.HTTP_201_CREATED)
        return Response(serializer_Heuristics.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
def API_Heuristics_Details(request, pk):
    try:
        Dato_Heuristics = Heuristics.objects.get(id=pk)
    except Heuristics.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer_Heuristics = HeuristicsSerializer(Dato_Heuristics)
        return Response(serializer_Heuristics.data)
    elif request.method == 'PUT':
        data = request.data
        serializer_Heuristics = HeuristicsSerializer(Dato_Heuristics, data=data)
        if serializer_Heuristics.is_valid():
            serializer_Heuristics.save()
            return Response(serializer_Heuristics.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer_Heuristics.errors, status=status.HTTP_400_BAD_REQUEST)


# Nueva función para obtener Heuristics por owner_id
@api_view(['GET'])
def API_Heuristics_By_Owner(request, owner_id):
    try:
        heuristics = Heuristics.objects.filter(owner_id=owner_id)  # Filtrar por owner_id
    except Heuristics.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = HeuristicsSerializer(heuristics, many=True)
    return Response(serializer.data)
