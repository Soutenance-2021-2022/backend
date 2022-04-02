
from dataclasses import field
from rest_framework import serializers

from transcript.models import Etudiant

class EtudiantSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Etudiant
        fields = '__all__'