# Generated by Django 3.2.6 on 2021-08-05 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review_stars',
            field=models.CharField(choices=[('1', '⭐'), ('2', '⭐⭐'), ('3', '⭐⭐⭐'), ('4', '⭐⭐⭐⭐'), ('5', '⭐⭐⭐⭐⭐')], default='⭐⭐⭐⭐⭐', max_length=20, verbose_name='리뷰 별점'),
        ),
    ]
