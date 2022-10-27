from os.path import basename

from rest_framework.routers import SimpleRouter
from .views import CharacterViewSet
from .views.character_view import PowerViewSet

app_name = 'characters'

router = SimpleRouter(trailing_slash=False)
router.register(r'characters', CharacterViewSet, basename='personajes')
router.register(r'powers', PowerViewSet, basename='poderes')

urlpatterns = router.urls