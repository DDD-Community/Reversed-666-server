# Generated by Django 3.2.8 on 2021-11-04 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brand', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='like_count',
            field=models.BigIntegerField(blank=True, default=0, verbose_name='브랜드를 좋아요한 횟수'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='total_click_count',
            field=models.BigIntegerField(blank=True, default=0, verbose_name='브랜드를 클릭한 횟수'),
        ),
    ]
