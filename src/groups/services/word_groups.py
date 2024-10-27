from typing import Iterable
from uuid import UUID

import structlog

from groups.exceptions import FolderDoesNotExistException
from groups.models import Folder, WordGroup

logger = structlog.get_logger(__name__)


def move_word_groups(word_group_ids: Iterable[UUID], folder_id: UUID) -> None:

    if not Folder.objects.filter(id=folder_id).exists():
        raise FolderDoesNotExistException

    WordGroup.objects.filter(id__in=word_group_ids).update(folder_id=folder_id)
    logger.info("Moved WordGroups", folder_id=folder_id, word_group_ids=word_group_ids)
