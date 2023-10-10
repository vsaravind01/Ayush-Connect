from app.index.utils.es import ElasticSearchClient
from fastapi import APIRouter, Body, Depends, Query
from fastapi.exceptions import HTTPException
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


@router.post("/")
async def add_plants(plant_data: dict = Body(...)) -> JSONResponse:
    """
    Add plant records to the Elasticsearch index.

    Parameters
    ----------
    - **plant_data**: (dict) JSON data containing plant information.

    Returns
    -------
    - **JSONResponse**: JSON response indicating the success or failure of the addition.

    Raises
    ------
    - **HTTPException**:
        - **500** - If the addition fails.
    """
    try:
        # Add the plant record to the Elasticsearch index
        response = es_client.add_document("plants", plant_data)
        
        if response:
            return JSONResponse(
                status_code=201, 
                content={
                    "message": "Plant records added successfully"
                })
        else:
            return JSONResponse(
                status_code=500, 
                content={
                    "message": "Failed to add plant records to the index"
                })
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Plant record addition failed - Internal Server Error: {str(e)}")


@router.put("/{plant_id}")
async def update_plant(plant_id: str, plant_data: dict = Body(...)) -> JSONResponse:
    """
    Update a plant record in the Elasticsearch index.

    Parameters
    ----------
    - **plant_id**: (str) Plant ID to be updated.
    - **plant_data**: (dict) JSON data containing updated plant information.

    Returns
    -------
    - **JSONResponse**: JSON response indicating the success or failure of the update.

    Raises
    ------
    - **HTTPException**:
        - **500** - If the update fails.
    """
    try:
        # Update the plant record in the Elasticsearch index
        response = es_client.update_document_by_id("plants", plant_id, plant_data)
        
        if response:
            return JSONResponse(
                status_code=200, 
                content={
                    "message": "Plant record updated successfully"
                })
        else:
            return JSONResponse(
                status_code=500, 
                content={
                    "message": "Failed to update plant record"
                })
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Plant record update failed - Internal Server Error: {str(e)}")


@router.delete("/{plant_id}")
async def delete_plant(plant_id: str) -> JSONResponse:
    """
    Delete a plant from plants index

    Parameters
    ----------
    - **plant_id**: (str) Plant id

    Returns
    -------
    - **JSONResponse**: JSON response indicating the success or failure of the deletion
    """
    response = es_client.delete_document_by_id(index="plants", document_id=plant_id)
    
    if response:
        return JSONResponse(
            status_code=200, 
            content={
                "message": "Plant deleted successfully"
            })
    else:
        return JSONResponse(
            status_code=404, 
            content={
                "message": "Plant not found or deletion failed"
            })