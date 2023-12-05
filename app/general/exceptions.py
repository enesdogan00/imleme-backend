from fastapi import HTTPException, status

from app.general.constants import Error


class _BaseException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: str = "Bilinmeyen bir hata oluştu",
    ):
        self.status_code = status_code
        self.detail = detail
        super().__init__(status_code, detail)


class NoRecordException(_BaseException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=Error.no_record)


class DuplicateRecordException(_BaseException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT, detail=Error.duplicate_record
        )


class PermissionDeniedException(_BaseException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, detail=Error.permission_denied
        )
