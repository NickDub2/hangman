import os
from django.db import migrations, models


def forwards_func(apps, schema_editor):
    current_path = os.path.abspath(os.getcwd())
    words = []

    with open(os.path.join(current_path, 'api/migrations/initial_words.txt')) as words_file:
        for line in words_file.readlines():
            words += line

    Word = apps.get_model("api", "Word")
    for word in words:
        new_word = Word(name=word.lower().strip())
        new_word.save()


class Migration(migrations.Migration):

    dependencies = [('api', '0001_initial')]

    operations = [
        migrations.RunPython(forwards_func),
    ]