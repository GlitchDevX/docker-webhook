from src.docker_webhook.app.common.logging import app_logger
import os
from typing import Any, Awaitable, Callable, MutableMapping
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

whitelisted_routes = ["/docs", "/openapi.json"]

class SecretCheck(BaseHTTPMiddleware):
    def __init__(self, app: Callable[[MutableMapping[str, Any], Callable[[], Awaitable[MutableMapping[str, Any]]], Callable[[MutableMapping[str, Any]], Awaitable[None]]], Awaitable[None]], dispatch: Callable[[Request, Callable[[Request], Awaitable[Response]]], Awaitable[Response]] | None = None) -> None:
        super().__init__(app, dispatch)
        self._get_secret()

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        if not self._verifiy_secret(request):
            return JSONResponse(status_code=403, content="Forbidden")
        return await call_next(request)

    def _verifiy_secret(self, request: Request):
        for route in whitelisted_routes:
            if request.url.path.startswith(route):
                return True

        received_secret = request.headers.get("X-Api-Secret")
        if received_secret is None or received_secret != self.secret:
            return False
        return True
        
    def _get_secret(self):
        self.secret = os.environ.get("API_SECRET")
        if self.secret is None:
            self.secret = "ADD_PASSWORD_BEFORE_PRODUCTION"
            app_logger.warning("No secret found in environment variable 'API_SECRET', will use 'ADD_PASSWORD_BEFORE_PRODUCTION'")
