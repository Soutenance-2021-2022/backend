from django.contrib import admin

from transcript.models import AcademicYear, Amphi, Etudiant, Evaluation, Exam, Faculty, Filiere, Level, Obtain, Participate, SchoolAt, Semester, Transcript, Ue

@admin.register(Level,Amphi,Exam,Evaluation,Semester,Ue,Etudiant,SchoolAt,Transcript,Participate,Obtain)
class GenericAdmin(admin.ModelAdmin):
    pass

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('abrev','name')

@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = ('name','faculty')