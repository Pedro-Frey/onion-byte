from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
from api.database import AsyncSessionLocal
from api.services.usage_service import log_usage
from api.services.auth_service import decode_token

class UsageLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = int((time.time() - start_time) * 1000)
        
        # Simples heurística para logar uso em rotas autenticadas
        if request.url.path.startswith("/api/v1/leads"):
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
                payload = decode_token(token)
                if payload and "sub" in payload:
                    async with AsyncSessionLocal() as db:
                        await log_usage(db, payload["sub"], request.url.path, process_time, response.status_code)
                        
        return response
