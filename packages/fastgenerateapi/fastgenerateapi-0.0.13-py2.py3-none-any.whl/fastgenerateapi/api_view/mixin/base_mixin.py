import inspect
from abc import ABC
from typing import List, Callable, Any, Union, Optional, Generic, Type

from fastapi import APIRouter
from fastapi.types import DecoratedCallable

from fastgenerateapi.controller.filter_controller import BaseFilter
from tortoise.expressions import Q
from tortoise.queryset import QuerySet

from fastgenerateapi.settings.register_settings import settings
from starlette.exceptions import HTTPException

from fastgenerateapi.data_type.data_type import DEPENDENCIES, T


class BaseMixin(Generic[T], APIRouter, ABC):

    @property
    def queryset(self) -> QuerySet:
        if not self.model_class:
            return self.error(msg="model_class not allow None")
        if type(settings.app_settings.ACTIVE_DEFAULT_VALUE) == str:
            queryset = self.model_class.filter(
                eval(f"Q({settings.app_settings.WHETHER_DELETE_FIELD}={settings.app_settings.ACTIVE_DEFAULT_VALUE})"))
        else:
            queryset = self.model_class.filter(
                eval(f"Q({settings.app_settings.WHETHER_DELETE_FIELD}={settings.app_settings.ACTIVE_DEFAULT_VALUE})"))
        return queryset

    @property
    def relation_queryset(self) -> QuerySet:
        if not self.relation_model_class:
            return self.error(msg="relation_model_class not allow None")
        if type(settings.app_settings.ACTIVE_DEFAULT_VALUE) == str:
            queryset = self.relation_model_class.filter(
                eval(f"Q({settings.app_settings.WHETHER_DELETE_FIELD}='{settings.app_settings.ACTIVE_DEFAULT_VALUE}')"))
        else:
            queryset = self.relation_model_class.filter(
                eval(f"Q({settings.app_settings.WHETHER_DELETE_FIELD}={settings.app_settings.ACTIVE_DEFAULT_VALUE})"))
        return queryset

    def get_base_filter(self, fields: list) -> list:
        if fields is None:
            return []
        return [BaseFilter(field) if not isinstance(field, BaseFilter) else field for field in fields]

    @staticmethod
    def _get_routes(is_controller_field: bool = False) -> List[str]:
        if is_controller_field:
            return ["get_one_route", "get_all_route", "get_tree_route", "create_route",
                    "update_route", "update_relation_route", "delete_route", "delete_tree_route", "switch_route_fields"]
        return ["get_one", "get_all", "get_tree", "create", "update", "update_relation", "destroy", "destroy_tree",
                "switch"]

    @classmethod
    def _get_cls_func(cls):
        func_list = inspect.getmembers(cls, inspect.isfunction)
        return [func[0] for func in func_list if func[0].startswith("view_")]

    def _add_api_route(
            self,
            path: str,
            endpoint: Callable[..., Any],
            dependencies: Union[bool, DEPENDENCIES],
            error_responses: Optional[List[HTTPException]] = None,
            **kwargs: Any,
    ) -> None:
        dependencies = [] if isinstance(dependencies, bool) else dependencies
        responses: Any = (
            {err.status_code: {"detail": err.detail} for err in error_responses}
            if error_responses
            else None
        )

        self.add_api_route(
            path, endpoint, dependencies=dependencies, responses=responses, **kwargs
        )

    def api_route(
            self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        """Overrides and exiting route if it exists"""
        methods = kwargs["methods"] if "methods" in kwargs else ["GET"]
        self._remove_api_route(path, methods)
        return super().api_route(path, *args, **kwargs)

    def get(
            self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self._remove_api_route(path, ["Get"])
        return super().get(path, *args, **kwargs)

    def post(
            self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self._remove_api_route(path, ["POST"])
        return super().post(path, *args, **kwargs)

    def put(
            self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self._remove_api_route(path, ["PUT"])
        return super().put(path, *args, **kwargs)

    def patch(
            self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self._remove_api_route(path, ["PATCH"])
        return super().put(path, *args, **kwargs)

    def delete(
            self, path: str, *args: Any, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        self._remove_api_route(path, ["DELETE"])
        return super().delete(path, *args, **kwargs)

    def _remove_api_route(self, path: str, methods: List[str]) -> None:
        methods_ = set(methods)

        for route in self.routes:
            if (
                    route.path == f"{self.prefix}{path}"  # type: ignore
                    and route.methods == methods_  # type: ignore
            ):
                self.routes.remove(route)



