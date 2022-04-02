from rest_framework import routers
from transcript.views import EtudiantViewSet

router = routers.DefaultRouter()
router.register('etudiant',EtudiantViewSet)