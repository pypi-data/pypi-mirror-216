from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.check_health_response_503_details import CheckHealthResponse503Details
    from ..models.check_health_response_503_error import CheckHealthResponse503Error
    from ..models.check_health_response_503_info import CheckHealthResponse503Info


T = TypeVar("T", bound="CheckHealthResponse503")


@attr.s(auto_attribs=True)
class CheckHealthResponse503:
    """
    Attributes:
        status (Union[Unset, str]):  Example: error.
        info (Union[Unset, None, CheckHealthResponse503Info]):  Example: {'database': {'status': 'up'}}.
        error (Union[Unset, None, CheckHealthResponse503Error]):  Example: {'redis': {'status': 'down', 'message':
            'Could not connect'}}.
        details (Union[Unset, CheckHealthResponse503Details]):  Example: {'database': {'status': 'up'}, 'redis':
            {'status': 'down', 'message': 'Could not connect'}}.
    """

    status: Union[Unset, str] = UNSET
    info: Union[Unset, None, "CheckHealthResponse503Info"] = UNSET
    error: Union[Unset, None, "CheckHealthResponse503Error"] = UNSET
    details: Union[Unset, "CheckHealthResponse503Details"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        status = self.status
        info: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.info, Unset):
            info = self.info.to_dict() if self.info else None

        error: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict() if self.error else None

        details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.details, Unset):
            details = self.details.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if info is not UNSET:
            field_dict["info"] = info
        if error is not UNSET:
            field_dict["error"] = error
        if details is not UNSET:
            field_dict["details"] = details

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.check_health_response_503_details import CheckHealthResponse503Details
        from ..models.check_health_response_503_error import CheckHealthResponse503Error
        from ..models.check_health_response_503_info import CheckHealthResponse503Info

        d = src_dict.copy()
        status = d.pop("status", UNSET)

        _info = d.pop("info", UNSET)
        info: Union[Unset, None, CheckHealthResponse503Info]
        if _info is None:
            info = None
        elif isinstance(_info, Unset):
            info = UNSET
        else:
            info = CheckHealthResponse503Info.from_dict(_info)

        _error = d.pop("error", UNSET)
        error: Union[Unset, None, CheckHealthResponse503Error]
        if _error is None:
            error = None
        elif isinstance(_error, Unset):
            error = UNSET
        else:
            error = CheckHealthResponse503Error.from_dict(_error)

        _details = d.pop("details", UNSET)
        details: Union[Unset, CheckHealthResponse503Details]
        if isinstance(_details, Unset):
            details = UNSET
        else:
            details = CheckHealthResponse503Details.from_dict(_details)

        check_health_response_503 = cls(
            status=status,
            info=info,
            error=error,
            details=details,
        )

        return check_health_response_503
