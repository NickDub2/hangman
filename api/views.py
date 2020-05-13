import logging
from random import randint

from django.db import transaction
from django.db.models.aggregates import Count

from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api import constants
from api.models import Game
from api.serializers import GameSerializer, GameInProgressSerializer


logger = logging.getLogger(__name__)


def _get_random_word():
    count = Game.objects.all().aggregate(count=Count('id'))['count']
    random_index = randint(0, count - 1)
    return Game.objects.all()[random_index]


@api_view(['POST'])
def game_start(request):
    with transaction.atomic():
        game = Game.objects.create(word=_get_random_word())
        rsp = {
            'data': {"game_id": game.id},
            'message': "Game Started! Used the response game_id to get guessing!"
        }

    return Response(rsp, status=200)


@api_view(['GET'])
def game_status(request, game_id):
    game = Game.objects.filter(id=game_id)
    if not game:
        error_message = "You have an invalid game id!"
        logger.error(error_message)
        return Response(error_message, status=400)

    game = game.first()

    if game.success:
        resp = {
            'data': GameSerializer(game),
            'message': "CONGRATULATIONS! Your game has been solved!".format(
                word=game.word.name, attempts=game.attempts)
        }
        return Response(resp, status=200)

    if not game.success and game.attempts < len(game.word.name):
        msg = "Your game is not complete! Keep guessing"
        return Response({
            'data': GameInProgressSerializer(game),
            'message': msg}, status=200)

    if not game.success and game.attempts >= len(game.word.name):
        msg = "Your game is complete! But you FAILED"
        return Response({
            'data': GameSerializer(game),
            'message': msg}, status=200)


@api_view(['POST'])
def game_guess_letter(request, game_id):
    game = Game.objects.filter(id=game_id)
    if not game:
        error_message = "You have an invalid game id!"
        return Response(error_message, status=400)

    game = game.first()
    data = request.data

    if not data.get('letter'):
        msg = {'data': {}, 'message': "Your post must include a letter!"}
        return Response(msg, status=200)

    letter = list(data.get('letter'))[0]

    if letter in constants.CONSONANTS:
        game.consonants_used += letter

    elif letter in constants.VOWELS:
        game.vowels_used += letter
    else:
        msg = {'data': GameInProgressSerializer(game), 'message': "INVALID LETTER PROVIDED: {}!".format(letter)}
        return Response(msg, status=200)

    game.attempts += 1
    if game.attempts == len(game.word.name):
        game.success = False
        game.save()

        msg = {'data': GameInProgressSerializer(game), 'message': "HANGMAN! GAME OVER!"}
        return Response(msg, status=200)

    game.save()
    msg = "Keep guessing!"
    return Response({
        'data': GameInProgressSerializer(game),
        'message': msg}, status=200)


@api_view(['POST'])
def game_guess_word(request, game_id):
    game = Game.objects.filter(id=game_id)
    if not game:
        error_message = "You have an invalid game id!"
        return Response(error_message, status=400)

    game = game.first()
    data = request.data

    if not data.get('guess'):
        msg = {'data': GameInProgressSerializer(game), 'message': "Your post must include a guess!"}
        return Response(msg, status=200)

    guess = data.get('guess').lower().strip()

    if guess == game.word.name:
        game.success = True
        game.guess = guess
        game.save()

        resp = {
            'data': GameSerializer(game),
            'message': "CONGRATULATIONS! Your game has been solved!".format(
                word=game.word.name, attempts=game.attempts)
        }
        return Response(resp, status=200)

    else:

        game.guess = guess
        game.save()

        msg = "Your game is complete! But you FAILED"
        return Response({
            'data': GameSerializer(game),
            'message': msg}, status=200)




