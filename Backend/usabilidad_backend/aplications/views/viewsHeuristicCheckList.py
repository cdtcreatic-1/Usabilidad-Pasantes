from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from aplications.models import HeuristicCheckList
from aplications.serializers import HeuristicCheckListSerializer

@api_view(['GET','POST'])
def API_HeuristicCheckList(request):
    if request.method =='GET':
        Datos_HeuristicCheckLists=HeuristicCheckList.objects.all() # select * from HeuristicCheckList
        serializer_HeuristicCheckList=HeuristicCheckListSerializer(Datos_HeuristicCheckLists,many=True)
        return JsonResponse(serializer_HeuristicCheckList.data,safe=False)
    else:
        data_HeuristicCheckList=JSONParser().parse(request)
        serializer_HeuristicCheckList=HeuristicCheckListSerializer(data=data_HeuristicCheckList)
        if serializer_HeuristicCheckList.is_valid():
           serializer_HeuristicCheckList.save()
           return JsonResponse(serializer_HeuristicCheckList.data,status=status.HTTP_201_CREATED)
        return JsonResponse(serializer_HeuristicCheckList.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT'])
def API_HeuristicCheckList_Details(request,pk):
    try:
        Dato_HeuristicCheckList=HeuristicCheckList.objects.get(id=pk) # select * from HeuristicCheckList where codigo=pk
    except HeuristicCheckList.DoesNotExist:# ERROR 1 no es Dato_HeuristicCheckList sino HeuristicCheckList
        return  Response(status=status.HTTP_404_NOT_FOUND)  

    if request.method=='GET':
        serializer_HeuristicCheckList = HeuristicCheckListSerializer(Dato_HeuristicCheckList)
        return JsonResponse(serializer_HeuristicCheckList.data,safe=False)
    elif request.method=='PUT':
        data=JSONParser().parse(request)
        serializer_HeuristicCheckList=HeuristicCheckListSerializer(Dato_HeuristicCheckList,data=data)
        if serializer_HeuristicCheckList.is_valid():
            serializer_HeuristicCheckList.save()
            return JsonResponse(serializer_HeuristicCheckList.data,status=status.HTTP_202_ACCEPTED)
        return JsonResponse(serializer_HeuristicCheckList.errors,status=status.HTTP_400_BAD_REQUEST)

