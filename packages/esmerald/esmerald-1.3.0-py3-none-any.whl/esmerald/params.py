from typing import Any, Callable, Dict, Optional, Union

from pydantic.dataclasses import dataclass
from pydantic.fields import FieldInfo, Undefined

from esmerald.enums import EncodingType, ParamType
from esmerald.utils.constants import IS_DEPENDENCY, SKIP_VALIDATION


class Param(FieldInfo):
    in_: ParamType

    def __init__(
        self,
        default: Any = Undefined,
        *,
        alias: Optional[str] = None,
        value_type: Any = Undefined,
        header: Optional[str] = None,
        cookie: Optional[str] = None,
        query: Optional[str] = None,
        path: Optional[str] = None,
        content_encoding: Optional[str] = None,
        required: bool = True,
        title: Optional[str] = None,
        description: Optional[str] = None,
        const: Optional[bool] = None,
        gt: Optional[float] = None,
        ge: Optional[float] = None,
        lt: Optional[float] = None,
        le: Optional[float] = None,
        multiple_of: Optional[float] = None,
        min_items: Optional[int] = None,
        max_items: Optional[int] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        regex: Optional[str] = None,
        example: Any = Undefined,
        examples: Optional[Dict[str, Any]] = None,
        deprecated: Optional[bool] = None,
        include_in_schema: bool = True,
    ) -> None:
        self.deprecated = deprecated
        self.example = example
        self.examples = examples
        self.include_in_schema = include_in_schema

        extra: Dict[str, Any] = {}
        extra.update(header=header)
        extra.update(cookie=cookie)
        extra.update(query=query)
        extra.update(path=path)
        extra.update(required=required)
        extra.update(content_encoding=content_encoding)
        extra.update(value_type=value_type)
        extra.update(example=self.example)
        extra.update(examples=self.examples)
        extra.update(deprecated=self.deprecated)
        extra.update(include_in_schema=self.include_in_schema)

        super().__init__(
            default=default,
            alias=alias,
            title=title,
            description=description,
            const=const,
            gt=gt,
            ge=ge,
            lt=lt,
            le=le,
            multiple_of=multiple_of,
            min_items=min_items,
            max_items=max_items,
            min_length=min_length,
            max_length=max_length,
            regex=regex,
            **extra,
        )


class Header(Param):
    in_ = ParamType.HEADER

    def __init__(
        self,
        *,
        default: Any = Undefined,
        value: Optional[str] = None,
        alias: Optional[str] = None,
        value_type: Any = Undefined,
        content_encoding: Optional[str] = None,
        required: bool = True,
        title: Optional[str] = None,
        description: Optional[str] = None,
        const: Optional[bool] = None,
        gt: Optional[float] = None,
        ge: Optional[float] = None,
        lt: Optional[float] = None,
        le: Optional[float] = None,
        multiple_of: Optional[float] = None,
        min_items: Optional[int] = None,
        max_items: Optional[int] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        regex: Optional[str] = None,
        example: Any = Undefined,
        examples: Optional[Dict[str, Any]] = None,
        deprecated: Optional[bool] = None,
        include_in_schema: bool = True,
    ) -> None:
        super().__init__(
            default=default,
            header=value,
            alias=alias,
            title=title,
            description=description,
            const=const,
            gt=gt,
            ge=ge,
            lt=lt,
            le=le,
            multiple_of=multiple_of,
            min_items=min_items,
            max_items=max_items,
            min_length=min_length,
            max_length=max_length,
            regex=regex,
            required=required,
            content_encoding=content_encoding,
            value_type=value_type,
            example=example,
            examples=examples,
            deprecated=deprecated,
            include_in_schema=include_in_schema,
        )


