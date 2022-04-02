from django.db import models

# Create your models here.
class AcademicYear((models.Model)): 
    name = models.CharField(max_length=100)
    
class Faculty(models.Model):
    abrev = models.CharField(max_length=10)
    name = models.CharField(max_length=200)

class Filiere(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    faculty = models.ForeignKey('Faculty',null=False, on_delete=models.CASCADE)
    
class Level(models.Model):
    code = models.CharField(max_length=5)
    intitule = models.CharField(max_length=255)

class Amphi(models.Model):
    name = models.CharField(max_length=255)
    level = models.ForeignKey('Level',null=False, on_delete=models.CASCADE)
    filiere = models.ForeignKey('Filiere',null=False, on_delete=models.CASCADE)
    
class Exam(models.Model):
    code = models.CharField(max_length=10)
    intitule = models.CharField(max_length=255)
    
class Evaluation(models.Model):
    note = models.DecimalField(max_digits=3, decimal_places=2)
    ue = models.ForeignKey('UE',null=False, on_delete=models.CASCADE)
    exam = models.ForeignKey('Exam',null=False, on_delete=models.CASCADE)
    
class Semester(models.Model):
    code= models.CharField(max_length=5)
    name= models.CharField(max_length=200)
    academicyear = models.ForeignKey('AcademicYear',null=False, on_delete=models.CASCADE)
    
class Ue(models.Model):
    code= models.CharField(max_length=10)
    intitule = models.CharField(max_length=255)
    credit = models.PositiveIntegerField()
    description = models.TextField()
    semester = models.ForeignKey('Semester',null=False, on_delete=models.CASCADE)
    amphi = models.ForeignKey('Amphi',null=False, on_delete=models.CASCADE)
    
class Etudiant(models.Model):
    name= models.CharField(max_length=255)
    surname=  models.CharField(max_length=255)
    matricule=  models.CharField(max_length=7)
    born_on = models.DateField()
    born_at = models.CharField(max_length=255)
    gender = models.CharField(max_length=25)
    
class SchoolAt(models.Model):
    amphi = models.ForeignKey('Amphi',null=False, on_delete=models.CASCADE)
    etudiant =  models.ForeignKey('Etudiant',null=False, on_delete=models.CASCADE)

class Transcript(models.Model):
    number = models.CharField(max_length=255)
    mgp = models.PositiveSmallIntegerField()
    complete_credit = models.PositiveIntegerField()
    academicyear = models.ForeignKey('AcademicYear',null=False, on_delete=models.CASCADE)

class Participate(models.Model):
    evaluation = models.ForeignKey('Evaluation',null=False, on_delete=models.CASCADE)
    etudiant =  models.ForeignKey('Etudiant',null=False, on_delete=models.CASCADE)
    decision = models.CharField(max_length=10)
    grade = models.CharField(max_length=5)

class Obtain(models.Model):
    etudiant =  models.ForeignKey('Etudiant',null=False, on_delete=models.CASCADE)
    transcript =  models.ForeignKey('Transcript',null=False, on_delete=models.CASCADE)
    
    