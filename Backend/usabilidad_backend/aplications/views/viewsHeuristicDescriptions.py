from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from aplications.models import HeuristicDescriptions
from aplications.serializers import HeuristicDescriptionsSerializer

@api_view(['GET','POST'])
def API_HeuristicDescriptions(request):
    if request.metshod =='GET':
        Datos_HeuristicDescriptions=HeuristicDescriptions.objects.all() # select * from HeuristicCheckList
        serializer_HeuristicDescriptions=HeuristicDescriptionsSerializer(Datos_HeuristicDescriptions,many=True)
        return JsonResponse(serializer_HeuristicDescriptions.data,safe=False)
    else:
        data_HeuristicDescriptions=JSONParser().parse(request)
        serializer_HeuristicDescriptions=HeuristicDescriptionsSerializer(data=data_HeuristicDescriptions)
        if serializer_HeuristicDescriptions.is_valid():
           serializer_HeuristicDescriptions.save()
           return JsonResponse(serializer_HeuristicDescriptions.data,status=status.HTTP_201_CREATED)
        return JsonResponse(serializer_HeuristicDescriptions.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT'])
def API_HeuristicDescriptions_Details(request,pk):
    try:
        Dato_HeuristicDescriptions=HeuristicDescriptions.objects.get(id=pk) # select * from HeuristicCheckList where codigo=pk
    except HeuristicDescriptions.DoesNotExist:# ERROR 1 no es Dato_HeuristicCheckList sino HeuristicCheckList
        return  Response(status=status.HTTP_404_NOT_FOUND)  

    if request.method=='GET':
        serializer_HeuristicDescriptions = HeuristicDescriptionsSerializer(Dato_HeuristicDescriptions)
        return JsonResponse(serializer_HeuristicDescriptions.data,safe=False)
    elif request.method=='PUT':
        data=JSONParser().parse(request)
        serializer_HeuristicDescriptions=HeuristicDescriptionsSerializer(Dato_HeuristicDescriptions,data=data)
        if serializer_HeuristicDescriptions.is_valid():
            serializer_HeuristicDescriptions.save()
            return JsonResponse(serializer_HeuristicDescriptions.data,status=status.HTTP_202_ACCEPTED)
        return JsonResponse(serializer_HeuristicDescriptions.errors,status=status.HTTP_400_BAD_REQUEST)

