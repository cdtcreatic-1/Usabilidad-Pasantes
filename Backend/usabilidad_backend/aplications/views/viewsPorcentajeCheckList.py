from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from aplications.models import  PorcentajeCheckList
from aplications.serializers import PorcentajeCheckListSerializer

@api_view(['GET','POST'])
def API_PorcentajeCheckList(request):
    if request.metshod =='GET':
        Datos_PorcentajeCheckList=PorcentajeCheckList.objects.all() # select * from HeuristicCheckList
        serializer_PorcentajeCheckList=PorcentajeCheckListSerializer(Datos_PorcentajeCheckList,many=True)
        return JsonResponse(serializer_PorcentajeCheckList.data,safe=False)
    else:
        data_PorcentajeCheckList=JSONParser().parse(request)
        serializer_PorcentajeCheckList=PorcentajeCheckListSerializer(data=data_PorcentajeCheckList)
        if serializer_PorcentajeCheckList.is_valid():
           serializer_PorcentajeCheckList.save()
           return JsonResponse(serializer_PorcentajeCheckList.data,status=status.HTTP_201_CREATED)
        return JsonResponse(serializer_PorcentajeCheckList.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT'])
def API_PorcentajeCheckList_Details(request,pk):
    try:
        Dato_PorcentajeCheckList=PorcentajeCheckList.objects.get(id=pk) # select * from HeuristicCheckList where codigo=pk
    except PorcentajeCheckList.DoesNotExist:# ERROR 1 no es Dato_HeuristicCheckList sino HeuristicCheckList
        return  Response(status=status.HTTP_404_NOT_FOUND)  

    if request.method=='GET':
        serializer_PorcentajeCheckList = PorcentajeCheckListSerializer(Dato_PorcentajeCheckList)
        return JsonResponse(serializer_PorcentajeCheckList.data,safe=False)
    elif request.method=='PUT':
        data=JSONParser().parse(request)
        serializer_PorcentajeCheckList=PorcentajeCheckListSerializer(Dato_PorcentajeCheckList,data=data)
        if serializer_PorcentajeCheckList.is_valid():
            serializer_PorcentajeCheckList.save()
            return JsonResponse(serializer_PorcentajeCheckList.data,status=status.HTTP_202_ACCEPTED)
        return JsonResponse(serializer_PorcentajeCheckList.errors,status=status.HTTP_400_BAD_REQUEST)

