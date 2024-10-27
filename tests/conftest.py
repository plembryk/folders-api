import uuid
from datetime import datetime
from typing import Any, Callable, Optional, Union
from uuid import UUID

import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from groups.models import Folder, Word, WordGroup


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def folder_factory():
    def _builder(name: str = "folder_name", folder_id: Optional[Union[UUID, str]] = None) -> Folder:
        return Folder.objects.create(name=name, id=folder_id or uuid.uuid4())

    return _builder


@pytest.fixture
def word_group_factory(folder_factory):
    def _builder(name: str = "word_group_name", folder_id: Optional[UUID] = None) -> WordGroup:
        if folder_id is None:
            folder_id = folder_factory().id
        return WordGroup.objects.create(name=name, folder_id=folder_id)

    return _builder


@pytest.fixture
def word_factory():
    def _builder(
        name: str = "word",
        delimiter: str = "_",
        batch_id: Optional[UUID] = None,
        word_group_id: Optional[UUID] = None,
        add_date: Optional[datetime] = None,
    ) -> Word:
        if batch_id is None:
            batch_id = uuid.uuid4()
        return Word.objects.create(
            name=name,
            delimiter=delimiter,
            batch_id=batch_id,
            word_group_id=word_group_id,
            add_date=add_date or timezone.now(),
        )

    return _builder
