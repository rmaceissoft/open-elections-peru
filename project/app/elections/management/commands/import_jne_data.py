from django.core.management.base import BaseCommand

from pyjne_peru.client import JNE

from app.elections.models import Candidate, ElectionProcess, ElectionType, ElectoralDistrict,\
    Gender, Person, PoliticalOrganization, Position


class Command(BaseCommand):

    def handle(self, *args, **options):
        client = JNE()

        election_processes = client.get_election_processes()
        for election_process in election_processes.exclude_empty_item:
            if election_process.idProcesoElectoral not in [110]:
                continue
            # import election process
            self.stdout.write(f"Importing election process {election_process.strProcesoElectoral}")
            data = {
                "name": election_process.strProcesoElectoral,
                "call_date": election_process.strFechaConvocatoria,
                "registration_date": election_process.strFechaRegistro,
                "opening_date": election_process.strFechaAperturaProceso,
                "closing_date": election_process.strFechaCierreProceso
            }
            obj_election_process, _created = ElectionProcess.objects.get_or_create(
                jne_id=election_process.idProcesoElectoral, defaults=data)
            if not _created:
                # update info
                for key, val in data.items():
                    if hasattr(obj_election_process, key):
                        setattr(obj_election_process, key, val)
                obj_election_process.save()
            # import election types for each election process
            election_types = client.get_election_types_by_process(obj_election_process.jne_id)
            for election_type in election_types:
                obj_election_type, _created = ElectionType.objects.get_or_create(
                    jne_id=election_type.idTipoEleccion, defaults={
                        'name': election_type.strTipoEleccion})
                msg_type = "CREATED" if _created else "ALREADY_EXIST"
                self.stdout.write(f"{msg_type}: Election Type: {election_type.strTipoEleccion}")
                obj_election_process.election_types.add(obj_election_type)
                # pull files on list
                self.stdout.write(f"BEGIN: Importing Files on list")
                files_on_list = client.get_files_on_list(
                    election_process.idProcesoElectoral, election_type.idTipoEleccion)
                for file in files_on_list:
                    self.stdout.write(f"BEGIN: Importing File: {file.idExpediente}")
                    # get or create political organization
                    obj_political_organization, _created = PoliticalOrganization.objects.get_or_create(
                        jne_id=file.idOrganizacionPolitica,
                        defaults={
                            'name': file.strOrganizacionPolitica
                        }
                    )
                    msg_type = "CREATED" if _created else "ALREADY_EXIST"
                    self.stdout.write(f"{msg_type}: Political Organization: {file.strOrganizacionPolitica}")
                    # get or create electoral district
                    if file.strUbigeo:
                        obj_electoral_district, _created = ElectoralDistrict.objects.get_or_create(
                            ubigeo=file.strUbigeo,
                            defaults={'name': file.strDistritoElec})
                        msg_type = "CREATED" if _created else "ALREADY_EXIST"
                        self.stdout.write(f"{msg_type}: Electoral District: {file.strDistritoElec}")
                        obj_election_process.districts.add(obj_electoral_district)
                    else:
                        obj_electoral_district = None

                    # import candidates for each file on list
                    candidates = client.get_candidates_by_list(
                        election_process.idProcesoElectoral,
                        election_type.idTipoEleccion,
                        file.idSolicitudLista,
                        file.idExpediente
                    )
                    for candidate in candidates:
                        self.stdout.write(f"Importing candidate {candidate.strCandidato}")
                        obj_person, _ = Person.objects.get_or_create(
                            dni=candidate.strDocumentoIdentidad,
                            defaults={
                                'first_name': candidate.strNombreCompleto,
                                'surname': candidate.strApellidoPaterno,
                                'second_surname': candidate.strApellidoMaterno,
                                'birth_date': candidate.strFechaNacimiento,
                                'gender': Gender.MALE if candidate.strSexo == "1" else Gender.FEMALE
                            })

                        # get or create position
                        obj_position, _ = Position.objects.get_or_create(
                            jne_id=candidate.idCargoEleccion,
                            defaults={
                                'name': candidate.strCargoEleccion
                            })
                        # add position to election process
                        obj_election_process.positions.add(obj_position)
                        # get or create candidate
                        Candidate.objects.get_or_create(
                            jne_id=candidate.idCandidato,
                            defaults={
                                'election': obj_election_process,
                                'election_type': obj_election_type,
                                'person': obj_person,
                                'position': obj_position,
                                'ballot_position': candidate.intPosicion,
                                'political_organization': obj_political_organization,
                                'electoral_district': obj_electoral_district,
                                'status_on_list': candidate.strEstadoExp,
                                'photo_url_path': candidate.strRutaArchivo,
                            })
