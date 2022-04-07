
from dataclasses import field, fields
from rest_framework import serializers

from transcript.models import AcademicYear, Amphi, Etudiant, Evaluation, Faculty, Filiere, Level, SchoolAt, Semester, Transcript, Ue

class AcademicSerializer(serializers.ModelSerializer):
    # tracks = TrackSerializer(many=True, read_only=True)
    class Meta:
        model = AcademicYear
        fields = '__all__'
        
class AcademicRelatedField(serializers.RelatedField):
    def to_representation(self, instance):
        return AcademicSerializer(instance).data
    
    def to_internal_value(self, data):
        return self.queryset.get(pk=data)
    
class SemesterSerializer(serializers.ModelSerializer):
    academic_year = AcademicRelatedField(queryset=AcademicYear.objects.all(), many=False)
    class Meta:
        model = Semester
        fields = '__all__'  
        
class SemesterRelatedField(serializers.RelatedField):
    def to_representation(self, instance):
        return SemesterSerializer(instance).data
    
    def to_internal_value(self, data):
        return self.queryset.get(pk=data)
      
class EtudiantSerializer(serializers.ModelSerializer):
    # tracks = TrackSerializer(many=True, read_only=True)
    class Meta:
        model = Etudiant
        fields = '__all__'
class EtudiantRelatedField(serializers.RelatedField):
    def to_representation(self, instance):
        return EtudiantSerializer(instance).data
    
    def to_internal_value(self, data):
        return self.queryset.get(pk=data)


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'
        
class FacultyRelatedField(serializers.RelatedField):
    def to_representation(self, instance):
        return FacultySerializer(instance).data
    
    def to_internal_value(self, data):
        return self.queryset.get(pk=data)
    
class FiliereSerializer(serializers.ModelSerializer):
    faculty = FacultyRelatedField(queryset=Faculty.objects.all(), many=False)
    class Meta:
        model = Filiere
        fields = '__all__'

class FiliereRelatedField(serializers.RelatedField):
    def to_representation(self, instance):
        return FiliereSerializer(instance).data
    
    def to_internal_value(self, data):
        return self.queryset.get(pk=data)
class LevelSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Level
        fields = '__all__'
class LevelRelatedField(serializers.RelatedField):
    def to_representation(self, instance):
        return LevelSerializer(instance).data
    
    def to_internal_value(self, data):
        return self.queryset.get(pk=data)
    
class AmphiSerializer(serializers.ModelSerializer):
    filiere = FiliereRelatedField(queryset=Filiere.objects.all())
    level = LevelRelatedField(queryset=Level.objects.all())
    class Meta:
        model = Amphi
        fields = '__all__'

class AmphiRelatedField(serializers.RelatedField):
    def to_representation(self, instance):
        return AmphiSerializer(instance).data
    
    def to_internal_value(self, data):
        return self.queryset.get(pk=data) 
   
class UeSerializer(serializers.ModelSerializer):
    semester = SemesterRelatedField(queryset=Semester.objects.all(), many=False)
    class Meta:
        model = Ue
        fields = '__all__'
        
class UeRelatedField(serializers.RelatedField):
    def to_representation(self, instance):
        return UeSerializer(instance).data
    
    def to_internal_value(self, data):
        return self.queryset.get(pk=data)

class TranscriptSerializer(serializers.ModelSerializer):
    etudiant = EtudiantRelatedField(queryset=Etudiant.objects.all(), many=False)
    academic_year = AcademicRelatedField(queryset=AcademicYear.objects.all(), many=False)
    class Meta:
        model = Transcript
        fields = [
            'number',
            'mgp',
            'complete_credit',
            'academic_year',
            'etudiant'
        ]
class EvaluationSerializer(serializers.ModelSerializer):
    ue = UeRelatedField(queryset=Ue.objects.all(), many=False)
    class Meta:
        model = Evaluation
        fields = '__all__'
        
    
class SchoolAtSerializer(serializers.ModelSerializer):
    amphi = AmphiRelatedField(queryset=Amphi.objects.all())
    class Meta:
        model = SchoolAt
        fields = '__all__'
        
