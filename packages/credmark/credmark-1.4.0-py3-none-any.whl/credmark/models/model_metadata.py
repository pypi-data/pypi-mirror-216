from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelMetadata")


@attr.s(auto_attribs=True)
class ModelMetadata:
    """
    Attributes:
        slug (str): Short identifying name for the model Example: price.quote.
        tags (List[str]): A list of tag strings for the model Example: ["var", "aave"].
        display_name (Union[Unset, str]): Name of the model Example: Price Quote.
        description (Union[Unset, str]): A short description of the model Example: Value at Risk.
        latest_version (Union[Unset, str]): Latest version of the model Example: 1.0.
        developer (Union[Unset, str]): Name of the developer Example: Credmark.
        category (Union[Unset, str]): The category of the model Example: utility.
        subcategory (Union[Unset, str]): The subcategory of the model Example: composition.
        attributes (Union[Unset, Dict[str, Any]]): Attributes for the model
        input (Union[Unset, Dict[str, Any]]): Model input JSON schema
        output (Union[Unset, Dict[str, Any]]): Model output JSON schema
        error (Union[Unset, Dict[str, Any]]): Model error JSON schema
        client (Union[Unset, str]): Client owner of the model Example: public.
        cmf_version (Union[Unset, str]): The version of the credmark model framework used in the latest deployment
            Example: 1.0.0.
    """

    slug: str
    tags: List[str]
    display_name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    latest_version: Union[Unset, str] = UNSET
    developer: Union[Unset, str] = UNSET
    category: Union[Unset, str] = UNSET
    subcategory: Union[Unset, str] = UNSET
    attributes: Union[Unset, Dict[str, Any]] = UNSET
    input: Union[Unset, Dict[str, Any]] = UNSET
    output: Union[Unset, Dict[str, Any]] = UNSET
    error: Union[Unset, Dict[str, Any]] = UNSET
    client: Union[Unset, str] = UNSET
    cmf_version: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        slug = self.slug
        tags = self.tags

        display_name = self.display_name
        description = self.description
        latest_version = self.latest_version
        developer = self.developer
        category = self.category
        subcategory = self.subcategory
        attributes = self.attributes
        input = self.input
        output = self.output
        error = self.error
        client = self.client
        cmf_version = self.cmf_version

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "slug": slug,
                "tags": tags,
            }
        )
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if description is not UNSET:
            field_dict["description"] = description
        if latest_version is not UNSET:
            field_dict["latestVersion"] = latest_version
        if developer is not UNSET:
            field_dict["developer"] = developer
        if category is not UNSET:
            field_dict["category"] = category
        if subcategory is not UNSET:
            field_dict["subcategory"] = subcategory
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if input is not UNSET:
            field_dict["input"] = input
        if output is not UNSET:
            field_dict["output"] = output
        if error is not UNSET:
            field_dict["error"] = error
        if client is not UNSET:
            field_dict["client"] = client
        if cmf_version is not UNSET:
            field_dict["cmfVersion"] = cmf_version

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        slug = d.pop("slug")

        tags = cast(List[str], d.pop("tags"))

        display_name = d.pop("displayName", UNSET)

        description = d.pop("description", UNSET)

        latest_version = d.pop("latestVersion", UNSET)

        developer = d.pop("developer", UNSET)

        category = d.pop("category", UNSET)

        subcategory = d.pop("subcategory", UNSET)

        attributes = d.pop("attributes", UNSET)

        input = d.pop("input", UNSET)

        output = d.pop("output", UNSET)

        error = d.pop("error", UNSET)

        client = d.pop("client", UNSET)

        cmf_version = d.pop("cmfVersion", UNSET)

        model_metadata = cls(
            slug=slug,
            tags=tags,
            display_name=display_name,
            description=description,
            latest_version=latest_version,
            developer=developer,
            category=category,
            subcategory=subcategory,
            attributes=attributes,
            input=input,
            output=output,
            error=error,
            client=client,
            cmf_version=cmf_version,
        )

        return model_metadata
