from datetime import date
from typing import Optional

from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers

from app.elections.models import (
    Candidate,
    ElectionProcess,
    ElectionType,
    ElectoralDistrict,
    ObligationSentence,
    PenalSentence,
    PoliticalOrganization,
    Position,
    ProfessionalExperience,
    UniversityEducation,
    PostgraduateEducation,
    MovableProperty,
    ImmovableProperty,
    PartisanPosition,
)


class PoliticalOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliticalOrganization
        fields = ["name", "jne_id"]


class ElectionProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectionProcess
        fields = ["id", "name", "jne_id"]


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ["name", "jne_id"]


class ElectionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectionType
        fields = ["id", "name", "jne_id"]


class ElectoralDistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectoralDistrict
        fields = ["name", "ubigeo"]


class PenalSentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PenalSentence
        fields = [
            "file_number",
            "criminal_sentence_date",
            "judicial_authority",
            "criminal_offense",
            "judgment",
            "modality",
            "other_modality",
            "jne_id",
        ]


class ObligationSentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObligationSentence
        fields = [
            "demand_matter",
            "file_number",
            "judicial_authority",
            "judgment",
            "jne_id",
        ]


class ProfessionalExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalExperience
        fields = ["workplace", "position", "starting_year", "ending_year", "jne_id"]


class UniversityEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversityEducation
        fields = ["university", "degree", "year", "jne_id"]


class PostgraduateEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostgraduateEducation
        fields = ["study_center", "specialty", "year", "jne_id"]


class MovablePropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = MovableProperty
        fields = ["property_type", "features", "value", "comment", "jne_id"]


class ImmovablePropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImmovableProperty
        fields = ["property_type", "value", "comment", "jne_id"]


class PartisanPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartisanPosition
        fields = [
            "political_organization",
            "starting_year",
            "ending_year",
            "position",
            "jne_id",
        ]
        depth = 1


class CandidateSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    surname = serializers.SerializerMethodField()
    second_surname = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    dni = serializers.SerializerMethodField()
    birth_date = serializers.SerializerMethodField()
    residence_ubigeo = serializers.SerializerMethodField()
    birth_ubigeo = serializers.SerializerMethodField()
    primary_school = serializers.SerializerMethodField()
    concluded_primary_school = serializers.SerializerMethodField()
    high_school = serializers.SerializerMethodField()
    concluded_high_school = serializers.SerializerMethodField()
    has_technical_education = serializers.SerializerMethodField()
    has_non_university_education = serializers.SerializerMethodField()
    additional_information = serializers.SerializerMethodField()
    total_incomes = serializers.SerializerMethodField()
    gross_annual_remunerations_public = serializers.SerializerMethodField()
    gross_annual_remunerations_private = serializers.SerializerMethodField()
    gross_annual_income_per_individual_year_public = serializers.SerializerMethodField()
    gross_annual_income_per_individual_year_private = (
        serializers.SerializerMethodField()
    )
    other_income_public = serializers.SerializerMethodField()
    other_income_private = serializers.SerializerMethodField()
    total_sentences = serializers.SerializerMethodField()
    total_penal_sentences = serializers.SerializerMethodField()
    total_obligation_sentences = serializers.SerializerMethodField()

    class Meta:
        model = Candidate
        fields = [
            "id",
            "dni",
            "first_name",
            "surname",
            "second_surname",
            "full_name",
            "gender",
            "birth_date",
            "residence_ubigeo",
            "birth_ubigeo",
            "primary_school",
            "concluded_primary_school",
            "high_school",
            "concluded_high_school",
            "has_technical_education",
            "has_non_university_education",
            "additional_information",
            "photo_url",
            "jne_id",
            "position",
            "ballot_position",
            "political_organization",
            "electoral_district",
            "election_type",
            "status_on_list",
            "total_incomes",
            "gross_annual_remunerations_public",
            "gross_annual_remunerations_private",
            "gross_annual_income_per_individual_year_public",
            "gross_annual_income_per_individual_year_private",
            "other_income_public",
            "other_income_private",
            "total_sentences",
            "total_penal_sentences",
            "total_obligation_sentences",
        ]
        depth = 1

    def get_first_name(self, obj: Candidate) -> str:
        return obj.person.first_name

    def get_surname(self, obj: Candidate) -> str:
        return obj.person.surname

    def get_second_surname(self, obj: Candidate) -> str:
        return obj.person.second_surname

    def get_gender(self, obj: Candidate) -> str:
        return obj.person.gender

    def get_dni(self, obj: Candidate) -> str:
        return obj.person.dni

    @extend_schema_field(OpenApiTypes.DATE)
    def get_birth_date(self, obj: Candidate) -> date:
        return obj.person.birth_date

    def get_residence_ubigeo(self, obj: Candidate) -> Optional[str]:
        if not obj.cv:
            return None
        return obj.cv.residence_ubigeo

    def get_birth_ubigeo(self, obj: Candidate) -> Optional[str]:
        if not obj.cv:
            return None
        return obj.cv.birth_ubigeo

    def get_primary_school(self, obj: Candidate) -> Optional[bool]:
        if not obj.cv:
            return None
        return obj.cv.primary_school

    def get_concluded_primary_school(self, obj: Candidate) -> Optional[bool]:
        if not obj.cv:
            return None
        return obj.cv.concluded_primary_school

    def get_high_school(self, obj: Candidate) -> Optional[bool]:
        if not obj.cv:
            return None
        return obj.cv.high_school

    def get_concluded_high_school(self, obj: Candidate) -> Optional[bool]:
        if not obj.cv:
            return None
        return obj.cv.concluded_high_school

    def get_has_technical_education(self, obj: Candidate) -> Optional[bool]:
        if not obj.cv:
            return None
        return obj.cv.has_technical_education

    def get_has_non_university_education(self, obj: Candidate) -> Optional[bool]:
        if not obj.cv:
            return None
        return obj.cv.has_non_university_education

    def get_additional_information(self, obj: Candidate) -> str:
        if not obj.cv:
            return None
        return obj.cv.additional_information

    def get_total_incomes(self, obj: Candidate) -> int:
        if not obj.cv:
            return None
        return obj.cv.total_incomes

    def get_gross_annual_remunerations_public(self, obj: Candidate) -> int:
        if not obj.cv:
            return None
        return obj.cv.gross_annual_remunerations_public

    def get_gross_annual_remunerations_private(self, obj: Candidate) -> int:
        if not obj.cv:
            return None
        return obj.cv.gross_annual_remunerations_private

    def get_gross_annual_income_per_individual_year_public(self, obj: Candidate) -> int:
        if not obj.cv:
            return None
        return obj.cv.gross_annual_income_per_individual_year_public

    def get_gross_annual_income_per_individual_year_private(
        self, obj: Candidate
    ) -> int:
        if not obj.cv:
            return None
        return obj.cv.gross_annual_income_per_individual_year_private

    def get_other_income_public(self, obj: Candidate) -> int:
        if not obj.cv:
            return None
        return obj.cv.other_income_public

    def get_other_income_private(self, obj: Candidate) -> int:
        if not obj.cv:
            return None
        return obj.cv.other_income_private

    def get_total_sentences(self, obj: Candidate) -> int:
        if not obj.cv:
            return None
        return obj.cv.total_sentences

    def get_total_penal_sentences(self, obj: Candidate) -> int:
        if not obj.cv:
            return None
        return obj.cv.total_penal_sentences

    def get_total_obligation_sentences(self, obj: Candidate) -> int:
        if not obj.cv:
            return None
        return obj.cv.total_obligation_sentences


