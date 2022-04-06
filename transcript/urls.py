
# from rest_framework import routers
from django.urls import path
from transcript.views import AmphiViewSet, EtudiantViewSet, EvaluationViewSet, SchooAtViewSet,TranscriptViewSet

# router = routers.DefaultRouter()
# router.register('etudiants',EtudiantViewSet)
# router.register('amphis',AmphiViewSet)
# router.register('transcripts',TranscriptViewSet)
# router.register('evaluations',EvaluationViewSet)

urlpatterns = [
    path('transcripts',TranscriptViewSet.as_view({
        "get":"list"
    })),
     path('school_at/<int:pk>', SchooAtViewSet.as_view({
            'get': 'retrieve'
    }))
]
