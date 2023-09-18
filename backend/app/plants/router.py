from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from elasticsearch import Elasticsearch

es_client = Elasticsearch(hosts=["http://localhost:9200"])

router = APIRouter(prefix="/plants", tags=["plants"])


@router.post("/create_index")
async def create_index(index_name: str) -> JSONResponse:
    """
    Create elasticsearch index for given index name

    Parameters
    ----------
    index_name: str
        Name of the index to be created

    Returns
    -------
    JSONResponse
        JSON response with status of the index creation

    Raises
    ------
    HTTPException
        409 - If index already exists
        500 - If index creation fails
    """
    if es_client.indices.exists(index_name):
        raise HTTPException(status_code=409, detail=f"Index - '{index_name}' already exists")
    else:
        try:
            es_client.indices.create(index=index_name)
            return JSONResponse(content={"status": "True"})
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal Server Error")
