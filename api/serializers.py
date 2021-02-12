from rest_framework import serializers
from paper.models import Paper


class PaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paper

        fields = ['title', 'id', 'year']
