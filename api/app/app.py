from fastapi import FastAPI

from app.routers import processing
from app.database.models import Base
from app.database.db_admin import engine


Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(processing.router)