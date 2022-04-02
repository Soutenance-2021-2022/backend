from django.shortcuts import render
from rest_framework import viewsets
from transcript.models import Etudiant
from transcript.serializers import EtudiantSerializer

# Create your views here.
class EtudiantViewSet(viewsets.ModelViewSet):
    queryset = Etudiant.objects.all()
    serializer_class = EtudiantSerializer