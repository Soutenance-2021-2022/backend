from django.shortcuts import render
from rest_framework import viewsets
from transcript.models import Amphi, Etudiant, Evaluation, Transcript
from transcript.serializers import AmphiSerializer, EtudiantSerializer, EvaluationSerializer, TranscriptSerializer

# Create your views here.
class EtudiantViewSet(viewsets.ModelViewSet):
    queryset = Etudiant.objects.all()
    serializer_class = EtudiantSerializer
    
class AmphiViewSet(viewsets.ModelViewSet):
    queryset = Amphi.objects.all()
    serializer_class = AmphiSerializer
    
class TranscriptViewSet(viewsets.ModelViewSet):
    queryset = Transcript.objects.all()
    serializer_class = TranscriptSerializer
    
class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    