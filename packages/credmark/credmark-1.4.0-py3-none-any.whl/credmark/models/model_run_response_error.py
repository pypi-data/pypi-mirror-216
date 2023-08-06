from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.model_call_stack_entry import ModelCallStackEntry


T = TypeVar("T", bound="ModelRunResponseError")


@attr.s(auto_attribs=True)
class ModelRunResponseError:
    """
    Attributes:
        type (str): Short identifying name for type of error Example: 'ModelDataError', 'ModelRunError',
            'ModelEngineError'.
        message (str): A descriptive message about the error Example: An error happened for reason XYZ.
        code (str): A short string, values to specific to the error type Example: generic.
        permanent (bool): If true the error is considered deterministically permanent, for example a requested item does
            not exist on the blockchain within the context of a particular block.
        stack (List['ModelCallStackEntry']):
        detail (Optional[Dict[str, Any]]): An object or null. Some errors may have a detail object containing error-
            specific data. Example: {}.
    """

    type: str
    message: str
    code: str
    permanent: bool
    stack: List["ModelCallStackEntry"]
    detail: Optional[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        message = self.message
        code = self.code
        permanent = self.permanent
        stack = []
        for stack_item_data in self.stack:
            stack_item = stack_item_data.to_dict()

            stack.append(stack_item)

        detail = self.detail

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "type": type,
                "message": message,
                "code": code,
                "permanent": permanent,
                "stack": stack,
                "detail": detail,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_call_stack_entry import ModelCallStackEntry

        d = src_dict.copy()
        type = d.pop("type")

        message = d.pop("message")

        code = d.pop("code")

        permanent = d.pop("permanent")

        stack = []
        _stack = d.pop("stack")
        for stack_item_data in _stack:
            stack_item = ModelCallStackEntry.from_dict(stack_item_data)

            stack.append(stack_item)

        detail = d.pop("detail")

        model_run_response_error = cls(
            type=type,
            message=message,
            code=code,
            permanent=permanent,
            stack=stack,
            detail=detail,
        )

        return model_run_response_error
