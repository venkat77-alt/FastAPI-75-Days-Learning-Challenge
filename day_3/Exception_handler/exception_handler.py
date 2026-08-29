from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

async def global_http_exception_handler(request : Request, exc: Exception):

    return JSONResponse(
        status_code=exc.status_code,
        content={

            "status":"error",
            "code":"HTTP Error",
            "message":exc.details,
            "details":None
        }
    )