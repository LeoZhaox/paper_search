# Generated by Django 3.1.6 on 2021-02-10 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paper', '0005_auto_20210206_1644'),
    ]

    operations = [
        migrations.CreateModel(
            name='WordPosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word_name', models.CharField(max_length=128, verbose_name='word_name')),
                ('position', models.JSONField(verbose_name='word_position')),
                ('paper_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paper.paper', verbose_name='paper')),
            ],
        ),
    ]
