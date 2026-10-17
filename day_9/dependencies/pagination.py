from fastapi import Query

async def pagination(page:int=Query(1,ge=1),
                     limit:int=Query(10,ge=1,le=100)):
    return{
        "page": page,
        "limit":limit
    }