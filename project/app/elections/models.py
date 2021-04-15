from django.db import models
from django.db.models import Sum
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from .managers import CandidateQuerySet


class ElectoralDistrict(models.Model):
    name = models.CharField(max_length=50)
    ubigeo = models.CharField(max_length=6, unique=True)

    class Meta:
        verbose_name = _("Electoral District")
        verbose_name_plural = _("Electoral Districts")

    def __str__(self) -> str:
        return self.name


class PoliticalOrganization(models.Model):
    name = models.CharField(max_length=200)

    jne_id = models.BigIntegerField(unique=True)

    class Meta:
        verbose_name = _("Political Organization")
        verbose_name_plural = _("Political Organizations")

    def __str__(self) -> str:
        return self.name


class ElectionType(models.Model):
    name = models.CharField(max_length=50)
    jne_id = models.BigIntegerField(unique=True)

    class Meta:
        verbose_name = _("Election Type")
        verbose_name_plural = _("Election Types")

    def __str__(self) -> str:
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=50)
    jne_id = models.BigIntegerField(unique=True)

    def __str__(self) -> str:
        return self.name


class ElectionProcess(models.Model):
    name = models.CharField(max_length=100)

    # relevant dates related to each election process
    call_date = models.DateField(null=True)
    registration_date = models.DateField(null=True)
    opening_date = models.DateField(null=True)
    closing_date = models.DateField(null=True)

    election_types = models.ManyToManyField(
        ElectionType, through="RelElectionProcessElectionType"
    )
    positions = models.ManyToManyField(Position)
    districts = models.ManyToManyField(ElectoralDistrict)

    jne_id = models.BigIntegerField(unique=True)

    class Meta:
        verbose_name = _("Election Process")
        verbose_name_plural = _("Election Processes")

    def __str__(self) -> str:
        return self.name


class RelElectionProcessElectionType(models.Model):
    election_process = models.ForeignKey(ElectionProcess, on_delete=models.CASCADE)
    election_type = models.ForeignKey(ElectionType, on_delete=models.CASCADE)
    political_organizations = models.ManyToManyField(PoliticalOrganization)

    class Meta:
        unique_together = ("election_process", "election_type")


class Gender:
    UNKNOWN = ""
    MALE = "M"
    FEMALE = "F"
    CHOICES = (
        (UNKNOWN, ""),
        (MALE, "Male"),
        (FEMALE, "Female"),
    )


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    second_surname = models.CharField(max_length=50)
    birth_date = models.DateField(null=True, blank=True)
    birth_address = models.CharField(max_length=255)
    birth_country = models.CharField(max_length=50)
    birth_department = models.CharField(max_length=50)
    birth_province = models.CharField(max_length=50)
    birth_district = models.CharField(max_length=50)
    birth_ubigeo = models.CharField(max_length=6)

    dni = models.CharField(max_length=20, db_index=True)
    gender = models.CharField(max_length=1, choices=Gender.CHOICES, blank=True)

    def __str__(self) -> str:
        return self.full_name

    @property
    def full_name(self) -> str:
        return " ".join([self.first_name, self.surname, self.second_surname])


