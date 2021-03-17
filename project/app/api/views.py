from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.elections.models import ElectionProcess
from .serializers import CandidateSerializer, ElectionProcessSerializer, ElectionTypeSerializer, \
    ElectoralDistrictSerializer, PositionSerializer


class ElectionProcessViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ElectionProcess.objects.all()
    serializer_class = ElectionProcessSerializer

    @action(detail=True)
    def election_types(self, request, pk=None):
        election = self.get_object()
        serializer = ElectionTypeSerializer(election.election_types.all(), many=True)
        return Response(serializer.data)

    @action(detail=True)
    def positions(self, request, pk=None):
        election = self.get_object()
        serializer = PositionSerializer(election.positions.all(), many=True)
        return Response(serializer.data)

    @action(detail=True)
    def electoral_districts(self, request, pk=None):
        election = self.get_object()
        serializer = ElectoralDistrictSerializer(election.districts.all(), many=True)
        return Response(serializer.data)

    @action(detail=True)
    def candidates(self, request, pk=None):
        election = self.get_object()
        qs_candidates = election.candidates.all().select_related(
            'position', 'political_organization', 'electoral_district', 'election_type')
        page = self.paginate_queryset(qs_candidates)
        if page is not None:
            serializer = CandidateSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CandidateSerializer(qs_candidates, many=True)
        return Response(serializer.data)
