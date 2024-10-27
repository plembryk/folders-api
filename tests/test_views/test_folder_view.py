from collections import OrderedDict

import pytest
from rest_framework import status
from rest_framework.test import APIRequestFactory

from groups.views import FolderViewSet


@pytest.mark.django_db
class TestFolderView:
    def test_list_folders(self, api_client, folder_factory):
        folder = folder_factory()
        factory = APIRequestFactory()
        request = factory.get("/api/folders")
        view = FolderViewSet.as_view(actions={"get": "list"})
        response = view(request)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert dict(response.data[0]) == {"id": str(folder.id), "name": folder.name}

    def test_get_folder(self, api_client, folder_factory, word_factory, word_group_factory, django_assert_num_queries):
        folder = folder_factory()
        word_group = word_group_factory(folder_id=folder.id, name="word_group_name")
        words = [
            word_factory(word_group_id=word_group.id, name=word, delimiter="_")
            for word in [f"word_{x}" for x in range(1)]
        ]
        factory = APIRequestFactory()
        request = factory.get("/api/folders")
        view = FolderViewSet.as_view(actions={"get": "retrieve"})
        with django_assert_num_queries(3):
            response = view(request, pk=folder.id)

        expected_data = {
            "id": str(folder.id),
            "name": folder.name,
            "word_groups": [
                {
                    "id": str(word_group.id),
                    "name": word_group.name,
                    "words": [
                        OrderedDict(
                            [
                                ("id", str(word.id)),
                                ("name", word.name),
                                ("word_group_id", word.word_group_id),
                                ("delimiter", word.delimiter),
                            ]
                        )
                        for word in words
                    ],
                }
            ],
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    def test_get_folder_not_found(self, api_client):
        factory = APIRequestFactory()
        request = factory.get("/api/folders")
        view = FolderViewSet.as_view(actions={"get": "retrieve"})
        response = view(request, pk="non-existent-id")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_folder(self, api_client):
        factory = APIRequestFactory()
        name = "New Folder"
        request = factory.post("/api/folders", {"name": name}, format="json")
        view = FolderViewSet.as_view(actions={"post": "create"})
        response = view(request)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == name

    def test_create_folder_missing_name(self, api_client):
        factory = APIRequestFactory()
        request = factory.post("/api/folders", {}, format="json")
        view = FolderViewSet.as_view(actions={"post": "create"})
        response = view(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "This field is required" in str(response.data["name"])

    def test_create_folder_duplicate_name(self, api_client, folder_factory):
        name = "duplicated_name"
        folder_factory(name=name)
        factory = APIRequestFactory()
        request = factory.post("/api/folders", {"name": name}, format="json")
        view = FolderViewSet.as_view(actions={"post": "create"})
        response = view(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "folder with this name already exists" in str(response.data["name"])