class CandidateDetailSerializer(CandidateSerializer):
    penal_sentences = serializers.SerializerMethodField()
    obligation_sentences = serializers.SerializerMethodField()
    professional_experiences = serializers.SerializerMethodField()
    university_educations = serializers.SerializerMethodField()
    postgraduate_educations = serializers.SerializerMethodField()
    movable_properties = serializers.SerializerMethodField()
    immovable_properties = serializers.SerializerMethodField()
    partisan_positions = serializers.SerializerMethodField()

    class Meta(CandidateSerializer.Meta):
        fields = CandidateSerializer.Meta.fields + [
            "penal_sentences",
            "obligation_sentences",
            "professional_experiences",
            "university_educations",
            "postgraduate_educations",
            "movable_properties",
            "immovable_properties",
            "partisan_positions",
        ]

    @extend_schema_field(PenalSentenceSerializer(many=True))
    def get_penal_sentences(self, obj: Candidate):
        if not obj.cv:
            return []
        return PenalSentenceSerializer(obj.cv.penal_sentences.all(), many=True).data

    @extend_schema_field(ObligationSentenceSerializer(many=True))
    def get_obligation_sentences(self, obj: Candidate):
        if not obj.cv:
            return []
        return ObligationSentenceSerializer(
            obj.cv.obligation_sentences.all(), many=True
        ).data

    @extend_schema_field(ProfessionalExperienceSerializer(many=True))
    def get_professional_experiences(self, obj: Candidate):
        if not obj.cv:
            return []
        return ProfessionalExperienceSerializer(
            obj.cv.professional_experiences.all(), many=True
        ).data

    @extend_schema_field(UniversityEducationSerializer(many=True))
    def get_university_educations(self, obj: Candidate):
        if not obj.cv:
            return []
        return UniversityEducationSerializer(
            obj.cv.university_educations.all(), many=True
        ).data

    @extend_schema_field(PostgraduateEducationSerializer(many=True))
    def get_postgraduate_educations(self, obj: Candidate):
        if not obj.cv:
            return []
        return PostgraduateEducationSerializer(
            obj.cv.postgraduate_educations.all(), many=True
        ).data

    @extend_schema_field(MovablePropertySerializer(many=True))
    def get_movable_properties(self, obj: Candidate):
        if not obj.cv:
            return []
        return MovablePropertySerializer(
            obj.cv.movable_properties.all(), many=True
        ).data

    @extend_schema_field(ImmovablePropertySerializer(many=True))
    def get_immovable_properties(self, obj: Candidate):
        if not obj.cv:
            return []
        return ImmovablePropertySerializer(
            obj.cv.immovable_properties.all(), many=True
        ).data

    @extend_schema_field(PartisanPositionSerializer(many=True))
    def get_partisan_positions(self, obj: Candidate):
        if not obj.cv:
            return []
        return PartisanPositionSerializer(
            obj.cv.partisan_positions.all(), many=True
        ).data
