from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Candidate, ElectionProcess, ElectionType, ElectoralDistrict, Person,\
    Position, PoliticalOrganization


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('dni', 'first_name', 'surname', 'second_surname', 'birth_date', 'gender')
    list_filter = ('gender', )
    search_fields = ('dni', 'first_name', 'surname', 'second_surname')


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('rendered_photo', 'ballot_position', 'political_organization', 'position',
                    'get_person_dni', 'full_name', 'get_person_birth_date',
                    'get_person_gender', 'status_on_list', 'electoral_district', )
    list_filter = ('election_type', 'electoral_district', 'political_organization',
                   'position', 'person__gender', 'status_on_list', )
    search_fields = ('person__dni', 'person__first_name', 'person__surname', 'person__second_surname')
    autocomplete_fields = ('person', )

    def get_person_dni(self, obj):
        return obj.person.dni
    get_person_dni.short_description = _('DNI')
    get_person_dni.admin_order_field = 'person__dni'

    def get_person_gender(self, obj):
        return obj.person.gender
    get_person_gender.short_description = _('Gender')
    get_person_gender.admin_order_field = 'person__gender'

    def get_person_birth_date(self, obj):
        return obj.person.birth_date
    get_person_birth_date.short_description = _('Birth Date')
    get_person_birth_date.admin_order_field = 'person__birth_date'


@admin.register(ElectoralDistrict)
class ElectoralDistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'ubigeo', )


@admin.register(ElectionType)
class ElectionTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'jne_id')


@admin.register(ElectionProcess)
class ElectionProcessAdmin(admin.ModelAdmin):
    list_display = ('name', 'jne_id', )


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'jne_id', )


@admin.register(PoliticalOrganization)
class PoliticalOrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'jne_id')
