from django.contrib import admin

from transcript.models import AcademicYear, Amphi, Etudiant, Evaluation, Exam, Faculty, Filiere, Level, Obtain, Participate, SchoolAt, Semester, Transcript, Ue


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('code','name','academicyear')
    
@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('abrev','name')

@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = ('name','faculty')

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('code','intitule')
    
@admin.register(Amphi)
class AmphiAdmin(admin.ModelAdmin):
    list_display = ('name','level','filiere')
    
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('code','intitule')
    
@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('ue','note','exam')
    
@admin.register(Ue)
class UeAdmin(admin.ModelAdmin):
    list_display = ('code','intitule','credit','semester','amphi')

@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('matricule','name','surname')
    
@admin.register(Transcript)
class TranscriptAdmin(admin.ModelAdmin):
    list_display = ('number','mgp','complete_credit','academicyear')
    