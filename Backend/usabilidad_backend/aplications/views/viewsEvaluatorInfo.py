from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from aplications.models import  EvaluatorInfo
from aplications.serializers import EvaluatorInfoSerializer

@api_view(['GET','POST'])
def API_EvaluatorInfo(request):
    if request.metshod =='GET':
        Datos_EvaluatorInfo=EvaluatorInfo.objects.all() # select * from HeuristicCheckList
        serializer_EvaluatorInfo=EvaluatorInfoSerializer(Datos_EvaluatorInfo,many=True)
        return JsonResponse(serializer_EvaluatorInfo.data,safe=False)
    else:
        data_EvaluatorInfo=JSONParser().parse(request)
        serializer_EvaluatorInfot=EvaluatorInfoSerializer(data=data_EvaluatorInfo)
        if serializer_EvaluatorInfo.is_valid():
           serializer_EvaluatorInfo.save()
           return JsonResponse(serializer_EvaluatorInfo.data,status=status.HTTP_201_CREATED)
        return JsonResponse(serializer_EvaluatorInfo.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT'])
def API_EvaluatorInfo_Details(request,pk):
    try:
        Dato_EvaluatorInfo=EvaluatorInfo.objects.get(id=pk) # select * from HeuristicCheckList where codigo=pk
    except EvaluatorInfo.DoesNotExist:# ERROR 1 no es Dato_HeuristicCheckList sino HeuristicCheckList
        return  Response(status=status.HTTP_404_NOT_FOUND)  

    if request.method=='GET':
        serializer_EvaluatorInfo = EvaluatorInfoSerializer(Dato_EvaluatorInfo)
        return JsonResponse(serializer_EvaluatorInfo.data,safe=False)
    elif request.method=='PUT':
        data=JSONParser().parse(request)
        serializer_EvaluatorInfo=EvaluatorInfoSerializer(Dato_EvaluatorInfo,data=data)
        if serializer_EvaluatorInfo.is_valid():
            serializer_EvaluatorInfo.save()
            return JsonResponse(serializer_EvaluatorInfo.data,status=status.HTTP_202_ACCEPTED)
        return JsonResponse(serializer_EvaluatorInfo.errors,status=status.HTTP_400_BAD_REQUEST)

