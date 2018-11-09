"""
Web service utility functions and decorators
"""
import json
from enum import Enum

from flask import Response


class MimeType(Enum):
    """
    Enum for providing mimetypes to Web service response objects
    """
    DEFAULT_MIMETYPE = "text/html"
    JSON_MIMETYPE = "text/json"


class ResponseStatus(Enum):
    """
    Enum for providing status codes to Web service response objects
    """
    OK = 200
    CREATED = 201
    NO_CONTENT = 204

    BAD_REQUEST = 400
    NOT_FOUND = 404
    CONFLICT = 409

    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501


def get_response(content, mimetype=MimeType.DEFAULT_MIMETYPE.value, status=ResponseStatus.OK.value):
    """
    Since return types and data formats may vary, we use this simple wrapper to generate proper response object

    :param content: Content object
    :param mimetype: Mimetype. Consider using MimeType enum for clarity ans consistency
    :param status: HTTP status code. Consider using ResponseStatus enum for clarity and consistency
    :return: Response string or Response object with respective mimetype set
    """
    if isinstance(content, str):
        payload = content
    else:
        payload = json.dumps(content)

    return Response(payload, mimetype=mimetype, status=status)

