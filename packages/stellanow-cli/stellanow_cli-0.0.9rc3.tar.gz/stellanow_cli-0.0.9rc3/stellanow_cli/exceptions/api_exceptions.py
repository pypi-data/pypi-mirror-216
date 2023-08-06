"""
Copyright (C) 2022-2023 Stella Technologies (UK) Limited.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

from typing import List

from .cli_exceptions import StellaNowCLIException


class StellaAPIError(StellaNowCLIException):
    """Exception raised for errors in the Stella API."""


class StellaAPIForbiddenError(StellaAPIError):
    """Exception raised for when trying to access the Stella API from blacklisted address."""

    def __init__(self):
        super().__init__("Forbidden", {})


class StellaAPINotFoundError(StellaAPIError):
    """Exception raised for when a requested object does not exist in the Stella API."""

    def __init__(self, details):
        super().__init__("Not Found", details)


class StellaAPIUnauthorisedError(StellaAPIError):
    """Exception raised for when request is not authorised to be performed by requesting entity in the Stella API."""

    def __init__(self, details):
        super().__init__("Unauthorised", details)


class StellaAPIWrongCredentialsError(StellaAPIError):
    """Exception raised for wrong credentials during auth in the Stella API."""

    def __init__(self):
        super().__init__("Unauthorized: Provided username or password is invalid.", {})
