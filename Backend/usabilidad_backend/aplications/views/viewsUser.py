from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from aplications.models import User
from aplications.serializers import UserSerializer

# Vista para obtener todos los usuarios o crear un nuevo usuario
@api_view(['GET', 'POST'])
def API_User(request):
    """
    GET: Devuelve una lista de todos los usuarios.
    POST: Crea un nuevo usuario en la base de datos.
    """
    if request.method == 'GET':
        # Obtener todos los usuarios
        Datos_Users = User.objects.all()
        serializer_User = UserSerializer(Datos_Users, many=True)
        return JsonResponse(serializer_User.data, safe=False)

    elif request.method == 'POST':
        # Crear un nuevo usuario
        data_User = JSONParser().parse(request)
        serializer_User = UserSerializer(data=data_User)
        if serializer_User.is_valid():
            serializer_User.save()
            return JsonResponse(serializer_User.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer_User.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista para obtener o actualizar un usuario por su ID
@api_view(['GET', 'PUT'])
def API_User_Details(request, pk):
    """
    GET: Obtiene los detalles de un usuario específico por su ID.
    PUT: Actualiza la información de un usuario específico por su ID.
    """
    try:
        # Buscar usuario por ID
        Dato_User = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Obtener datos del usuario
        serializer_User = UserSerializer(Dato_User)
        return JsonResponse(serializer_User.data, safe=False)

    elif request.method == 'PUT':
        # Actualizar datos del usuario
        data = JSONParser().parse(request)
        serializer_User = UserSerializer(Dato_User, data=data)
        if serializer_User.is_valid():
            serializer_User.save()
            return JsonResponse(serializer_User.data, status=status.HTTP_202_ACCEPTED)
        return JsonResponse(serializer_User.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista para obtener o actualizar un usuario por su email
@api_view(['GET', 'PUT'])
def API_User_Register(request, email):
    """
    GET: Obtiene los detalles de un usuario específico por su email.
    PUT: Actualiza la información de un usuario específico por su email.
    """
    try:
        # Buscar usuario por email
        Dato_User = User.objects.get(mailUser=email)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer_User = UserSerializer(Dato_User)
        return JsonResponse(serializer_User.data, safe=False)

    elif request.method == 'PUT':
        # Actualizar datos del usuario
        data = JSONParser().parse(request)
        serializer_User = UserSerializer(Dato_User, data=data)
        if serializer_User.is_valid():
            serializer_User.save()
            return JsonResponse(serializer_User.data, status=status.HTTP_202_ACCEPTED)
        return JsonResponse(serializer_User.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista para el inicio de sesión del usuario
@api_view(['POST'])
def API_User_Login(request):
    """
    POST: Autentica a un usuario verificando su nombre de usuario y contraseña.
    """
    data_User = JSONParser().parse(request)
    try:
        # Verificar si el usuario existe con el nombre de usuario y contraseña proporcionados
        Dato_User = User.objects.get(username=data_User['username'], password=data_User['password'])
    except User.DoesNotExist:
        return Response({'error': 'Usuario o contraseña incorrectos'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        # Retornar los datos del usuario autenticado
        serializer_User = UserSerializer(Dato_User)
        return JsonResponse(serializer_User.data, safe=False)
