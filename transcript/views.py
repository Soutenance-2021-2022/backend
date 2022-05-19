from re import search
from django.shortcuts import render
from rest_framework import viewsets,generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from transcript.models import Amphi, Etudiant, Evaluation, SchoolAt, Transcript, Ue
from transcript.serializers import AmphiSerializer, EtudiantSerializer, EvaluationSerializer, SchoolAtSerializer, TranscriptNormalSerializer, TranscriptSerializer, UeSerializer
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
            
            
class AddNoteAtViewSet(viewsets.ModelViewSet):
    
    def create(self, request):
        elements = request.data
        for item in elements['data']:
           etudiant = Etudiant.objects.filter(matricule=item['matricule'])
           if(len(etudiant) > 0):
                Evaluation.objects.create(
                    etudiant=etudiant[0], 
                    ue=Ue.objects.get(id=elements['ue']), 
                    note=item['note'],
                    examen=elements['examen']
                    )
               
        
        return Response({
            'data': {}
        }, status=status.HTTP_201_CREATED)
class StudentSchoolATViewSet(viewsets.ModelViewSet):
       
    def retrieve(self, request, pk=None):    
            
        school_at = SchoolAt.objects.filter(amphi=pk)
        custom_response =[]
        
        for item in school_at:
            custom_response.append(Etudiant.objects.get(id=item.etudiant.id))
            
        
        response_d = EtudiantSerializer(custom_response, many=True)
        
        return Response({
           'data': response_d.data
        })
class UeAmphiViewSet(viewsets.ModelViewSet):
    
    def retrieve(self, request, pk=None):
            
        ue_amphi = Ue.objects.filter(amphi=pk)
        response_d = UeSerializer(ue_amphi, many=True)
            
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

class StudentEvaluationViewSet(viewsets.ModelViewSet):
     def retrieve(self, request, pk=None):    
        evaluation = Evaluation.objects.filter(etudiant=pk)
        response_d = EvaluationSerializer(evaluation, many=True)
        
        return Response({
           'data': response_d.data
        })
class OperationTranscriptViewSet(viewsets.ModelViewSet):
    
   
    
    def determined_intermediare_note(self,notes):
        total =0
        for item in notes:
            if(item['ue']['has_tp'] == True):
                if(item['examen'] == "CC"):
                    total+=float(item['note'])
                if(item['examen'] == "SN"):
                    total+=float(item['note'])*2
                if(item['examen'] == "TP"):
                    total+=float(item['note'])*2
            else:
                if(item['examen'] == "CC"):
                    total+=float(item['note'])*1.5
                if(item['examen'] == "SN"):
                    total+=float(item['note'])*3.5
        return total
    
  
    def get_letter_grade(self,notefinale) :
        decision={
            "grade":'',
            "mgp":0.0
        }
        if 80<= notefinale and notefinale  <= 100:
            decision['grade'] = 'A'
            decision['mgp'] = 4.00
        elif 75 <= notefinale and notefinale <= 79:
            decision['grade'] = 'A-'
            decision['mgp'] = 3.70
        elif 70 <= notefinale and notefinale <= 74:
            decision['grade'] = 'B+'
            decision['mgp'] = 3.30
        elif 65 <= notefinale and notefinale <= 69:
            decision['grade'] = 'B'
            decision['mgp'] = 3.00
        elif 60 <= notefinale and notefinale <= 64:
            decision['grade'] = 'B-'
            decision['mgp'] = 2.70
        elif 55 <= notefinale and notefinale <= 59:
            decision['grade'] = 'C+'
            decision['mgp'] = 2.30
        elif 50 <= notefinale and notefinale <= 54:
            decision['grade'] = 'C'
            decision['mgp'] = 2.00
        elif 45 <= notefinale and notefinale<= 49:
            decision['grade'] = 'C-'
            decision['mgp'] = 1.70
        elif 40 <= notefinale and notefinale<= 44:
            decision['grade'] = 'D+'
            decision['mgp'] = 1.30
        elif 35 <= notefinale and notefinale <= 39:
            decision['grade'] = 'D'
            decision['mgp'] = 1.00
        elif 30 <= notefinale and notefinale <= 34:
            decision['grade'] = 'E'
            decision['mgp'] = 0.00
        else:
            decision['grade'] = 'F'
            decision['mgp'] = 0.00
        return decision
   
    def retrieve(self, request, pk=None):    
        evaluation = Evaluation.objects.filter(etudiant=pk)
        etudiant = Etudiant.objects.filter(id=pk)
        allEvaluation = EvaluationSerializer(evaluation, many=True)
        id_used =[]
        notes_classed=[]
        for item in allEvaluation.data:
            if item['ue']['id'] not in id_used:
                note = Evaluation.objects.filter(etudiant=pk).filter(ue=item['ue']['id'])
                note_serializers = EvaluationSerializer(note, many=True)
                notes = note_serializers.data
                note_ee = self.determined_intermediare_note(notes)
                print(note_ee)
                print(self.get_letter_grade(note_ee))
                id_used.append(item['ue']['id'])
        
        return Response({
           'data': notes_classed
        })
