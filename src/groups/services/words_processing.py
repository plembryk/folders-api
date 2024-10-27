from uuid import UUID

import structlog
from django.db import transaction

from groups.grouping import make_groups
from groups.models import Word, WordGroup
from groups.services.folders import create_folder

logger = structlog.get_logger(__name__)


def process_words() -> None:
    word_batches_to_process = Word.objects.distinct().values_list("batch_id", flat=True).filter(word_group__isnull=True)

    for batch_id in word_batches_to_process:
        process_batch(batch_id=batch_id)


@transaction.atomic
def process_batch(batch_id: UUID) -> None:
    logger.info("Processing batch started", batch_id=batch_id)
    words = list(Word.objects.filter(batch_id=batch_id, word_group__isnull=True).iterator())
    any_word = words[0]
    delimiter = any_word.delimiter
    add_date = any_word.add_date
    folder = create_folder(name=f"{add_date}_delimiter:{delimiter}")
    word_names_mapping = {word.name: word for word in words}
    groups = make_groups(words_list=word_names_mapping.keys(), delimiter=delimiter)

    for group_name, group_words in groups.items():
        word_group = WordGroup.objects.create(name=group_name, folder_id=folder.id)
        for word in group_words:
            word_names_mapping[word].word_group = word_group

    Word.objects.bulk_update(word_names_mapping.values(), ["word_group"], batch_size=2000)
    logger.info("Processing batch finished", batch_id=batch_id)
