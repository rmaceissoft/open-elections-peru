from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ElectionProcessViewSet

router = DefaultRouter()

router.register("elections", ElectionProcessViewSet)

urlpatterns = router.urls


urlpatterns = [
    path('', include(router.urls)),
]
