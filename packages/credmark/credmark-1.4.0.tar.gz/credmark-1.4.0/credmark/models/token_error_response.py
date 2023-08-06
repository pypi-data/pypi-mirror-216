from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

T = TypeVar("T", bound="TokenErrorResponse")


@attr.s(auto_attribs=True)
class TokenErrorResponse:
    """
    Attributes:
        status_code (float): If an error response (non-200 status code), the status code will be set. Example: 400.
        error (str): If an error response (non-200 status code), the error will be set with a short string for the code.
            Example: Unprocessable Entity.
        message (Union[List[str], str]): If an error response (non-200 status code), the message will be set with an
            error message. It can either be a string or a list of strings. Example: ['Invalid token address'].
    """

    status_code: float
    error: str
    message: Union[List[str], str]

    def to_dict(self) -> Dict[str, Any]:
        status_code = self.status_code
        error = self.error
        message: Union[List[str], str]

        if isinstance(self.message, list):
            message = self.message

        else:
            message = self.message

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "statusCode": status_code,
                "error": error,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status_code = d.pop("statusCode")

        error = d.pop("error")

        def _parse_message(data: object) -> Union[List[str], str]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                message_type_1 = cast(List[str], data)

                return message_type_1
            except:  # noqa: E722
                pass
            return cast(Union[List[str], str], data)

        message = _parse_message(d.pop("message"))

        token_error_response = cls(
            status_code=status_code,
            error=error,
            message=message,
        )

        return token_error_response
