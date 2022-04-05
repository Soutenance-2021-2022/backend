
from dataclasses import field, fields
from rest_framework import serializers

from transcript.models import Amphi, Etudiant, Evaluation, Exam, Participate, Transcript

class EtudiantSerializer(serializers.ModelSerializer):
    # tracks = TrackSerializer(many=True, read_only=True)
    class Meta:
        model = Etudiant
        fields = ('id','name','surname','transcripts')

class AmphiSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Amphi
        fields = '__all__'

# class EtudiantRelatedField(serializers.RelatedField):
#     def to_representation(self, instance):
#         return EtudiantSerializer(instance).data
#     def to_internal_value(self, data):
#         return self.queryset.get(pk=data)
class TranscriptSerializer(serializers.ModelSerializer):
    
    # category_name = serializers.RelatedField(source='category', read_only=True)
    class Meta:
        model = Transcript
        fields = '__all__'
class EvaluationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Evaluation
        fields = '__all__'