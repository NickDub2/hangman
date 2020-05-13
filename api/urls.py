from django.contrib import admin
from django.urls import include, path

from api.views import game_start, game_status, game_guess_letter, game_guess_word

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('game/start/', game_start, name='game-start'),
    path('game/<game_id>/status/', game_status, name='game-status'),
    path('game/<game_id>/letter', game_guess_letter, name='game-letter'),
    path('game/<game_id>/guess', game_guess_word, name='game-guess')
]
