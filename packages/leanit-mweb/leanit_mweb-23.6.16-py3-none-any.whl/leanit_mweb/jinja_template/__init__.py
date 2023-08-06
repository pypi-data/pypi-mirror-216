from __future__ import annotations
import logging

from starlette.datastructures import URL
from starlette.routing import Router
from starlette.templating import pass_context

logger = logging.getLogger(__name__)

from typing import TYPE_CHECKING, Any
from fastapi.templating import Jinja2Templates as FastAPIJinja2Templates

if TYPE_CHECKING:
    pass

class Jinja2Templates(FastAPIJinja2Templates):

    def _create_env(self, *args, **kwargs) -> "jinja2.Environment":
        from leanit_mweb import config
        templates_config = config.get("mweb", {}).get("templates", {})
        cache_size = templates_config.get("cache_size", 1000)
        kwargs["cache_size"] = cache_size

        env = super()._create_env(*args, **kwargs)

        @pass_context
        def url(context: dict, name: str, **path_params: Any) -> URL:
            request = context["request"]
            router: Router = request.scope["router"]
            try:
                url_path = router.url_path_for(name, **path_params)
            except AssertionError as e:
                raise ValueError(f"Could not generate url for '{name}' with params {path_params}: {e}") from e
            return url_path

        env_config = templates_config.get("env", {})
        env.globals.update(env_config.get("globals", {}))

        env.globals["url"] = url

        return env