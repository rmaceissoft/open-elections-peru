from django.core.management.base import BaseCommand

from pyjne_peru.client import JNE

from app.elections.models import Candidate, CurriculumVitae, PoliticalOrganization


class Command(BaseCommand):
    help = "Import the CV of the candidates who meet the selection criteria"

    def add_arguments(self, parser):
        parser.add_argument(
            "--election_process",
            help="Select candidates that belong to the election process",
        )
        parser.add_argument(
            "--election_type", help="Select candidates that belong to the election type"
        )

    def handle(self, *args, **options):
        # we can only import cv for candidates enrolled in list
        # candidates unregistered don't  have resume at JNE
        lookups = {}
        election_jne_id = options["election_process"]
        if election_jne_id:
            lookups["election__jne_id"] = election_jne_id
        election_type_jne_id = options["election_type"]
        if election_type_jne_id:
            lookups["election_type__jne_id"] = election_type_jne_id

        candidates = Candidate.objects.on_list().filter(**lookups)
        self.stdout.write(f"Selected {candidates.count()} registered candidates")
        for candidate in candidates:
            self.import_candidate_cv(candidate)

    def _get_defaults_from_mapping(self, item, mapping_fields):
        _defaults = {}
        for key, value in mapping_fields.items():
            if isinstance(value, dict):
                model_class = value["model_class"]
                _defaults[key], _ = model_class.objects.get_or_create(
                    jne_id=getattr(item, value["jne_id"]),
                    defaults={
                        k: getattr(item, v)
                        for k, v in value.items()
                        if k not in ["model_class"]
                    },
                )
            else:
                _defaults[key] = getattr(item, value)
        return _defaults

    def import_cv_section(
        self,
        cv_instance,
        reverse_foreign_key,
        cv,
        cv_section_field,
        cv_section_item_pk_field,
        mapping_fields,
    ):
        items = getattr(cv, cv_section_field)
        if not isinstance(items, list):
            items = [items]
        if hasattr(items, "exclude_empty_item"):
            items = items.exclude_empty_item
        for item in items:
            _defaults = self._get_defaults_from_mapping(
                item, mapping_fields=mapping_fields
            )
            related_manager = getattr(cv_instance, reverse_foreign_key)
            related_manager.get_or_create(
                jne_id=getattr(item, cv_section_item_pk_field), defaults=_defaults
            )

    def import_candidate_cv(self, candidate):
        self.stdout.write(
            f"CANDIDATE FULLNAME={candidate.full_name}; CV_JNE_ID={candidate.cv_jne_id}"
        )
        client = JNE()
        resume_info = client.get_resume(
            candidate.cv_jne_id,
            candidate.election.jne_id,
            candidate.political_organization.jne_id,
        )

        defaults = {
            # residence info
            "residence_address": resume_info.oDatosPersonales.strDomicilioDirecc,
            "residence_department": resume_info.oDatosPersonales.strDomiDepartamento,
            "residence_province": resume_info.oDatosPersonales.strDomiProvincia,
            "residence_district": resume_info.oDatosPersonales.strDomiDistrito,
            "residence_ubigeo": resume_info.oDatosPersonales.strUbigeoDomicilio,
            # birth place info
            "birth_country": resume_info.oDatosPersonales.strPaisNacimiento,
            "birth_department": resume_info.oDatosPersonales.strNaciDepartamento,
            "birth_province": resume_info.oDatosPersonales.strNaciProvincia,
            "birth_district": resume_info.oDatosPersonales.strNaciDistrito,
            "birth_ubigeo": resume_info.oDatosPersonales.strUbigeoNacimiento,
            # basic education
            "primary_school": resume_info.oEduBasica.strEduPrimaria == "1",
            "concluded_primary_school": resume_info.oEduBasica.strConcluidoEduPrimaria
            == "1",
            "high_school": resume_info.oEduBasica.strEduSecundaria == "1",
            "concluded_high_school": resume_info.oEduBasica.strConcluidoEduSecundaria
            == "1",
            "has_technical_education": resume_info.oEduTecnico
            and resume_info.oEduTecnico.tengoEduTecnico,
            "has_non_university_education": resume_info.oEduNoUniversitaria
            and resume_info.oEduNoUniversitaria.tengoNoUniversitaria,
            "additional_information": resume_info.oInfoAdicional.strInfoAdicional,
        }
        if not resume_info.oIngresos.is_empty:
            defaults.update(
                {
                    "incomes_year": resume_info.oIngresos.strAnioIngresos,
                    "gross_annual_remunerations_public": resume_info.oIngresos.decRemuBrutaPublico,
                    "gross_annual_remunerations_private": resume_info.oIngresos.decRemuBrutaPrivado,
                    "gross_annual_income_per_individual_year_public": resume_info.oIngresos.decRentaIndividualPublico,
                    "gross_annual_income_per_individual_year_private": resume_info.oIngresos.decRentaIndividualPrivado,
                    "other_income_public": resume_info.oIngresos.decOtroIngresoPublico,
                    "other_income_private": resume_info.oIngresos.decOtroIngresoPrivado,
                }
            )
        cv, _ = CurriculumVitae.objects.get_or_create(
            jne_id=candidate.cv_jne_id, defaults=defaults
        )

        # link cv to candidate
        candidate.cv = cv
        candidate.save()

        # import penal sentences
        self.import_cv_section(
            cv,
            "penal_sentences",
            resume_info,
            "lSentenciaPenal",
            "idHVSentenciaPenal",
            {
                "file_number": "strExpedientePenal",
                "criminal_sentence_date": "fechaSentenciaPenal",
                "judicial_authority": "strOrganoJudiPenal",
                "criminal_offense": "strDelitoPenal",
                "judgment": "strFalloPenal",
                "modality": "strModalidad",
                "other_modality": "strOtraModalidad",
            },
        )

        # import obligation sentences
        self.import_cv_section(
            cv,
            "obligation_sentences",
            resume_info,
            "lSentenciaObliga",
            "idHVSentenciaObliga",
            {
                "demand_matter": "strMateriaSentencia",
                "file_number": "strExpedienteObliga",
                "judicial_authority": "strOrganoJuridicialObliga",
                "judgment": "strFalloObliga",
            },
        )

        # import professional experiences
        self.import_cv_section(
            cv,
            "professional_experiences",
            resume_info,
            "lExperienciaLaboral",
            "idHVExpeLaboral",
            {
                "workplace": "strCentroTrabajo",
                "position": "strOcupacionProfesion",
                "starting_year": "anioTrabajoDesde",
                "ending_year": "anioTrabajoHasta",
            },
        )

        # import university educations
        self.import_cv_section(
            cv,
            "university_educations",
            resume_info,
            "lEduUniversitaria",
            "idHVEduUniversitaria",
            {
                "university": "strUniversidad",
                "degree": "strCarreraUni",
                "year": "anioBachiller",
            },
        )

        # import postgraduate educations
        self.import_cv_section(
            cv,
            "postgraduate_educations",
            resume_info,
            "oEduPosgrago",
            "idHVPosgrado",
            {
                "study_center": "strCenEstudioPosgrado",
                "specialty": "strEspecialidadPosgrado",
                "year": "anioPosgrado",
            },
        )

        # import movable properties
        self.import_cv_section(
            cv,
            "movable_properties",
            resume_info,
            "lBienMueble",
            "idHVBienMueble",
            {
                "property_type": "strVehiculo",
                "features": "strCaracteristica",
                "value": "decValor",
                "comment": "strComentario",
            },
        )

        # import immovable properties
        self.import_cv_section(
            cv,
            "immovable_properties",
            resume_info,
            "lBienInmueble",
            "idHVBienInmueble",
            {
                "property_type": "strTipoBienInmueble",
                "value": "decAutovaluo",
                "comment": "strComentario",
            },
        )

        # import partisan positions
        self.import_cv_section(
            cv,
            "partisan_positions",
            resume_info,
            "lCargoPartidario",
            "idHVCargoPartidario",
            {
                "political_organization": {
                    "model_class": PoliticalOrganization,
                    "jne_id": "idOrgPolCargoPartidario",
                    "name": "strOrgPolCargoPartidario",
                },
                "starting_year": "anioCargoPartiDesde",
                "ending_year": "anioCargoPartiHasta",
                "position": "strCargoPartidario",
            },
        )

        # calculate totals
        cv.calculate_aggregate_totals()
        cv.save()
