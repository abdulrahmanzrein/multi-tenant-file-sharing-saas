from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from jose import JWTError

from app.core.security import decode_token


class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.tenant_id = None
        request.state.user_id = None


        authorization = request.headers.get("Authorization", "")
        
        if authorization.startswith("Bearer "):
            token = authorization[7:]
            try:
                payload = decode_token(token)
                request.state.user_id = payload.get("sub")
                request.state.tenant_id = payload.get("tenant_id")
            except JWTError:
                pass

        response = await call_next(request)
        return response
