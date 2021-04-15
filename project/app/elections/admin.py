from django.contrib import admin
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import F
from django.utils.translation import ugettext_lazy as _

from .models import (
    Candidate,
    CurriculumVitae,
    ElectionProcess,
    ElectionType,
    ElectoralDistrict,
    Person,
    Position,
    PoliticalOrganization,
)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        "dni",
        "first_name",
        "surname",
        "second_surname",
        "birth_date",
        "gender",
    )
    list_filter = ("gender",)
    search_fields = ("dni", "first_name", "surname", "second_surname")


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = (
        "rendered_photo",
        "ballot_position",
        "political_organization",
        "position",
        "get_person_dni",
        "full_name",
        "get_person_birth_date",
        "get_person_gender",
        "status_on_list",
        "electoral_district",
        "get_total_incomes",
        "get_total_sentences",
        "get_total_penal_sentences",
        "get_total_obligation_sentences",
        "jne_id",
    )
    list_filter = (
        "election_type",
        "electoral_district",
        "political_organization",
        "position",
        "person__gender",
        "status_on_list",
    )
    search_fields = (
        "person__dni",
        "person__first_name",
        "person__surname",
        "person__second_surname",
    )
    autocomplete_fields = ("person",)

    def get_person_dni(self, obj):
        return obj.person.dni

    get_person_dni.short_description = _("DNI")
    get_person_dni.admin_order_field = "person__dni"

    def get_person_gender(self, obj):
        return obj.person.gender

    get_person_gender.short_description = _("Gender")
    get_person_gender.admin_order_field = "person__gender"

    def get_person_birth_date(self, obj):
        return obj.person.birth_date

    get_person_birth_date.short_description = _("Birth Date")
    get_person_birth_date.admin_order_field = "person__birth_date"

    def get_total_incomes(self, obj):
        if not obj.cv:
            return 0
        return intcomma(obj.cv.total_incomes)

    get_total_incomes.short_description = _("Total Incomes")
    get_total_incomes.admin_order_field = F("cv__total_incomes").desc(nulls_last=True)

    def get_total_sentences(self, obj):
        if not obj.cv:
            return 0
        return obj.cv.total_sentences

    get_total_sentences.short_description = _("Total Sentences")
    get_total_sentences.admin_order_field = F("cv__total_sentences").desc(
        nulls_last=True
    )

    def get_total_penal_sentences(self, obj):
        if not obj.cv:
            return 0
        return obj.cv.total_penal_sentences

    get_total_penal_sentences.short_description = _("Total Penal Sentences")
    get_total_penal_sentences.admin_order_field = F("cv__total_penal_sentences").desc(
        nulls_last=True
    )

    def get_total_obligation_sentences(self, obj):
        if not obj.cv:
            return 0
        return obj.cv.total_obligation_sentences

    get_total_obligation_sentences.short_description = _("Total Obligation Sentences")
    get_total_obligation_sentences.admin_order_field = F(
        "cv__total_obligation_sentences"
    ).desc(nulls_last=True)


@admin.register(CurriculumVitae)
class CurriculumVitaeAdmin(admin.ModelAdmin):
    list_display = (
        "residence_ubigeo",
        "birth_ubigeo",
        "primary_school",
        "concluded_primary_school",
        "high_school",
        "concluded_high_school",
        "incomes_year",
        "gross_annual_remunerations_public",
        "gross_annual_remunerations_private",
        "gross_annual_income_per_individual_year_public",
        "gross_annual_income_per_individual_year_private",
        "other_income_public",
        "other_income_private",
        "jne_id",
    )


@admin.register(ElectoralDistrict)
class ElectoralDistrictAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "ubigeo",
    )


@admin.register(ElectionType)
class ElectionTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "jne_id")


@admin.register(ElectionProcess)
class ElectionProcessAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "jne_id",
    )


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "jne_id",
    )


@admin.register(PoliticalOrganization)
class PoliticalOrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "jne_id")
