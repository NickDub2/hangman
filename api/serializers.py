from rest_framework import serializers

from api import constants
from api.models import Game, Word


class GameSerializer(serializers.ModelSerializer):
    current_word = serializers.SerializerMethodField
    word = serializers.SerializerMethodField
    remaining_guesses = serializers.SerializerMethodField

    class Meta:
        model = Game

    def word(self, obj):
        return obj.word.name

    def current_word(self, obj):
        used_letters = list(obj.consonants_used) + list(obj.vowels_used)
        remaining_letters = [l for l in constants.VOWELS + constants.CONSONANTS if l not in used_letters]
        word = obj.word.name
        for letter in remaining_letters:
            word.replace(letter, '-')
        return word

    def remaining_guesses(self, obj):
        return len(obj.word.name) - (len(obj.consonants_used) + len(obj.vowels_used))


class GameInProgressSerializer(serializers.ModelSerializer):
    current_word = serializers.SerializerMethodField
    remaining_guesses = serializers.SerializerMethodField

    class Meta:
        model = Game
        fields = ['current_word', 'remaining_guesses', 'attempts', 'consonants_used', 'vowels_used', 'success']

    def current_word(self, obj):
        used_letters = list(obj.consonants_used) + list(obj.vowels_used)
        remaining_letters = [l for l in constants.VOWELS + constants.CONSONANTS if l not in used_letters]
        word = obj.word.name
        for letter in remaining_letters:
            word.replace(letter, '-')
        return word

    def remaining_guesses(self, obj):
        return len(obj.word.name) - (len(obj.consonants_used) + len(obj.vowels_used))


class WordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Word
