from typing import Awaitable, Callable
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

class Cors(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        response = await call_next(request)
        response.headers.append("Access-Control-Allow-Origin", "*")
        response.headers.append("Access-Control-Allow-Methods", "*")
        response.headers.append("Access-Control-Allow-Headers", "*")
        return response
