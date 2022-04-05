from rest_framework import routers
from transcript.views import AmphiViewSet, EtudiantViewSet, EvaluationViewSet,TranscriptViewSet

router = routers.DefaultRouter()
router.register('etudiants',EtudiantViewSet)
router.register('amphis',AmphiViewSet)
router.register('transcripts',TranscriptViewSet)
router.register('evaluations',EvaluationViewSet)