class Candidate(models.Model):
    election = models.ForeignKey(
        ElectionProcess, on_delete=models.CASCADE, related_name="candidates"
    )
    election_type = models.ForeignKey(ElectionType, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    ballot_position = models.PositiveSmallIntegerField()
    full_name = models.CharField(max_length=200)
    political_organization = models.ForeignKey(
        PoliticalOrganization, on_delete=models.CASCADE
    )
    electoral_district = models.ForeignKey(
        ElectoralDistrict, on_delete=models.CASCADE, null=True, blank=True
    )

    status_on_list = models.CharField(max_length=20, db_index=True)
    jne_id = models.BigIntegerField(unique=True)
    cv_jne_id = models.BigIntegerField(db_index=True, null=True)
    cv = models.ForeignKey(
        "CurriculumVitae", on_delete=models.SET_NULL, null=True, blank=True
    )
    photo_url_path = models.CharField(max_length=255)

    objects = CandidateQuerySet.as_manager()

    def __str__(self) -> str:
        return self.full_name

    def save(self, **kwargs):
        self.full_name = self.person.full_name
        super().save(**kwargs)

    @property
    def photo_url(self) -> str:
        _base_url = "https://declara.jne.gob.pe"
        return f"{_base_url}{self.photo_url_path}"

    @property
    def rendered_photo(self) -> str:
        return format_html(f"<img width='100px;' src='{self.photo_url}' />")


class CurriculumVitae(models.Model):
    # residence info
    residence_address = models.CharField(max_length=255)
    residence_department = models.CharField(max_length=50)
    residence_province = models.CharField(max_length=50)
    residence_district = models.CharField(max_length=50)
    residence_ubigeo = models.CharField(max_length=6)
    # birth place
    birth_country = models.CharField(max_length=100)
    birth_department = models.CharField(max_length=50)
    birth_province = models.CharField(max_length=50)
    birth_district = models.CharField(max_length=50)
    birth_ubigeo = models.CharField(max_length=6)

    primary_school = models.BooleanField()
    concluded_primary_school = models.BooleanField()
    high_school = models.BooleanField()
    concluded_high_school = models.BooleanField()
    has_technical_education = models.BooleanField(null=True, blank=True)
    has_non_university_education = models.BooleanField(null=True, blank=True)
    additional_information = models.TextField()

    # income
    incomes_year = models.PositiveIntegerField(null=True, blank=0)
    gross_annual_remunerations_public = models.PositiveBigIntegerField(
        null=True, blank=0
    )
    gross_annual_remunerations_private = models.PositiveBigIntegerField(
        null=True, blank=0
    )
    gross_annual_income_per_individual_year_public = models.PositiveBigIntegerField(
        null=True, blank=0
    )
    gross_annual_income_per_individual_year_private = models.PositiveBigIntegerField(
        null=True, blank=0
    )
    other_income_public = models.PositiveBigIntegerField(null=True, blank=0)
    other_income_private = models.PositiveBigIntegerField(null=True, blank=0)

    jne_id = models.BigIntegerField(unique=True)

    # calculated fields
    total_incomes = models.PositiveBigIntegerField()
    # properties
    total_movable_properties_value = models.PositiveBigIntegerField(default=0)
    total_immovable_properties_value = models.PositiveBigIntegerField(default=0)
    total_movable_immovable_properties_value = models.PositiveBigIntegerField()
    # sentences
    total_penal_sentences = models.PositiveIntegerField(default=0)
    total_obligation_sentences = models.PositiveIntegerField(default=0)
    total_sentences = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.jne_id}"

    def calculate_aggregate_totals(self):
        self.total_movable_properties_value = (
            self.movable_properties.aggregate(total=Sum("value")).get("total") or 0
        )
        self.total_immovable_properties_value = (
            self.immovable_properties.aggregate(total=Sum("value")).get("total") or 0
        )
        self.total_penal_sentences = self.penal_sentences.count()
        self.total_obligation_sentences = self.obligation_sentences.count()

    def save(self, **kwargs):
        self.total_incomes = (
            (self.gross_annual_remunerations_public or 0)
            + (self.gross_annual_remunerations_private or 0)
            + (self.gross_annual_income_per_individual_year_public or 0)
            + (self.gross_annual_income_per_individual_year_private or 0)
            + (self.other_income_public or 0)
            + (self.other_income_private or 0)
        )
        self.total_movable_immovable_properties_value = (
            self.total_movable_properties_value + self.total_immovable_properties_value
        )
        self.total_sentences = (
            self.total_penal_sentences + self.total_obligation_sentences
        )
        super().save(**kwargs)


