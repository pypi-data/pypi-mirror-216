""" Contains shared errors types that can be raised from API functions """


from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class CredmarkError(Exception, Generic[T]):
    """Raised by api functions when the response status an undocumented status and Client.raise_on_unexpected_status is True"""

    def __init__(self, status_code: int, content: bytes, parsed: Optional[T]):
        self.status_code = status_code
        self.content = content
        self.parsed = parsed

        super().__init__(f"Unexpected status code: {status_code}")


__all__ = ["CredmarkError"]
