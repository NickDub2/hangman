from django.contrib import admin

from api.models import (Word, Game)


admin.site.site_header = 'Hangman Admin'


class WordAdmin(admin.ModelAdmin):
    fields = ['name']


class GameAdmin(admin.ModelAdmin):
    list_display = ["word", "guess, consonants_used, vowels_used, success"]


admin.site.register(Word)
admin.site.register(Game)