class PenalSentence(models.Model):
    cv = models.ForeignKey(
        CurriculumVitae, on_delete=models.CASCADE, related_name="penal_sentences"
    )
    file_number = models.CharField(max_length=40)
    criminal_sentence_date = models.DateField()
    judicial_authority = models.CharField(max_length=100)
    criminal_offense = models.CharField(max_length=100)
    judgment = models.CharField(max_length=255)
    modality = models.CharField(max_length=50)
    other_modality = models.CharField(max_length=100)
    jne_id = models.BigIntegerField(unique=True)

    def __str__(self) -> str:
        return f"{self.cv} {self.file_number}"


class ObligationSentence(models.Model):
    cv = models.ForeignKey(
        CurriculumVitae, on_delete=models.CASCADE, related_name="obligation_sentences"
    )
    demand_matter = models.CharField(max_length=50)
    file_number = models.CharField(max_length=40)
    judicial_authority = models.CharField(max_length=100)
    judgment = models.TextField()
    jne_id = models.BigIntegerField(unique=True)

    def __str__(self) -> str:
        return f"{self.cv} {self.file_number}"


class ProfessionalExperience(models.Model):
    cv = models.ForeignKey(
        CurriculumVitae,
        on_delete=models.CASCADE,
        related_name="professional_experiences",
    )
    workplace = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    starting_year = models.PositiveIntegerField()
    ending_year = models.PositiveIntegerField(null=True, blank=True)
    jne_id = models.BigIntegerField(unique=True)

    def __str__(self) -> str:
        return f"{self.cv} {self.jne_id}"


class UniversityEducation(models.Model):
    cv = models.ForeignKey(
        CurriculumVitae, on_delete=models.CASCADE, related_name="university_educations"
    )
    university = models.CharField(max_length=200)
    degree = models.CharField(max_length=150)
    year = models.PositiveIntegerField(null=True, blank=True)
    jne_id = models.BigIntegerField(unique=True)

    def __str__(self) -> str:
        return f"{self.cv} {self.jne_id}"


class PostgraduateEducation(models.Model):
    cv = models.ForeignKey(
        CurriculumVitae,
        on_delete=models.CASCADE,
        related_name="postgraduate_educations",
    )
    study_center = models.CharField(max_length=200)
    specialty = models.CharField(max_length=200)
    year = models.PositiveIntegerField(null=True, blank=True)
    jne_id = models.BigIntegerField(unique=True)

    def __str__(self) -> str:
        return f"{self.cv} {self.jne_id}"


class MovableProperty(models.Model):
    cv = models.ForeignKey(
        CurriculumVitae, on_delete=models.CASCADE, related_name="movable_properties"
    )
    property_type = models.CharField(max_length=100)
    features = models.CharField(max_length=255, blank=True)
    value = models.BigIntegerField()
    comment = models.TextField(blank=True)
    jne_id = models.BigIntegerField(unique=True)

    def __str__(self) -> str:
        return f"{self.cv} {self.jne_id}"


class ImmovableProperty(models.Model):
    cv = models.ForeignKey(
        CurriculumVitae, on_delete=models.CASCADE, related_name="immovable_properties"
    )
    property_type = models.CharField(max_length=100)
    value = models.BigIntegerField()
    comment = models.TextField(blank=True)
    jne_id = models.BigIntegerField(unique=True)

    def __str__(self) -> str:
        return f"{self.cv} {self.jne_id}"


class PartisanPosition(models.Model):
    cv = models.ForeignKey(
        CurriculumVitae, on_delete=models.CASCADE, related_name="partisan_positions"
    )
    political_organization = models.ForeignKey(
        PoliticalOrganization, on_delete=models.CASCADE
    )
    starting_year = models.PositiveIntegerField()
    ending_year = models.PositiveIntegerField(null=True, blank=True)
    position = models.CharField(max_length=100)
    jne_id = models.BigIntegerField(unique=True)

    def __str__(self) -> str:
        return f"{self.cv} {self.jne_id}"
