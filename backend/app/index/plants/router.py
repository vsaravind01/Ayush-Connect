from app.index.utils.es import ElasticSearchClient
from fastapi import APIRouter, Body, Depends, Query
from fastapi.responses import JSONResponse

es_client = ElasticSearchClient()

router = APIRouter(prefix="/plants", tags=["index"])


@router.get("/")
async def get_plants(page: int = Query(1, ge=1),
                     size: int = Query(20, ge=1, le=50)) -> JSONResponse:
    """
    Get all plants from plants index

    Parameters
    ----------
    - **page**: (int) Page number - greater than or equal to 1 (default: 1)
    - **size**: (int) Number of plants per page - greater than or equal to 1 and less than or equal to 50 (default: 50)

    Returns
    -------
    - **JSONResponse**: JSON response with all plants
    """
    client = es_client.client
    response = client.search(index="plants",
                             size=size,
                             from_=(page - 1) * size,
                             query={"match_all": {}})
    return JSONResponse(status_code=200, content=response.body)


@router.get("/search")
async def search_plants(
        query: str = Query(..., min_length=3),
        fields: str = Query(
            "generic_name,scientific_name,accepted_scientific_name"),
        page: int = Query(1, ge=1),
        size: int = Query(20, ge=1, le=50)) -> JSONResponse:
    """
    Search plants from plants index

    Parameters
    ----------
    - **query**: (str) Search query
    - **page**: (int) Page number - greater than or equal to 1 (default: 1)
    - **size**: (int) Number of plants per page - greater than or equal to 1 and less than or equal to 50 (default: 50)

    Returns
    -------
    - **JSONResponse**: JSON response with all plants
    """
    client = es_client.client
    fields = fields.split(",")
    response = client.search(
        index="plants",
        size=size,
        from_=(page - 1) * size,
        query={"multi_match": {
            "query": query,
            "fields": fields
        }})
    return JSONResponse(status_code=200, content=response.body)


@router.get("/{plant_id}")
async def get_plant(plant_id: str) -> JSONResponse:
    """
    Get plant details from plants index

    Parameters
    ----------
    - **plant_id**: (str) Plant id

    Returns
    -------
    - **JSONResponse**: JSON response with plant details
    """
    client = es_client.client
    response = client.get(index="plants", id=plant_id)
    return JSONResponse(status_code=200, content=response.body)
