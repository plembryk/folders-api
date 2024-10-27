from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .exceptions import FolderDoesNotExistException, GroupApiException
from .models import Folder, Word, WordGroup
from .serializers import (FolderBasicSerializer, FolderSerializer,
                          MoveWordGroupSerializer, WordBatchCreateSerializer,
                          WordGroupSerializer, WordSerializer)
from .services.folders import create_folder
from .services.word_groups import move_word_groups
from .services.words import create_words


class FolderViewSet(ListModelMixin, CreateModelMixin, GenericViewSet, RetrieveModelMixin):

    def get_serializer_class(self):
        if self.action in ("list", "create"):
            return FolderBasicSerializer
        if self.action == "retrieve":
            return FolderSerializer

    def get_queryset(self):
        queryset = Folder.objects.all()
        if self.action == "retrieve":
            queryset = queryset.prefetch_related("word_groups__words")
        return queryset

    def perform_create(self, serializer):
        folder = create_folder(name=serializer.validated_data.get("name"))
        serializer.instance = folder


class WordGroupViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = WordGroupSerializer

    def get_queryset(self):
        return WordGroup.objects.prefetch_related("words").all()

    @action(detail=False, methods=["post"], url_path="move")
    def move_word_items(self, request, pk=None):
        serializer = MoveWordGroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        word_group_ids = serializer.validated_data.get("word_group_ids")
        destination_folder_id = serializer.validated_data.get("folder_id")
        try:
            move_word_groups(word_group_ids=word_group_ids, folder_id=destination_folder_id)
        except FolderDoesNotExistException:
            raise GroupApiException(f"Folder with id {destination_folder_id} does not exist.")

        return Response({"status": "Groups moved successfully"}, status=status.HTTP_200_OK)


class WordViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet, CreateModelMixin):
    def get_queryset(self):
        return Word.objects.all()

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return WordSerializer
        if self.action == "create":
            return WordBatchCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_words = create_words(
            words_list=serializer.validated_data.get("words"),
            delimiter=serializer.validated_data.get("delimiter"),
        )
        word_serializer = WordSerializer(created_words, many=True)
        return Response(word_serializer.data, status=status.HTTP_201_CREATED)
