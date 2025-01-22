from rest_framework.decorators import api_view
from rest_framework.response import Response
from aplications.models import Observation
from aplications.serializers import ObservationSerializer


@api_view (['GET'])
def API_Get_Observations(request, owner_id):
    try:
        # Obtener las observaciones asociadas al propietario
        observations = Observation.objects.filter(owner_id=owner_id)

        # Serializar las observaciones
        serializer_observations = ObservationSerializer(observations, many=True)

        # Retornar la respuesta con los datos serializados
        return Response(serializer_observations.data)
    except Exception as e:
        # Manejo de errores
        return Response({"detail": str(e)}, status=500)

