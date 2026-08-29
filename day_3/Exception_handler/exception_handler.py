from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

async def global_http_exception_handler(request : Request, exc: Exception):

    return JSONResponse(
        status_code=exc.status_code,
        content={

            "Status":"error",
            "Code":"HTTP Error",
            "Message":exc.detail,
            "Details":None,
            "Request_id":request.state.request_id,
            "Path":request.url.path,
            "Medthod":request.method
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