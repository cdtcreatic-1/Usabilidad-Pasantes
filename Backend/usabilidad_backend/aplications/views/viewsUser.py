from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from aplications.models import User
from aplications.serializers import UserSerializer

# API para listar y crear usuarios
@api_view(['GET', 'POST'])
def API_User(request):
    if request.method == 'GET':
        Datos_Users = User.objects.all()  # Obtener todos los usuarios
        serializer_User = UserSerializer(Datos_Users, many=True)
        return JsonResponse(serializer_User.data, safe=False)
    elif request.method == 'POST':
        data_User = JSONParser().parse(request)
        serializer_User = UserSerializer(data=data_User)
        if serializer_User.is_valid():
            serializer_User.save()
            return JsonResponse(serializer_User.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer_User.errors, status=status.HTTP_400_BAD_REQUEST)

# API para obtener y actualizar un usuario por ID
@api_view(['GET', 'PUT'])
def API_User_Details(request, pk):
    try:
        Dato_User = User.objects.get(id=pk)  # Obtener usuario por ID
    except User.DoesNotExist:
        return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer_User = UserSerializer(Dato_User)
        return JsonResponse(serializer_User.data, safe=False)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer_User = UserSerializer(Dato_User, data=data)
        if serializer_User.is_valid():
            serializer_User.save()
            return JsonResponse(serializer_User.data, status=status.HTTP_202_ACCEPTED)
        return JsonResponse(serializer_User.errors, status=status.HTTP_400_BAD_REQUEST)

# API para registrar y actualizar usuarios por correo electrónico
@api_view(['GET', 'PUT'])
def API_User_Register(request, email):
    try:
        Dato_User = User.objects.get(mailUser=email)  # Obtener usuario por correo
    except User.DoesNotExist:
        return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer_User = UserSerializer(Dato_User)
        return JsonResponse(serializer_User.data, safe=False)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer_User = UserSerializer(Dato_User, data=data)
        if serializer_User.is_valid():
            serializer_User.save()
            return JsonResponse(serializer_User.data, status=status.HTTP_202_ACCEPTED)
        return JsonResponse(serializer_User.errors, status=status.HTTP_400_BAD_REQUEST)

# API para inicio de sesión
@api_view(['POST'])
def API_User_Login(request):
    # Parsear datos del cuerpo de la solicitud
    data_User = JSONParser().parse(request)
    print(data_User)

    try:
        # Obtener usuario por nombre de usuario y contraseña
        Dato_User = User.objects.get(username=data_User['username'], password=data_User['password'])
    except User.DoesNotExist:
        return JsonResponse({'error': 'Usuario o contraseña incorrectos.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        # Serializar datos del usuario encontrado
        serializer_User = UserSerializer(Dato_User)
        return JsonResponse(serializer_User.data, safe=False, status=status.HTTP_200_OK)
