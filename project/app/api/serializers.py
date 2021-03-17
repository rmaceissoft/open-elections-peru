from rest_framework import serializers

from app.elections.models import Candidate, ElectionProcess, ElectionType, ElectoralDistrict, Position


class ElectionProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectionProcess
        fields = ['id', 'name', 'jne_id']


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['name', 'jne_id']


class ElectionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectionType
        fields = ['name', 'jne_id']


class ElectoralDistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectoralDistrict
        fields = ['name', 'ubigeo']


class CandidateSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    surname = serializers.SerializerMethodField()
    second_surname = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    dni = serializers.SerializerMethodField()

    class Meta:
        model = Candidate
        fields = ['dni', 'first_name', 'surname', 'second_surname', 'full_name', 'gender',
                  'photo_url', 'jne_id', 'position', 'ballot_position', 'political_organization',
                  'electoral_district', 'election_type', 'status_on_list']
        depth = 1

    def get_first_name(self, obj):
        return obj.person.first_name

    def get_surname(self, obj):
        return obj.person.surname

    def get_second_surname(self, obj):
        return obj.person.second_surname

    def get_gender(self, obj):
        return obj.person.gender

    def get_dni(self, obj):
        return obj.person.dni
