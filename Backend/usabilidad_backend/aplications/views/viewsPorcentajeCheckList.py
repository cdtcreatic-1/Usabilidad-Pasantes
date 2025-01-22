from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from aplications.models import PorcentajeCheckList
from aplications.serializers import PorcentajeCheckListSerializer

@api_view(['GET', 'POST'])
def API_PorcentajeCheckList(request):
    if request.method == 'GET':
        # Obtiene todos los datos de PorcentajeCheckList
        datos_porcentaje_checklist = PorcentajeCheckList.objects.all()
        serializer = PorcentajeCheckListSerializer(datos_porcentaje_checklist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # Procesa los datos enviados en la solicitud
        serializer = PorcentajeCheckListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
def API_PorcentajeCheckList_Details(request, pk):
    # Obtiene el objeto o devuelve 404 si no existe
    dato_porcentaje_checklist = get_object_or_404(PorcentajeCheckList, id=pk)

    if request.method == 'GET':
        serializer = PorcentajeCheckListSerializer(dato_porcentaje_checklist)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        # Actualiza los datos del objeto
        serializer = PorcentajeCheckListSerializer(dato_porcentaje_checklist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
