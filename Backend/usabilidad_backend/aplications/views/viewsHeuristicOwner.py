from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from aplications.models import HeuristicOwner
from aplications.serializers import HeuristicOwnerSerializer

# Vista para obtener o crear HeuristicOwner
@api_view(['GET', 'POST'])
def API_HeuristicOwner(request):
    if request.method == 'GET':
        # Obtener todos los HeuristicOwner
        Datos_HeuristicOwner = HeuristicOwner.objects.all() 
        # Serializar los datos
        serializer_HeuristicOwner = HeuristicOwnerSerializer(Datos_HeuristicOwner, many=True)
        # Retornar los datos serializados
        return Response(serializer_HeuristicOwner.data)

    elif request.method == 'POST':
        # Parsear los datos recibidos
        data_HeuristicOwner = JSONParser().parse(request)
        # Serializar los datos
        serializer_HeuristicOwner = HeuristicOwnerSerializer(data=data_HeuristicOwner)
        
        if serializer_HeuristicOwner.is_valid():
            # Guardar el nuevo HeuristicOwner
            serializer_HeuristicOwner.save()
            # Retornar los datos del objeto recién creado
            return Response(serializer_HeuristicOwner.data, status=status.HTTP_201_CREATED)
        
        # Si los datos no son válidos, retornar los errores
        return Response(serializer_HeuristicOwner.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista para obtener o actualizar un HeuristicOwner por ID
@api_view(['GET', 'PUT'])
def API_HeuristicOwner_Details(request, pk):
    try:
        # Intentar obtener el HeuristicOwner por su ID
        Dato_HeuristicOwner = HeuristicOwner.objects.get(id=pk)
    except HeuristicOwner.DoesNotExist:
        # Si no existe, retornar 404 Not Found
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Si el método es GET, serializar y devolver los datos
        serializer_HeuristicOwner = HeuristicOwnerSerializer(Dato_HeuristicOwner)
        return Response(serializer_HeuristicOwner.data)

    elif request.method == 'PUT':
        # Si el método es PUT, actualizar los datos
        data = JSONParser().parse(request)
        serializer_HeuristicOwner = HeuristicOwnerSerializer(Dato_HeuristicOwner, data=data)
        
        if serializer_HeuristicOwner.is_valid():
            # Guardar los datos actualizados
            serializer_HeuristicOwner.save()
            return Response(serializer_HeuristicOwner.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer_HeuristicOwner.errors, status=status.HTTP_400_BAD_REQUEST)
