import structlog

from groups.models import Folder

logger = structlog.get_logger(__name__)


def create_folder(name: str) -> Folder:
    folder = Folder.objects.create(name=name)
    logger.info("Created folder", folder_id=folder.id)
    return folder
