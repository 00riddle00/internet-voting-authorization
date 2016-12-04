from django.db import models
from django.urls import reverse


class VoterData(models.Model):

    name = models.CharField(max_length=36, verbose_name="Vardas")
    surname = models.CharField(max_length=36, verbose_name="Pavardė")
    id_code = models.CharField(max_length=36, verbose_name="Asmens Kodas")


class Voter(models.Model):
    # Voter id (uuid4) comes from CEC server, idetifies real user.
    voter_id = models.CharField(max_length=36, verbose_name="Autorizacijos numeris")

    # Voter ballot id (uuid4) will be published, should not be associated with voter id.
    ballot_id = models.CharField(max_length=36)

    # Voter candidate codes
    candidates = models.TextField()

    def get_absolute_url(self):
        return reverse('ballot', args=[self.ballot_id])
