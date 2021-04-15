from django.db import models


class CandidateQuerySet(models.QuerySet):
    def on_list(self):
        return self.filter(status_on_list="INSCRITO")
