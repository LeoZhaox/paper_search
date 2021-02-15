from django.db import models


# Create your models here.

class Author(models.Model):
    name = models.CharField(verbose_name='author', max_length=255)

    def __str__(self):
        return self.name


class Paper(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    title = models.TextField(verbose_name="Paper Name")
    authors = models.ManyToManyField(Author, verbose_name="author", null=True)
    year = models.DateTimeField(verbose_name="time", null=True)
    venue = models.CharField(verbose_name="venue", max_length=255, null=True)
    abstract = models.TextField(verbose_name="abstract", null=True)
    n_citation = models.IntegerField(verbose_name="citation", null=True)
    references = models.JSONField(verbose_name="references", null=True)

    def __str__(self):
        return self.title

class WordPosition(models.Model):
    word_name = models.CharField(max_length=128, verbose_name='word_name')
    paper = models.ForeignKey(Paper, verbose_name='paper', on_delete=models.CASCADE)
    position = models.JSONField(verbose_name='word_position')


class PaperLength(models.Model):
    paper = models.ForeignKey(Paper, verbose_name='paper', on_delete=models.CASCADE)
    length = models.IntegerField(verbose_name='paper_length')
