from fastapi import Depends, FastAPI, HTTPException, status
from index.dependencies import get_db
from index.router import router as index_router
from app.database import Base, sync_engine


Base.metadata.create_all(bind=sync_engine)

app = FastAPI()

app.include_router(index_router)


@app.get("/")
async def root():
    return {"message": "Ayush Connect API", "version": "0.1.0"}


@app.get("/healthcheck", status_code=status.HTTP_200_OK)
async def perform_healthcheck(db=Depends(get_db)):
    result = db.exec("SELECT 1")
    one = result.one()
    if not one[0] == 1:
        db_status = False
    else:
        db_status = True

    status = {}
    if not db_status:
        raise HTTPException(status_code=404, detail="db conn not available")
    elif db_status:
        status["operations"] = "ok"
    return status
