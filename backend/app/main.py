from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import text
from app.index.dependencies import get_db
from app.index.router import router as index_router
from app.database import Base, sync_engine, SessionLocal
from app.index.utils.es import ElasticSearchClient
from app.index.models import PlantIndex

es_client = ElasticSearchClient()

Base.metadata.create_all(bind=sync_engine)

app = FastAPI()

app.include_router(index_router)


@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    # add existing elasticsearch indices to database (plant_idx table)
    indices = es_client.get_indices()
    db_indices = db.query(PlantIndex).all()
    db_indices = [index.index_name for index in db_indices]

    for index in indices:
        if index not in db_indices:
            try:
                idx_uuid = es_client.get_index_uuid(index)
                plant_idx = PlantIndex(idx_uuid=idx_uuid,
                                       index_name=index,
                                       description=f"Initialized '{index}'")
                db.add(plant_idx)
                db.commit()
            except Exception as e:
                print(e)
    db.close()


@app.get("/")
async def root():
    return {"message": "Ayush Connect API", "version": "0.1.0"}


@app.get("/healthcheck", status_code=status.HTTP_200_OK)
async def perform_healthcheck(db=Depends(get_db)):
    result = db.execute(text("SELECT 1"))
    one = result.one()
    if not one[0] == 1:
        db_status = False
    else:
        db_status = True

    _status = {}
    if not db_status:
        raise HTTPException(status_code=404, detail="db conn not available")
    elif db_status:
        _status["operations"] = "ok"
    return _status
