class JsonApiClientError(Exception):
    """
    Generic exception class for drupaljsonapiclient
    """
    pass


class ValidationError(JsonApiClientError):
    pass


class DocumentError(JsonApiClientError):
    """
    Raised when 404 or other error takes place.
    Status code is stored in errors['status_code'].
    """
    def __init__(self, *args, errors, **kwargs):
        super().__init__(*args)
        self.errors = errors
        for key, value in kwargs.items():
            setattr(self, key, value)


class DocumentInvalid(JsonApiClientError):
    pass


class AsyncError(JsonApiClientError):
    pass
