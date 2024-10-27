import pytest
from rest_framework import status
from rest_framework.test import APIRequestFactory

from groups.views import WordGroupViewSet


@pytest.mark.django_db
class TestWordGroupView:
    def test_list_word_groups(self, api_client, word_group_factory, folder_factory, django_assert_num_queries):
        folder = folder_factory()
        word_group = word_group_factory(folder_id=folder.id)
        factory = APIRequestFactory()
        request = factory.get("/api/folders")
        view = WordGroupViewSet.as_view(actions={"get": "list"})
        with django_assert_num_queries(2):
            response = view(request)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == word_group.name
        assert response.data[0]["id"] == str(word_group.id)
        assert response.data[0]["words"] == []

    def test_move_word_groups(self, folder_factory, word_group_factory):
        folder_1 = folder_factory(name="folder_1")
        folder_2 = folder_factory(name="folder_2")
        word_group = word_group_factory(folder_id=folder_1.id)
        data = {
            "folder_id": str(folder_2.id),
            "word_group_ids": [str(word_group.id)],
        }
        factory = APIRequestFactory()
        request = factory.post("/api/folders", data, format="json")
        view = WordGroupViewSet.as_view(actions={"post": "move_word_items"})
        response = view(request)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "Groups moved successfully"
        word_group.refresh_from_db()
        assert word_group.folder.id == folder_2.id

    def test_move_word_groups_invalid_folder(self, folder_factory, word_group_factory):
        folder = folder_factory(name="folder_1", folder_id="0841b5cc-2327-4dcb-915e-29315be399d3")
        non_existing_folder_id = "b8fbaeb2-cef6-4123-95ea-15f354cfa3f4"
        word_group = word_group_factory(folder_id=folder.id)
        data = {
            "folder_id": non_existing_folder_id,
            "word_group_ids": [str(word_group.id)],
        }
        factory = APIRequestFactory()
        request = factory.post("/api/folders", data, format="json")
        view = WordGroupViewSet.as_view(actions={"post": "move_word_items"})
        response = view(request)
        word_group.refresh_from_db()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert f"Folder with id {non_existing_folder_id} does not exist" in str(response.data)

    def test_move_word_groups_empty_request_body(self):
        factory = APIRequestFactory()
        request = factory.post("/api/folders/move", {}, format="json")  # Pusty payload
        view = WordGroupViewSet.as_view(actions={"post": "move_word_items"})
        response = view(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "This field is required." in str(response.data.get("folder_id", []))
        assert "This field is required." in str(response.data.get("word_group_ids", []))