class Cookie(Param):
    in_ = ParamType.COOKIE

    def __init__(
        self,
        default: Any = Undefined,
        *,
        value_type: Any = Undefined,
        value: Optional[str] = None,
        alias: Optional[str] = None,
        content_encoding: Optional[str] = None,
        required: bool = True,
        title: Optional[str] = None,
        description: Optional[str] = None,
        const: Optional[bool] = None,
        gt: Optional[float] = None,
        ge: Optional[float] = None,
        lt: Optional[float] = None,
        le: Optional[float] = None,
        multiple_of: Optional[float] = None,
        min_items: Optional[int] = None,
        max_items: Optional[int] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        regex: Optional[str] = None,
        example: Any = Undefined,
        examples: Optional[Dict[str, Any]] = None,
        deprecated: Optional[bool] = None,
        include_in_schema: bool = True,
    ) -> None:
        super().__init__(
            default=default,
            cookie=value,
            alias=alias,
            title=title,
            description=description,
            const=const,
            gt=gt,
            ge=ge,
            lt=lt,
            le=le,
            multiple_of=multiple_of,
            min_items=min_items,
            max_items=max_items,
            min_length=min_length,
            max_length=max_length,
            regex=regex,
            required=required,
            content_encoding=content_encoding,
            value_type=value_type,
            example=example,
            examples=examples,
            deprecated=deprecated,
            include_in_schema=include_in_schema,
        )


class Query(Param):
    in_ = ParamType.QUERY

    def __init__(
        self,
        default: Any = Undefined,
        *,
        value_type: Any = Undefined,
        value: Optional[str] = None,
        alias: Optional[str] = None,
        content_encoding: Optional[str] = None,
        required: bool = True,
        title: Optional[str] = None,
        description: Optional[str] = None,
        const: Optional[bool] = None,
        gt: Optional[float] = None,
        ge: Optional[float] = None,
        lt: Optional[float] = None,
        le: Optional[float] = None,
        multiple_of: Optional[float] = None,
        min_items: Optional[int] = None,
        max_items: Optional[int] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        regex: Optional[str] = None,
        example: Any = Undefined,
        examples: Optional[Dict[str, Any]] = None,
        deprecated: Optional[bool] = None,
        include_in_schema: bool = True,
    ) -> None:
        super().__init__(
            default=default,
            query=value,
            alias=alias,
            title=title,
            description=description,
            const=const,
            gt=gt,
            ge=ge,
            lt=lt,
            le=le,
            multiple_of=multiple_of,
            min_items=min_items,
            max_items=max_items,
            min_length=min_length,
            max_length=max_length,
            regex=regex,
            required=required,
            content_encoding=content_encoding,
            value_type=value_type,
            example=example,
            examples=examples,
            deprecated=deprecated,
            include_in_schema=include_in_schema,
        )


class Path(Param):
    in_ = ParamType.PATH

    def __init__(
        self,
        default: Any = Undefined,
        *,
        value_type: Any = Undefined,
        content_encoding: Optional[str] = None,
        required: bool = True,
        title: Optional[str] = None,
        description: Optional[str] = None,
        const: Optional[bool] = None,
        gt: Optional[float] = None,
        ge: Optional[float] = None,
        lt: Optional[float] = None,
        le: Optional[float] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        regex: Optional[str] = None,
        example: Any = Undefined,
        examples: Optional[Dict[str, Any]] = None,
        deprecated: Optional[bool] = None,
        include_in_schema: bool = True,
    ) -> None:
        super().__init__(
            default=default,
            title=title,
            description=description,
            const=const,
            gt=gt,
            ge=ge,
            lt=lt,
            le=le,
            min_length=min_length,
            max_length=max_length,
            regex=regex,
            required=required,
            content_encoding=content_encoding,
            value_type=value_type,
            example=example,
            examples=examples,
            deprecated=deprecated,
            include_in_schema=include_in_schema,
        )


