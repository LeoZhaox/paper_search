from rest_framework import serializers

from paper.models import Paper, Author


class AuthorSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        return value.name

    class Meta:
        model = Author


class PaperSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    references = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()

    class Meta:
        model = Paper
        fields = '__all__'

    def get_references(self, obj):
        if obj.references is None:
            return obj.references
        papers = Paper.objects.filter(id__in=obj.references)
        return papers

    def get_year(self, obj):
        return obj.year.strftime('%Y-%m-%d')
