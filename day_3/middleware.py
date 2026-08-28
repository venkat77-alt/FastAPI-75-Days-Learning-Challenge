from fastapi import Request
import time , uuid
async def middleware(request: Request, call_next):

    request_id = str(uuid.uuid4()) # unique request id generation 

    request.state.request_id = request_id #assigning the request id to the current request state so that it can be accessed in the route handler

    start_time = time.perf_counter() 

    print("========Request received========")
    print("Request ID:", request_id)
    print("Method:", request.method)
    print("path:", request.url.path)
    print("headers:" , request.headers.get("user-agent"))
    print("request state:",request.state)

    response = await call_next(request)

    end_time = time.perf_counter()
    process_time = end_time - start_time

    response.headers["X-Request-ID"] = request_id       #including request id for the current request in the response headers
    response.headers["X-Process-Time"] = str(process_time)
    print("========Response generated========")
    print("Status Code:", response.status_code)     #response status code
    
    print("Headers:", response.headers)     #response headers

    print("Process Time:", process_time)
    print("Response background:",response.background)      #resonse background
    return response