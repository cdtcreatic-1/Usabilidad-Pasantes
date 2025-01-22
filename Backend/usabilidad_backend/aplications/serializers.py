from rest_framework import serializers
from aplications.models import *

class HeuristicCheckListSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeuristicCheckList
        fields ='__all__'
        
class HeuristicOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeuristicOwner
        fields ='__all__'

class HeuristicEvaluationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeuristicEvaluations
        fields ='__all__'

class HeuristicDescriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeuristicDescriptions
        fields ='__all__'

class PorcentajeCheckListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PorcentajeCheckList
        fields ='__all__'

class EvaluatorInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluatorInfo
        fields ='__all__'

class HeuristicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Heuristics
        fields ='__all__'




class ObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observation
        fields = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10']

class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ['name', 'description', 'hi', 'incidents', 'severity', 'frequency', 'criticism']
        
class CheckListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckList
        fields = '__all__'

class DescriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Descriptions
        fields = ['name', 'description']

#/////////////////////////////////////////////////////////////////

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Especifica el modelo User
        fields = '__all__'  # Incluir todos los campos del modelo User


class SubprincipleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subprinciple  # Especifica el modelo Subprinciple
        fields = ['code', 'subtitle', 'description', 'example']  # Campos específicos a incluir


class HeuristicSerializer(serializers.ModelSerializer):
    subprinciples = SubprincipleSerializer(many=True, read_only=True)  # Incluye los subprincipios asociados, solo lectura

    class Meta:
        model = Heuristic
        fields = ['code', 'title', 'description', 'subprinciples']


class ScreenshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screenshot
        fields = ['__all__']

#////////////////////////////////////////////////////////////////////////////

class DesignTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignTest
        fields ='__all__'


class DesignQuestionSerializer(serializers.ModelSerializer):
    heuristics = serializers.SlugRelatedField(
        many=True,
        slug_field='code',  # Usar el campo 'code' de la heurística en lugar de 'id'
        queryset=Heuristic.objects.all()  # Establece el conjunto de heurísticas disponibles
    )

    class Meta:
        model = DesignQuestion
        fields = '__all__'


class EvaluatorAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluatorAccess
        fields = '__all__'          


class EvaluatorStandardResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluatorStandardResponse
        fields ='__all__'


class EvaluatorHeuristicResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluatorHeuristicResponse
        fields ='__all__'