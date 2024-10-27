import pytest
from rest_framework import status
from rest_framework.test import APIRequestFactory

from groups.views import WordViewSet


@pytest.mark.django_db
class TestWordViewSet:
    def test_list_words(self, word_factory):
        word_factory(name="word1", delimiter=",")
        word_factory(name="word2", delimiter=";")
        factory = APIRequestFactory()
        request = factory.get("/api/words/")
        view = WordViewSet.as_view(actions={"get": "list"})
        response = view(request)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_retrieve_word(self, word_factory):
        word = word_factory(name="unique_word", delimiter=".")
        factory = APIRequestFactory()
        request = factory.get(f"/api/words/{word.id}/")
        view = WordViewSet.as_view(actions={"get": "retrieve"})
        response = view(request, pk=word.id)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == word.name
        assert response.data["delimiter"] == word.delimiter
        assert response.data["id"] == str(word.id)

    def test_create_word_empty_request_body(self):
        factory = APIRequestFactory()
        request = factory.post("/api/words", {}, format="json")
        view = WordViewSet.as_view(actions={"post": "create"})
        response = view(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "This field is required." in str(response.data.get("delimiter", []))
        assert "This field is required." in str(response.data.get("words", []))

    def test_create_word_invalid_delimiter(self):
        factory = APIRequestFactory()
        data = {"delimiter": "invalid", "words": ["word1", "word2"]}
        request = factory.post("/api/words", data, format="json")
        view = WordViewSet.as_view(actions={"post": "create"})
        response = view(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Ensure this field has no more than 1 characters." in str(response.data)

    def test_retrieve_word_not_found(self, word_factory):
        factory = APIRequestFactory()
        non_existing_id = "12345678-1234-5678-1234-567812345678"
        request = factory.get(f"/api/words/{non_existing_id}/")
        view = WordViewSet.as_view(actions={"get": "retrieve"})
        response = view(request, pk=non_existing_id)

        assert response.status_code == status.HTTP_404_NOT_FOUND
