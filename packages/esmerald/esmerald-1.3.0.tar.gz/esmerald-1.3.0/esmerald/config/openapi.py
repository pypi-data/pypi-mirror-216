from functools import partial
from typing import TYPE_CHECKING, Dict, List, Optional, Set, Type, Union

from openapi_schemas_pydantic import construct_open_api_with_schema_class
from openapi_schemas_pydantic.v3_1_0 import (
    Components,
    Contact,
    ExternalDocumentation,
    Info,
    License,
    OpenAPI,
    PathItem,
    Reference,
    SecurityRequirement,
    Server,
    Tag,
)
from pydantic import AnyUrl, BaseModel
from typing_extensions import Literal

from esmerald.enums import HttpMethod
from esmerald.openapi.path_item import create_path_item
from esmerald.routing.gateways import Gateway, WebSocketGateway
from esmerald.routing.router import Include
from esmerald.utils.helpers import is_class_and_subclass
from esmerald.utils.url import clean_path

if TYPE_CHECKING:
    from esmerald.applications import Esmerald
    from esmerald.openapi.apiview import OpenAPIView


class OpenAPIConfig(BaseModel):
    create_examples: bool = False
    openapi_apiview: Type["OpenAPIView"]
    title: str
    version: str
    contact: Optional[Contact] = None
    description: Optional[str] = None
    external_docs: Optional[ExternalDocumentation] = None
    license: Optional[License] = None
    security: Optional[List[SecurityRequirement]] = None
    components: Optional[Union[Components, List[Components]]] = None
    servers: List[Server] = [Server(url="/")]
    summary: Optional[str] = None
    tags: Optional[List[Tag]] = None
    terms_of_service: Optional[AnyUrl] = None
    use_handler_docstrings: bool = False
    webhooks: Optional[Dict[str, Union[PathItem, Reference]]] = None
    root_schema_site: Literal["redoc", "swagger", "elements"] = "redoc"
    enabled_endpoints: Set[str] = {
        "redoc",
        "swagger",
        "elements",
        "openapi.json",
        "openapi.yaml",
    }

    def to_openapi_schema(self) -> "OpenAPI":
        if isinstance(self.components, list):
            merged_components = Components()
            for components in self.components:
                for key in components.__fields__.keys():
                    value = getattr(components, key, None)
                    if value:
                        merged_value_dict = getattr(merged_components, key, {}) or {}
                        merged_value_dict.update(value)
                        setattr(merged_components, key, merged_value_dict)
            self.components = merged_components

        return OpenAPI(
            externalDocs=self.external_docs,
            security=self.security,
            components=self.components,
            servers=self.servers,
            tags=self.tags,
            webhooks=self.webhooks,
            info=Info(
                title=self.title,
                version=self.version,
                description=self.description,
                contact=self.contact,
                license=self.license,
                summary=self.summary,
                termsOfService=self.terms_of_service,
            ),
        )

    def get_http_verb(self, path_item: PathItem) -> str:
        if getattr(path_item, "get", None):
            return HttpMethod.GET.value.lower()
        elif getattr(path_item, "post", None):
            return HttpMethod.POST.value.lower()
        elif getattr(path_item, "put", None):
            return HttpMethod.PUT.value.lower()
        elif getattr(path_item, "patch", None):
            return HttpMethod.PATCH.value.lower()
        elif getattr(path_item, "delete", None):
            return HttpMethod.DELETE.value.lower()
        elif getattr(path_item, "header", None):
            return HttpMethod.HEAD.value.lower()

        return HttpMethod.GET.value.lower()

    def create_openapi_schema_model(self, app: "Esmerald") -> "OpenAPI":
        from esmerald.applications import ChildEsmerald, Esmerald

        schema = self.to_openapi_schema()
        schema.paths = {}

        def parse_route(app, prefix=""):  # type: ignore
            if getattr(app, "routes", None) is None:
                return

            # Making sure that ChildEsmerald or esmerald
            if hasattr(app, "app"):
                if (
                    isinstance(app.app, (Esmerald, ChildEsmerald))
                    or (
                        is_class_and_subclass(app.app, Esmerald)
                        or is_class_and_subclass(app.app, ChildEsmerald)
                    )
                ) and not getattr(app.app, "enable_openapi", False):
                    return

            for route in app.routes:
                if isinstance(route, Include) and not route.include_in_schema:
                    continue

                if isinstance(route, WebSocketGateway):
                    continue

                if isinstance(route, Gateway):
                    if route.include_in_schema is False:
                        continue

                    if (
                        isinstance(route, Gateway)
                        and any(
                            handler.include_in_schema
                            for handler, _ in route.handler.route_map.values()
                        )
                        and (route.path_format or "/") not in schema.paths
                    ):
                        path = clean_path(prefix + route.path)
                        path_item = create_path_item(
                            route=route.handler,  # type: ignore
                            create_examples=self.create_examples,
                            use_handler_docstrings=self.use_handler_docstrings,
                        )
                        verb = self.get_http_verb(path_item)
                        if path not in schema.paths:
                            schema.paths[path] = {}  # type: ignore
                        if verb not in schema.paths[path]:  # type: ignore
                            schema.paths[path][verb] = {}  # type: ignore
                        schema.paths[path][verb] = getattr(path_item, verb, None)  # type: ignore
                    continue

                route_app = getattr(route, "app", None)
                if not route_app:
                    continue

                if isinstance(route_app, partial):
                    try:
                        route_app = route_app.__wrapped__
                    except AttributeError:
                        pass

                path = clean_path(prefix + route.path)
                parse_route(route, prefix=f"{path}")  # type: ignore

        parse_route(app)  # type: ignore
        return construct_open_api_with_schema_class(schema)