class Body(FieldInfo):
    def __init__(
        self,
        *,
        default: Any = Undefined,
        media_type: Union[str, EncodingType] = EncodingType.JSON,
        content_encoding: Optional[str] = None,
        title: Optional[str] = None,
        alias: Optional[str] = None,
        description: Optional[str] = None,
        const: Optional[bool] = None,
        embed: Optional[bool] = None,
        gt: Optional[float] = None,
        ge: Optional[float] = None,
        lt: Optional[float] = None,
        le: Optional[float] = None,
        multiple_of: Optional[float] = None,
        min_items: Optional[int] = None,
        max_items: Optional[int] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        regex: Optional[str] = None,
        example: Any = Undefined,
        examples: Optional[Dict[str, Any]] = None,
    ) -> None:
        extra: Dict[str, Any] = {}
        self.media_type = media_type
        self.content_encoding = content_encoding
        self.example = example
        self.examples = examples
        extra.update(media_type=self.media_type)
        extra.update(content_encoding=self.content_encoding)
        extra.update(embed=embed)
        super().__init__(
            default=default,
            title=title,
            alias=alias,
            description=description,
            const=const,
            gt=gt,
            ge=ge,
            lt=lt,
            le=le,
            multiple_of=multiple_of,
            min_items=min_items,
            max_items=max_items,
            min_length=min_length,
            max_length=max_length,
            regex=regex,
            **extra,
        )


class Form(Body):
    def __init__(
        self,
        default: Any,
        *,
        media_type: Union[str, EncodingType] = EncodingType.URL_ENCODED,
        content_encoding: Optional[str] = None,
        alias: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        gt: Optional[float] = None,
        ge: Optional[float] = None,
        lt: Optional[float] = None,
        le: Optional[float] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        regex: Optional[str] = None,
        example: Any = Undefined,
        examples: Optional[Dict[str, Any]] = None,
        **extra: Any,
    ) -> None:
        super().__init__(
            default=default,
            embed=True,
            media_type=media_type,
            content_encoding=content_encoding,
            alias=alias,
            title=title,
            description=description,
            gt=gt,
            ge=ge,
            lt=lt,
            le=le,
            min_length=min_length,
            max_length=max_length,
            regex=regex,
            example=example,
            examples=examples,
            **extra,
        )


class File(Form):
    def __init__(
        self,
        default: Any,
        *,
        media_type: Union[str, EncodingType] = EncodingType.MULTI_PART,
        content_encoding: Optional[str] = None,
        alias: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        gt: Optional[float] = None,
        ge: Optional[float] = None,
        lt: Optional[float] = None,
        le: Optional[float] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        regex: Optional[str] = None,
        example: Any = Undefined,
        examples: Optional[Dict[str, Any]] = None,
        **extra: Any,
    ) -> None:
        super().__init__(
            default=default,
            embed=True,
            media_type=media_type,
            content_encoding=content_encoding,
            alias=alias,
            title=title,
            description=description,
            gt=gt,
            ge=ge,
            lt=lt,
            le=le,
            min_length=min_length,
            max_length=max_length,
            regex=regex,
            example=example,
            examples=examples,
            **extra,
        )


class Injects(FieldInfo):
    """
    Creates a FieldInfo class with extra parameters.
    This is used for dependencies and to inject them.

    Example:

        @get(dependencies={"value": Inject(lambda: 13)})
        def myview(value: Injects()):
            return {"value": value}
    """

    def __init__(
        self,
        default: Any = Undefined,
        skip_validation: bool = False,
    ) -> None:
        extra: Dict[str, Any] = {
            IS_DEPENDENCY: True,
            SKIP_VALIDATION: skip_validation,
        }
        super().__init__(default, **extra)


@dataclass
class DirectInject:
    def __init__(
        self,
        dependency: Optional[Callable[..., Any]] = None,
        *,
        use_cache: bool = True,
    ) -> None:
        self.dependency = dependency
        self.use_cache = use_cache

    def __hash__(self) -> int:
        values: Dict[str, Any] = {}
        for key, value in self.__dict__.items():
            values[key] = None
            if isinstance(value, (list, set)):
                values[key] = tuple(value)
            else:
                values[key] = value
        return hash((type(self),) + tuple(values))
