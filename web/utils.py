"""
Web service utility functions and decorators
"""
from flask import Response

DEFAULT_MIMETYPE = "text/html"
JSON_MIMETYPE = "text/json"


def get_response(content, mimetype):
    """
    Since return types and data formats may vary, we use this simple wrapper to generate proper response object
    :param content: Content string
    :param mimetype: Type
    :return: Response string or Response object with respective mimetype set
    """
    if mimetype == DEFAULT_MIMETYPE:
        return content
    else:
        return Response(content, mimetype=mimetype)
