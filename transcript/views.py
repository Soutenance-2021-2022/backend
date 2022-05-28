from re import search
from sys import hash_info
from django.shortcuts import render
from rest_framework import viewsets,generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from transcript.models import AcademicYear, Amphi, Etudiant, Evaluation, SchoolAt, Transcript, Ue
from transcript.serializers import AmphiSerializer, EtudiantSerializer, EvaluationSerializer, SchoolAtSerializer, TranscriptNormalSerializer, TranscriptSerializer, UeSerializer
from django.db.models import Q

from rest_framework import status
import hashlib
import environ

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
        etudiant = Etudiant.objects.get(id=pk)
        serializer = EtudiantSerializer(etudiant)
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
    
    
    def generate_name_initial(self, name, surname):
        full_name = name+ ' '+surname
        full_name_split = full_name.split()
        name_size= len(full_name_split) -1
        i=0
        initial =''
        while(name_size >=i):
            initial+= full_name_split[i][0][:1]
            i+=1  
        return initial[:3]
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
            "mgp":0.0,
            "decision":''
        }
        if 80<= notefinale and notefinale  <= 100:
            decision['grade'] = 'A'
            decision['mgp'] = 4.00
            decision['decision'] = "CA"
        elif 75 <= notefinale and notefinale <= 79:
            decision['grade'] = 'A-'
            decision['mgp'] = 3.70
            decision['decision'] = "CA"
        elif 70 <= notefinale and notefinale <= 74:
            decision['grade'] = 'B+'
            decision['mgp'] = 3.30
            decision['decision'] = "CA"
        elif 65 <= notefinale and notefinale <= 69:
            decision['grade'] = 'B'
            decision['mgp'] = 3.00
            decision['decision'] = "CA"
        elif 60 <= notefinale and notefinale <= 64:
            decision['grade'] = 'B-'
            decision['mgp'] = 2.70
            decision['decision'] = "CA"
        elif 55 <= notefinale and notefinale <= 59:
            decision['grade'] = 'C+'
            decision['mgp'] = 2.30
            decision['decision'] = "CA"
        elif 50 <= notefinale and notefinale <= 54:
            decision['grade'] = 'C'
            decision['mgp'] = 2.00
            decision['decision'] = "CA"
        elif 45 <= notefinale and notefinale<= 49:
            decision['grade'] = 'C-'
            decision['mgp'] = 1.70
            decision['decision'] = "CANT"
        elif 40 <= notefinale and notefinale<= 44:
            decision['grade'] = 'D+'
            decision['mgp'] = 1.30
            decision['decision'] = "CANT"
        elif 35 <= notefinale and notefinale <= 39:
            decision['grade'] = 'D'
            decision['mgp'] = 1.00
            decision['decision'] = "CANT"
        elif 30 <= notefinale and notefinale <= 34:
            decision['grade'] = 'E'
            decision['mgp'] = 0.00
            decision['decision'] = "NC"
        else:
            decision['grade'] = 'F'
            decision['mgp'] = 0.00
            decision['decision'] = "NC"
        return decision
   
    def retrieve(self, request, pk=None):
            
        evaluation = Evaluation.objects.filter(etudiant=pk)
        allEvaluation = EvaluationSerializer(evaluation, many=True)
        
        etudiant = Etudiant.objects.get(id=pk)
        etudiant_serializer = EtudiantSerializer(etudiant)
        
        school_info = SchoolAt.objects.get(etudiant=pk)
        school_info_serializer = SchoolAtSerializer(school_info)
        
        nbre_transcript_print = Transcript.objects.all().count()
        
        ue_amphi = Ue.objects.filter(amphi=school_info.amphi)
        total_credit_amphi = UeSerializer(ue_amphi, many=True)
        credit_sum=0
        credit_capitalised_sum=0
         
        for cred in total_credit_amphi.data:
            credit_sum+=cred['credit']
        
        SECRET_kEY_HASH="AUTHENTIFICATION_NEW_SYSTEM_UY1"
        
        id_used =[]
        all_notes_credit=[]
        for item in allEvaluation.data:
            if item['ue']['id'] not in id_used:
                note = Evaluation.objects.filter(etudiant=pk).filter(ue=item['ue']['id'])
                note_serializers = EvaluationSerializer(note, many=True)
                notes = note_serializers.data
                note_ee = self.determined_intermediare_note(notes)
                decision = self.get_letter_grade(note_ee)
                
                Evaluation.objects.create(
                    etudiant=Etudiant.objects.get(id=pk),
                    note=note_ee,
                    examen='EE',
                    ue=Ue.objects.get(id=item['ue']['id']),
                    grade=decision['grade'],
                    decision=decision['decision'],
                )
                notes_credit={
                    "note":note_ee,
                    "credit":item['ue']['credit']
                }
                if(note_ee >= 35):
                    credit_capitalised_sum+=item['ue']['credit']
                    
                all_notes_credit.append(notes_credit)
                id_used.append(item['ue']['id'])
                
        note_with_credit =0.0
        for note in all_notes_credit:
            note_with_credit+= note['note']*note['credit']
            
        mgp = note_with_credit/credit_sum
        final_decision= 'ECHEC'
       
        if(mgp >= 2):
            final_decision ='ADMIS'
            
    #Generate number of transcript
        name_abrv=self.generate_name_initial(etudiant_serializer.data['name'],etudiant_serializer.data['surname'])
        abrev_faculty = school_info_serializer.data['amphi']['filiere']['faculty']['abrev']
        filiere = school_info_serializer.data['amphi']['filiere']['name'][:3]
        code_level = school_info_serializer.data['amphi']['level']['code']
        academic_year = school_info_serializer.data['amphi']['academic_year']
        inter = academic_year['name'].split('/')
        abrev_academic_year = inter[0]+inter[1][2:4]
    #end generate number of transcript
        
        mgp = round(mgp,2)
        msg = SECRET_kEY_HASH+etudiant_serializer.data['matricule'] +etudiant_serializer.data['name']+ etudiant_serializer.data['surname']+ str(mgp)+final_decision
        hash_info = hashlib.new('sha1')
        hash_info.update(msg.encode('utf-8'))
        public_hash = hash_info.hexdigest()
        
        transcript_number = str(nbre_transcript_print+1)+ '/' +name_abrv+'/'+code_level+'/'+abrev_faculty+'/'+filiere+'/'+abrev_academic_year
       
        Transcript.objects.create(
                    etudiant=Etudiant.objects.get(id=pk),
                    mgp=mgp,
                    hash=public_hash,
                    number=transcript_number,
                    complete_credit=credit_capitalised_sum,
                    decision=final_decision,
                    academic_year=AcademicYear.objects.get(id=school_info_serializer.data['amphi']['academic_year']['id']),
                )
        
        return Response({
           'data': ''
        },status=status.HTTP_201_CREATED)
