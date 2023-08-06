from collections import namedtuple
from typing import List, NamedTuple

try:
    from simplejson import JSONDecodeError
except ImportError:
    from json import JSONDecodeError

from requests.exceptions import HTTPError

from fiddler.utils import logging

logger = logging.getLogger(__name__)


class NotSupported(Exception):
    pass


class AsyncJobFailed(Exception):
    pass


class ErrorResponseHandler:
    def __init__(self, http_error: HTTPError) -> None:
        self.http_error = http_error
        self.response = http_error.response
        self.ErrorResponse = namedtuple(
            'ErrorResponse', ['status_code', 'error_code', 'message', 'errors']
        )

    def get_error_details(self) -> NamedTuple:
        status_code = self.response.status_code
        try:
            error_details = self.response.json().get('error', {})
        except JSONDecodeError:
            raise FiddlerAPIHTTPException(
                status_code=self.response.status_code,
                error_code=self.response.status_code,
                message=f'Invalid response content-type. {self.response.status_code}:{self.response.content}',
                errors=[],
            )
        error_code = error_details.get('code')
        message = error_details.get('message')
        errors = error_details.get('errors')
        return self.ErrorResponse(status_code, error_code, message, errors)


class FiddlerBaseException(Exception):
    pass


class FiddlerException(FiddlerBaseException):
    '''
    Exception class to handle non API response exceptions
    '''


class FiddlerAPICallException(FiddlerBaseException):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class FiddlerAPIHTTPException(FiddlerBaseException):
    '''
    Exception class to specifically handle Fiddler's API error responses structure.
    This is a generic API response exception class
    '''

    # @TODO: Handle standard API error response.
    # How to surface error messages coming form the server. Server responds error messages in a list. Which error to surface?
    def __init__(
        self, status_code: int, error_code: int, message: str, errors: List[str]
    ) -> None:
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.errors = errors
        super().__init__(self.message)


class FiddlerAPIBadRequestException(FiddlerAPIHTTPException):
    pass


class FiddlerAPINotFoundException(FiddlerAPIHTTPException):
    pass


class FiddlerAPIConflictException(FiddlerAPIHTTPException):
    pass


class FiddlerAPIForbiddenException(FiddlerAPIHTTPException):
    pass


class FiddlerAPIInternalServerErrorException(FiddlerAPIHTTPException):
    pass

