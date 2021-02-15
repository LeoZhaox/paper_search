from rest_framework import serializers
from paper.models import Paper, Author


class PaperSerializer(serializers.ModelSerializer):
    # authors = serializers.SerializerMethodField()
    references = serializers.SerializerMethodField()
    #
    class Meta:
        model = Paper
        fields = ['title', 'year', 'venue', 'abstract', 'n_citation', 'references', 'id', 'authors']

    # def get_authors(self, obj):
    # print(obj.authors)
    # authors = Author.objects.filter(id__in=obj.authors)
    # return [author.name for author in authors]
    # return obj.authors

    def get_references(self, obj):
        print(obj.references)

        papers = Paper.objects.filter(id__in=obj.references)
        if papers is not None:
            return [paper.title for paper in papers]
        else:
            return []