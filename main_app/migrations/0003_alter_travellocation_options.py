# Generated by Django 4.0.3 on 2022-04-07 02:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_rename_createdby_review_user_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='travellocation',
            options={'ordering': ['name']},
        ),
    ]