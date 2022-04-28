
# from rest_framework import routers
from django import views
from django.urls import path
from transcript.views import AmphiViewSet, EtudiantViewSet, EvaluationViewSet, StudentSchoolATViewSet, TranscriptApiViewSet, SchooAtViewSet, SearchTranscriptView,TranscriptViewSet

# router = routers.DefaultRouter()
# router.register('etudiants',EtudiantViewSet)
# router.register('amphis',AmphiViewSet)
# router.register('transcripts',TranscriptViewSet)
# router.register('evaluations',EvaluationViewSet)

urlpatterns = [
    path('transcripts',TranscriptViewSet.as_view({
        "get":"list"
    })),
     path('etudiants',EtudiantViewSet.as_view({
        "get":"list",
        "post":"create"
    })),
    path('etudiant/<str:pk>', EtudiantViewSet.as_view({
        'get': "retrieve",
        'put': 'update',
        'delete': 'destroy'
    })),
    path('assign_amphi', SchooAtViewSet.as_view({
            "get":"list",
            "post":"create"
    })),
    path('school_at/<int:pk>', SchooAtViewSet.as_view({
            'get': 'retrieve'
    })),
    path('check_existing/<int:pk>', SearchTranscriptView.as_view({
            'get': 'retrieve'
    })), 
    path('student_by_amphis/<int:pk>', StudentSchoolATViewSet.as_view({
            'get': 'retrieve'
    })),
    path('transcript', TranscriptApiViewSet.as_view()),
    path('amphis', AmphiViewSet.as_view({
         "get":"list"
    }))
]
