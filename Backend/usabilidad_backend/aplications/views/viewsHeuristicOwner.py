from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from aplications.models import HeuristicOwner
from aplications.serializers import HeuristicOwnerSerializer

@api_view(['GET','POST'])
def API_HeuristicOwner(request):
    if request.method =='GET':
        Datos_HeuristicOwner=HeuristicOwner.objects.all() # select * from HeuristicCheckList
        serializer_HeuristicOwner=HeuristicOwnerSerializer(Datos_HeuristicOwner,many=True)
        return JsonResponse(serializer_HeuristicOwner.data,safe=False)
    else:
        data_HeuristicOwner=JSONParser().parse(request)
        serializer_HeuristicOwner=HeuristicOwnerSerializer(data=data_HeuristicOwner)
        if serializer_HeuristicOwner.is_valid():
           serializer_HeuristicOwner.save()
           return JsonResponse(serializer_HeuristicOwner.data,status=status.HTTP_201_CREATED)
        return JsonResponse(serializer_HeuristicOwner.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT'])
def API_HeuristicOwner_Details(request,pk):
    try:
        Dato_HeuristicOwner=HeuristicOwner.objects.get(id=pk) # select * from HeuristicCheckList where codigo=pk
    except HeuristicOwner.DoesNotExist:# ERROR 1 no es Dato_HeuristicCheckList sino HeuristicCheckList
        return  Response(status=status.HTTP_404_NOT_FOUND)  

    if request.method=='GET':
        serializer_HeuristicOwner = HeuristicOwner(HeuristicOwner)
        return JsonResponse(serializer_HeuristicOwner.data,safe=False)
    elif request.method=='PUT':
        data=JSONParser().parse(request)
        serializer_HeuristicOwner=HeuristicOwnerSerializer(Dato_HeuristicOwner,data=data)
        if serializer_HeuristicOwner.is_valid():
            serializer_HeuristicOwner.save()
            return JsonResponse(serializer_HeuristicOwner.data,status=status.HTTP_202_ACCEPTED)
        return JsonResponse(serializer_HeuristicOwner.errors,status=status.HTTP_400_BAD_REQUEST)
