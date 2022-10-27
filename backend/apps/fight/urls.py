from rest_framework.routers import SimpleRouter
from .views import FigthViewSet

app_name = 'fight'


router = SimpleRouter(trailing_slash=False)
router.register(r'fight', FigthViewSet, basename='personajes')

urlpatterns = router.urls