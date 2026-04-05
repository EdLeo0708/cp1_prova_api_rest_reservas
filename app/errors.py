from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from datetime import datetime, timezone


def error_response(status_code: int, error: str, message: str, path: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": status_code,
            "error": error,
            "message": message,
            "path": path,
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    messages = []
    for e in errors:
        field = " -> ".join(str(loc) for loc in e["loc"] if loc != "body")
        messages.append(f"{field}: {e['msg']}" if field else e["msg"])
    return error_response(
        status_code=422,
        error="Unprocessable Entity",
        message="; ".join(messages),
        path=str(request.url.path),
    )
