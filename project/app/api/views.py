from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.elections.models import Candidate, ElectionProcess
from .serializers import (
    CandidateDetailSerializer,
    CandidateSerializer,
    ElectionProcessSerializer,
    ElectionTypeSerializer,
    ElectoralDistrictSerializer,
    PoliticalOrganizationSerializer,
    PositionSerializer,
)


class ElectionProcessViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ElectionProcess.objects.all()
    serializer_class = ElectionProcessSerializer

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


class ElectionTypeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ElectionTypeSerializer

    def get_queryset(self):
        election_process = ElectionProcess.objects.get(id=self.kwargs["election_pk"])
        return election_process.election_types.all()

    @action(detail=True)
    def political_organizations(self, request, **kwargs):
        election_process = ElectionProcess.objects.get(id=kwargs["election_pk"])
        obj_rel = election_process.relelectionprocesselectiontype_set.get(
            election_type_id=kwargs["pk"]
        )
        serializer = PoliticalOrganizationSerializer(
            obj_rel.political_organizations.all(), many=True
        )
        return Response(serializer.data)


class CandidateFilter(filters.FilterSet):
    et = filters.NumberFilter(field_name="election_type")
    po = filters.NumberFilter(field_name="political_organization")

    o = filters.OrderingFilter(
        fields=(
            ("cv__total_sentences", "ts"),
            ("cv__total_penal_sentences", "tps"),
            ("cv__total_obligation_sentences", "tos"),
            ("cv__total_incomes", "ti"),
        ),
        field_labels={
            "cv__total_sentences": "Total Sentences",
            "cv__total_penal_sentences": "Total Penal Sentences",
            "cv__total_obligation_sentences": "Total Obligation Sentences",
            "cv__total_incomes": "Total Incomes",
        },
    )

    class Meta:
        model = Candidate
        fields = ["et", "po"]


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="et",
            description="Filter by election type",
            required=False,
            type=OpenApiTypes.NUMBER,
        ),
        OpenApiParameter(
            name="po",
            description="Filter by political organization",
            required=False,
            type=OpenApiTypes.NUMBER,
        ),
        OpenApiParameter(
            name="o",
            description="Order candidates by a given criteria",
            required=False,
            type=OpenApiTypes.STR,
            enum=["-ts", "ts", "-tps", "tps", "-tos", "tos", "-ti", "ti"],
            examples=[
                OpenApiExample(
                    "Order by total sentences (Descending)",
                    value="-ts",
                    description="Candidates with more sentences (both penal and obligation sentences) will appear at top",
                ),
                OpenApiExample(
                    "Order by total sentences (Ascending)",
                    value="ts",
                    description="Candidates with less sentences (both penal and obligation sentences) will appear at top",
                ),
                OpenApiExample(
                    "Order by total penal sentences (Descending)",
                    value="-tps",
                    description="Candidates with more penal sentences will appear at top",
                ),
                OpenApiExample(
                    "Order by total penal sentences (Ascending)",
                    value="tps",
                    description="Candidates with less penal sentences will appear at top",
                ),
                OpenApiExample(
                    "Order by total obligation sentences (Descending)",
                    value="-tos",
                    description="Candidates with more obligation sentences will appear at top",
                ),
                OpenApiExample(
                    "Order by total obligation sentences (Ascending)",
                    value="tos",
                    description="Candidates with less obligation sentences will appear at top",
                ),
                OpenApiExample(
                    "Order by total incomes (Descending)",
                    value="-ti",
                    description="Candidates with less incomes will appear at top",
                ),
                OpenApiExample(
                    "Order by total incomes (Ascending)",
                    value="ti",
                    description="Candidates with more incomes will appear at top",
                ),
            ],
        ),
    ]
)
class CandidateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CandidateSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CandidateFilter

    def get_queryset(self):
        return Candidate.objects.on_list().filter(
            election_id=self.kwargs["election_pk"]
        )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CandidateDetailSerializer
        else:
            return CandidateSerializer
