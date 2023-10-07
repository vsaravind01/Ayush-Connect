from fastapi import APIRouter, Body, Depends, Query
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from app.index.models import PlantIndex
from app.index.utils.es import ElasticSearchClient
from app.index.schemas import PlantIndexCreate
from app.index.dependencies import get_db
from app.index.plants.router import router as plant_router

es_client = ElasticSearchClient()

router = APIRouter(prefix="/index", tags=["index"])

router.include_router(plant_router)

@router.get("/")
async def get_indices() -> JSONResponse:
    """
    Get all elasticsearch indices

    Returns
    -------
    - **JSONResponse**: JSON response with all indices
    """
    indices = es_client.get_indices()
    return JSONResponse(status_code=200, content=indices)


@router.post("/")
async def create_index(
        index: PlantIndexCreate, db=Depends(get_db)) -> JSONResponse:
    """
    Create elasticsearch index for given index name

    Parameters
    ----------
    - **index**: (PlantIndexCreate) Index details
        - **index_name**: Name of the index to be created
        - **description**: Description of the index to be created
        - **alias**: Alias of the index to be created
    **db**: (Session) Database session

    Returns
    -------
    - **JSONResponse**: JSON response with status of the index creation

    Raises
    ------
    - **HTTPException**
        - **409** - If index already exists
        - **500** - If index creation fails
    """
    if es_client.create_index(index.index_name):
        try:
            plant_idx = PlantIndex(index_name=index.index_name,
                       description=index.description)
            db.add(plant_idx)
            db.commit()
            db.refresh(PlantIndex)
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Index creation failed - Internal Server Error")
        return JSONResponse(
            status_code=201,
            content={
                "message": f"Index - '{index.index_name}' created successfully"
            })


@router.delete("/{index_name}")
async def delete_index(index_name: str, db=Depends(get_db)) -> JSONResponse:
    """
    Delete elasticsearch index for given index name

    Parameters
    ----------
    - **index_name**: (str) Name of the index to be deleted
    - **db**: (Session) Database session

    Returns
    -------
    - **JSONResponse**: JSON response with status of the index deletion

    Raises
    ------
    - **HTTPException**
        - **404** - If index does not exist
        - **500** - If index deletion fails
    """
    if es_client.delete_index(index_name):
        try:
            db.query(PlantIndex).filter(
                PlantIndex.index_name == index_name).delete()
            return JSONResponse(
                status_code=200,
                content={
                    "message": f"Index - '{index_name}' deleted successfully"
                })
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Index deletion failed - Internal Server Error")


@router.put("/{index_name}")
async def update_index(
        index_name: str,
        description: str = Body(None),
        alias: str = Body(None),
        db=Depends(get_db)
) -> JSONResponse:
    """
    Update elasticsearch index for given index name

    Parameters
    ----------
    - **index_name**: (str) Name of the index to be updated
    - **description**: (str) Description of the index to be updated
    - **alias**: (str) Alias of the index to be updated
    - **db**: (Session) Database session

    Returns
    -------
    - **JSONResponse**: JSON response with status of the index update

    Raises
    ------
    - **HTTPException**
        - **404** - If index does not exist
        - **500** - If index update fails
    """
    if es_client.index_exists(index_name):
        try:
            if description and alias:
                update_dict = {"description": description, "alias": alias}
            elif description:
                update_dict = {"description": description}
            elif alias:
                update_dict = {"alias": alias}
            else:
                raise HTTPException(status_code=400,
                                    detail="Description or alias is required")
            db.query(PlantIndex).filter(
                PlantIndex.index_name == index_name).update(update_dict)
            return JSONResponse(
                status_code=200,
                content={
                    "message": f"Index - '{index_name}' updated successfully"
                })
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Index update failed - Internal Server Error")
    else:
        raise HTTPException(status_code=404,
                            detail=f"Index - '{index_name}' does not exists")


@router.get("/{index_name}/search")
async def search_index(
        index_name: str, field: str = Query(None), query: str = Query(None)
) -> JSONResponse:
    """
    Search elasticsearch index for given index name and query

    Parameters
    ----------
    - **index_name**: (str) Name of the index to be searched
    - **field**: (str) Field to be searched
    - **query**: (str) Query to be searched

    Returns
    -------
    - **JSONResponse**: JSON response with search results

    Raises
    ------
    - **HTTPException**
        - **400** - If field or query is not provided
        - **404** - If index does not exist
        - **500** - If search fails
    """
    if not field or not query:
        raise HTTPException(status_code=400,
                            detail="Field and query are required")

    if es_client.index_or_alias_exists(index_name):
        try:
            q = {"query": {"match": {field: query}}}
            results = es_client.search_document(index_name, q)
            return JSONResponse(status_code=200, content=results)
        except Exception:
            raise HTTPException(status_code=500,
                                detail="Search failed - Internal Server Error")
    else:
        raise HTTPException(status_code=404,
                            detail=f"Index - '{index_name}' does not exists")
