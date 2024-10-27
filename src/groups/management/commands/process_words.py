import time

import structlog
from django.core.management import BaseCommand

from groups.models import Word
from groups.services.words_processing import process_words

logger = structlog.get_logger(__name__)


class Command(BaseCommand):
    help = "Process not processed Words: update Folder's members and WordGroups"
    break_time_in_seconds = None

    def add_arguments(self, parser):
        parser.add_argument(
            "--sleep-time",
            action="store_true",
            help="define process sleep time",
            default=2,
        )

    def handle(self, *args, **options) -> None:
        logger.info("Start processing words")
        self.break_time_in_seconds: int = options["sleep_time"]

        while True:
            exist_words_to_process = Word.objects.filter(word_group__isnull=True).exists()

            if exist_words_to_process:
                logger.info("Found words to process")
                process_words()
            else:
                logger.info("Nothing to do, time to sleep... ")
                time.sleep(self.break_time_in_seconds)
