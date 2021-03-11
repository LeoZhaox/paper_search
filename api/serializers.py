from rest_framework import serializers

from paper.models import Paper, Author


class AuthorSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        return value.name

    class Meta:
        model = Author


class CitationSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    year = serializers.SerializerMethodField()
    n_citation = serializers.SerializerMethodField()
    abstract = serializers.SerializerMethodField()
    venue = serializers.SerializerMethodField()

    class Meta:
        model = Paper
        fields = '__all__'

    def get_year(self, obj):
        if obj.year == None:
            return ''
        return obj.year.strftime('%Y-%m-%d')

    def get_year(self, obj):
        if obj.year == None:
            return ''
        return obj.year.strftime('%Y-%m-%d')

    def get_abstract(self, obj):
        if obj.abstract == None:
            return ''
        return obj.abstract

    def get_venue(self, obj):
        if obj.venue == None:
            return ''
        return obj.venue

    def get_n_citation(self, obj):
        if obj.n_citation is None:
            return 0
        return obj.n_citation


class PaperSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    # references = ReferenceSerializer(many=True)
    references = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    n_citation = serializers.SerializerMethodField()
    abstract = serializers.SerializerMethodField()
    venue = serializers.SerializerMethodField()

    class Meta:
        model = Paper
        fields = '__all__'

    def get_year(self, obj):
        if obj.year == None:
            return ''
        return obj.year.strftime('%Y-%m-%d')

    def get_references(self, obj):
        if obj.references is None:
            return []
        # print('here')
        papers = Paper.objects.filter(id__in=obj.references)
        return CitationSerializer(papers, many=True).data

    # papers = Paper.objects.filter(id__in=obj.references)
    # return papers

    def get_year(self, obj):
        if obj.year == None:
            return ''
        return obj.year.strftime('%Y-%m-%d')

    def get_abstract(self, obj):
        if obj.abstract == None:
            return ''
        return obj.abstract

    def get_venue(self, obj):
        if obj.venue == None:
            return ''
        return obj.venue

    def get_n_citation(self, obj):
        if obj.n_citation is None:
            return 0
        return obj.n_citation
