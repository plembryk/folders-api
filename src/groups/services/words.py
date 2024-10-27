import uuid
from typing import Iterable, List

import structlog
from django.db import transaction
from django.utils import timezone

from groups.models import Word

logger = structlog.get_logger(__name__)


@transaction.atomic
def create_words(words_list: Iterable[str], delimiter: str) -> List[Word]:
    now = timezone.now()
    batch_id = uuid.uuid4()
    words = [Word(name=word, delimiter=delimiter, batch_id=batch_id, add_date=now) for word in words_list]
    created_words = Word.objects.bulk_create(words, batch_size=2000)
    logger.info("Words created", words_count=len(created_words), batch_id=batch_id)
    return created_words
