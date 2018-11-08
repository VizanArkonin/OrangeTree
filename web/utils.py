"""
Web service utility functions and decorators
"""
import json

from flask import Response

DEFAULT_MIMETYPE = "text/html"
JSON_MIMETYPE = "text/json"


def get_response(content, mimetype):
    """
    Since return types and data formats may vary, we use this simple wrapper to generate proper response object
    :param content: Content object
    :param mimetype: Type
    :return: Response string or Response object with respective mimetype set
    """
    if isinstance(content, str):
        payload = content
    else:
        payload = json.dumps(content)

    if mimetype == DEFAULT_MIMETYPE:
        return payload
    else:
        return Response(payload, mimetype=mimetype)
