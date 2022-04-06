from re import search
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from transcript.models import Amphi, Etudiant, Evaluation, SchoolAt, Transcript
from transcript.serializers import AmphiSerializer, EtudiantSerializer, EvaluationSerializer, SchoolAtSerializer, TranscriptSerializer

# Create your views here.
class EtudiantViewSet(viewsets.ModelViewSet):
    queryset = Etudiant.objects.all()
    serializer_class = EtudiantSerializer
    
class AmphiViewSet(viewsets.ModelViewSet):
    queryset = Amphi.objects.all()
    serializer_class = AmphiSerializer
    
class TranscriptViewSet(viewsets.ViewSet):
    
    
    def list(self, request):
        
        serializer = TranscriptSerializer(Transcript.objects.all(), many=True)
        response = serializer.data
        transcripts = Transcript.objects.all()
        custom_response =[]
        
        for item in response:
            
            evaluations = Evaluation.objects.filter(etudiant=item['etudiant']['id'])
            eval_serialize = EvaluationSerializer(evaluations, many=True)
            item['evaluations'] = eval_serialize.data
            custom_response.append(item)
        
        return Response({
            'data': custom_response
        })
    
class EvaluationViewSet(viewsets.ModelViewSet):
   
    def list(self, request):
        serializer = EvaluationSerializer(Evaluation.objects.all(), many=True)
        return Response({
            'data': serializer.data
        })
class SchooAtViewSet(viewsets.ModelViewSet):
       
    def retrieve(self, request, pk=None):
        
        school = SchoolAt.objects.filter(etudiant=pk)
        if(len(school) > 0):
            school_at = school[0]
            school_at_serializer = SchoolAtSerializer(school_at)
            return Response({
            'data': school_at_serializer.data
        })
        
       