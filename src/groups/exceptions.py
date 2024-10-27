from rest_framework import status
from rest_framework.exceptions import APIException


class BaseGroupException(Exception):
    """Base exception for all Groups exceptions"""


class FolderDoesNotExistException(BaseGroupException):
    """Exception raised when trying to move WordGroups to non-existent folder"""


class GroupApiException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
