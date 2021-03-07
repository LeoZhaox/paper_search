# Generated by Django 3.1.6 on 2021-03-07 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paper', '0010_auto_20210306_1733'),
    ]
    operations = [
        migrations.CreateModel(
            name='QuerySearch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=512, verbose_name='word')),
                ('papers', models.JSONField(verbose_name='papers_id')),
            ],
        ),
    ]
