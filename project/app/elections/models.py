from django.db import models
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _


class ElectoralDistrict(models.Model):
    name = models.CharField(max_length=50)
    ubigeo = models.CharField(max_length=6, unique=True)

    class Meta:
        verbose_name = _("Electoral District")
        verbose_name_plural = _("Electoral Districts")

    def __str__(self):
        return self.name


class ElectionType(models.Model):
    name = models.CharField(max_length=50)
    jne_id = models.BigIntegerField(unique=True)

    class Meta:
        verbose_name = _("Election Type")
        verbose_name_plural = _("Election Types")

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=50)
    jne_id = models.BigIntegerField(unique=True)

    def __str__(self):
        return self.name


class ElectionProcess(models.Model):
    name = models.CharField(max_length=100)

    # relevant dates related to each election process
    call_date = models.DateField(null=True)
    registration_date = models.DateField(null=True)
    opening_date = models.DateField(null=True)
    closing_date = models.DateField(null=True)

    election_types = models.ManyToManyField(ElectionType)
    positions = models.ManyToManyField(Position)
    districts = models.ManyToManyField(ElectoralDistrict)

    jne_id = models.BigIntegerField(unique=True)

    class Meta:
        verbose_name = _("Election Process")
        verbose_name_plural = _("Election Processes")

    def __str__(self):
        return self.name


class PoliticalOrganization(models.Model):
    name = models.CharField(max_length=200)

    jne_id = models.BigIntegerField(unique=True)

    class Meta:
        verbose_name = _("Political Organization")
        verbose_name_plural = _("Political Organizations")

    def __str__(self):
        return self.name


class Gender:
    UNKNOWN = ''
    MALE = 'M'
    FEMALE = 'F'
    CHOICES = (
        (UNKNOWN, ''),
        (MALE, 'Male'),
        (FEMALE, 'Female'),
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

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return ' '.join([self.first_name, self.surname, self.second_surname])


class Candidate(models.Model):
    election = models.ForeignKey(ElectionProcess, on_delete=models.CASCADE, related_name="candidates")
    election_type = models.ForeignKey(ElectionType, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    ballot_position = models.PositiveSmallIntegerField()
    full_name = models.CharField(max_length=200)
    political_organization = models.ForeignKey(PoliticalOrganization, on_delete=models.CASCADE)
    electoral_district = models.ForeignKey(
        ElectoralDistrict, on_delete=models.CASCADE, null=True, blank=True)

    residence_address = models.CharField(max_length=255)
    residence_department = models.CharField(max_length=50)
    residence_province = models.CharField(max_length=50)
    residence_district = models.CharField(max_length=50)
    residence_ubigeo = models.CharField(max_length=6)

    status_on_list = models.CharField(max_length=20, db_index=True)
    jne_id = models.BigIntegerField(unique=True)
    photo_url_path = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name

    def save(self, **kwargs):
        self.full_name = self.person.full_name
        super().save(**kwargs)

    @property
    def photo_url(self):
        _base_url = "https://declara.jne.gob.pe"
        return f"{_base_url}{self.photo_url_path}"

    @property
    def rendered_photo(self):
        return format_html(f"<img width='100px;' src='{self.photo_url}' />")
