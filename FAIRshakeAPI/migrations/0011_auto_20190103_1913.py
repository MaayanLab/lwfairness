# Generated by Django 2.0.7 on 2019-01-03 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FAIRshakeAPI', '0010_remove_answer_answer_tmp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer',
            field=models.FloatField(null=True),
        ),
    ]
