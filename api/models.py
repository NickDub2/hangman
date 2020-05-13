import logging

from django.db import models


logger = logging.getLogger(__name__)


class Word(models.Model):

    name = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = "word"
        app_label = "api"


class Game(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    vowels_used = models.CharField(max_length=200, null=True, blank=True)
    consonants_used = models.CharField(max_length=200, null=True, blank=True)

    guess = models.CharField(max_length=200, null=True, blank=True)
    attempts = models.IntegerField(default=0)
    success = models.BooleanField(default=False)

    class Meta:
        db_table = "game"
        app_label = "api"
