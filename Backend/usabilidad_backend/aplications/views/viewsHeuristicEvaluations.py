from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from aplications.models import HeuristicEvaluations
from aplications.serializers import HeuristicEvaluationsSerializer

@api_view(['GET','POST'])
def API_HeuristicEvaluations(request):
    if request.method =='GET':
        Datos_HeuristicOwner=HeuristicEvaluations.objects.all() # select * from HeuristicCheckList
        serializer_HeuristicEvaluations=HeuristicEvaluationsSerializer(Datos_HeuristicOwner,many=True)
        return JsonResponse(serializer_HeuristicEvaluations.data,safe=False)
    else:
        data_HeuristicEvaluations=JSONParser().parse(request)
        serializer_HeuristicEvaluations=HeuristicEvaluationsSerializer(data=data_HeuristicEvaluations)
        if serializer_HeuristicEvaluations.is_valid():
           serializer_HeuristicEvaluations.save()
           return JsonResponse(serializer_HeuristicEvaluations.data,status=status.HTTP_201_CREATED)
        return JsonResponse(serializer_HeuristicEvaluations.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT'])
def API_HeuristicEvaluations_Details(request,pk):
    try:
        Dato_HeuristicEvaluations=HeuristicEvaluations.objects.get(id=pk) # select * from HeuristicCheckList where codigo=pk
    except HeuristicEvaluations.DoesNotExist:# ERROR 1 no es Dato_HeuristicCheckList sino HeuristicCheckList
        return  Response(status=status.HTTP_404_NOT_FOUND)  

    if request.method=='GET':
        serializer_HeuristicEvaluations = HeuristicEvaluations(HeuristicEvaluations)
        return JsonResponse(serializer_HeuristicEvaluations.data,safe=False)
    elif request.method=='PUT':
        data=JSONParser().parse(request)
        serializer_HeuristicEvaluations=HeuristicEvaluationsSerializer(Dato_HeuristicEvaluations,data=data)
        if serializer_HeuristicEvaluations.is_valid():
            serializer_HeuristicEvaluations.save()
            return JsonResponse(serializer_HeuristicEvaluations.data,status=status.HTTP_202_ACCEPTED)
        return JsonResponse(serializer_HeuristicEvaluations.errors,status=status.HTTP_400_BAD_REQUEST)
