from re import search
from django.shortcuts import render
from rest_framework import viewsets,generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from transcript.models import Amphi, Etudiant, Evaluation, SchoolAt, Transcript
from transcript.serializers import AmphiSerializer, EtudiantSerializer, EvaluationSerializer, SchoolAtSerializer, TranscriptNormalSerializer, TranscriptSerializer
from django.db.models import Q

from rest_framework import status

# Create your views here.
class EtudiantViewSet(viewsets.ModelViewSet):
    queryset = Etudiant.objects.all()
    serializer_class = EtudiantSerializer
    
    def list(self, request):
        serializer = EtudiantSerializer(Etudiant.objects.all(), many=True)
        return Response({
            'data': serializer.data
        })

    def retrieve(self, request, pk=None):
        surveillant = Etudiant.objects.get(id=pk)
        serializer = EtudiantSerializer(surveillant)
        return Response({
            'data': serializer.data
        })

    def create(self, request):
        serializer = EtudiantSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        etudiant = Etudiant.objects.get(id=pk)
        serializer = EtudiantSerializer(instance=etudiant, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'data': serializer.data}, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        etudiant = Etudiant.objects.get(id=pk)
        etudiant.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

        
    
class AmphiViewSet(viewsets.ModelViewSet):
    queryset = Amphi.objects.all()
    serializer_class = AmphiSerializer
    
    
    def get(self, request):
        serializer = AmphiSerializer(Amphi.objects.all(), many=True)
        return Response({
            "data": serializer.data
        })

class TranscriptApiViewSet(generics.ListCreateAPIView):
    queryset = Transcript.objects.all()
    search_fields = ['=number']
    serializer_class = TranscriptNormalSerializer
    
         
class TranscriptViewSet(viewsets.ViewSet):
    permissions_classes = [IsAuthenticated]
    
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
    
    def list(self, request):
        serializer = SchoolAtSerializer(SchoolAt.objects.all(), many=True)
        return Response({
            'data': serializer.data
        })
        
    def create(self, request):
        serializer = SchoolAtSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
       
    def retrieve(self, request, pk=None):
        
        school = SchoolAt.objects.filter(etudiant=pk)
        if(len(school) > 0):
            school_at = school[0]
            school_at_serializer = SchoolAtSerializer(school_at)
            return Response({
            'data': school_at_serializer.data
        })
            
class StudentSchoolATViewSet(viewsets.ModelViewSet):
       
    def retrieve(self, request, pk=None):    
            
        school_at = SchoolAt.objects.filter(amphi=pk)
        amphi = []
    
        custom_response =[]
        
        for item in school_at:
            custom_response.append(Etudiant.objects.get(id=item.etudiant.id))
            
        
        response_d = EtudiantSerializer(custom_response, many=True)
        
        return Response({
           'data': response_d.data
        })

class SearchTranscriptView(viewsets.ModelViewSet):
    
    def retrieve(self, request,pk=None):
        
        transcript = Transcript.objects.filter(id=pk)
    
        
        find_tran_serializer = TranscriptSerializer(transcript, many=True)
        response = find_tran_serializer.data
        custom_response =[]
        
        for item in response:
            
            evaluations = Evaluation.objects.filter(etudiant=item['etudiant']['id'])
            eval_serialize = EvaluationSerializer(evaluations, many=True)
            item['evaluations'] = eval_serialize.data
            custom_response.append(item)
        
        return Response({
            'data': custom_response
        })

        
        
        
       