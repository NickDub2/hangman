import factory

from api.models import (Game)



class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Game