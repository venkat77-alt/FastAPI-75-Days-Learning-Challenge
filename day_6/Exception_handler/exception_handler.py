from fastapi import Request
from fastapi.responses import JSONResponse

async def global_http_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status":"error",
            "code":"http error",
            "message":exc.detail,
            "details":None,
            "request_id":request.state.request_id,
            "path":request.url.path,
            "method":request.method
        }
    )
    


async def global_general_exception_handler(request: Request, exc: Exception):

    return JSONResponse(
        status_code=500,
        content={
            "Status":"error",
            "Code":"INTERNAL SERVER ERROR",
            "Message":"There is something went wrong at server side.",
            "Details":None,
            "Request_id":request.state.request_id,
            "path":request.url.path,
            "Method":request.method

        }
    )