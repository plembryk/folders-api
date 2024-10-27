from rest_framework import serializers

from .models import Folder, Word, WordGroup


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ["id", "name", "word_group_id", "delimiter"]


class WordGroupSerializer(serializers.ModelSerializer):
    words = WordSerializer(many=True, read_only=True)

    class Meta:
        model = WordGroup
        fields = ["id", "name", "words"]


class FolderSerializer(serializers.ModelSerializer):
    word_groups = WordGroupSerializer(many=True, read_only=True)

    class Meta:
        model = Folder
        fields = ["id", "name", "word_groups"]


class FolderBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder
        fields = ["id", "name"]


class WordBatchCreateSerializer(serializers.Serializer):
    delimiter = serializers.CharField(max_length=1)
    words = serializers.ListField(child=serializers.CharField(max_length=255), allow_empty=False)


class MoveWordGroupSerializer(serializers.Serializer):
    folder_id = serializers.UUIDField()
    word_group_ids = serializers.ListField(child=serializers.UUIDField())
