from django.urls import path, include
from rest_framework_nested import routers

from .views import CandidateViewSet, ElectionProcessViewSet, ElectionTypeViewSet

router = routers.DefaultRouter()
router.register("elections", ElectionProcessViewSet)

elections_router = routers.NestedDefaultRouter(router, "elections", lookup="election")
elections_router.register(
    r"candidates", CandidateViewSet, basename="election-candidates"
)
elections_router.register(
    r"election_types", ElectionTypeViewSet, basename="election-election-types"
)


urlpatterns = [path("", include(router.urls)), path("", include(elections_router.urls))]
