import secrets, json
import time
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import crud, models, schemas
from database import SessionLocal, engine
from sqlalchemy.orm import Session

app = FastAPI()
security = HTTPBasic()
http_scheme = HTTPBearer()

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

origins = [
    "*",
    "http://localhost:8000",
    "http://localhost:8001",
    "http://localhost:8002",
    "http://localhost:8003",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def auth_required(db: Session, bearer: HTTPBearer):
    if(not crud.verify_access_token(db,bearer.credentials)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Access Token",
    )

# class LoginForm(BaseModel):
#     email: str
#     password: str
@app.post("/login", status_code=200)
async def login(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    if(crud.verify_password(db,credentials.username,credentials.password)):
        access_token = crud.create_access_token(db,credentials.username)
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Basic"},
    )


@app.post("/ships/log")
async def save_ship_log(log: schemas.ShipLogBase, token: bool = Depends(http_scheme), db: Session = Depends(get_db)):
    auth_required(db, token)
    status = crud.save_ship_log(db, log)
    return {"status": status}

@app.get("/shiplogs")
async def ship_logs(offset : int = 0, rows : int = 100, timestep : int = 1, group_id : int = -1, token: bool = Depends(http_scheme), db: Session = Depends(get_db)):
    start_time = time.time()
    auth_required(db, token)
    logs = crud.get_ship_logs(db,0,rows, timestep, group_id)
    process_time = time.time() - start_time
    print(process_time)
    return logs

@app.get("/shiplogs/realtime")
async def ship_logs(rows : int = 100, token: bool = Depends(http_scheme), db: Session = Depends(get_db)):
    auth_required(db, token)
    logs = crud.get_realtime_ship_logs(db,rows)
    return logs

@app.get("/shiplogs/groups")
async def ship_logs(token: bool = Depends(http_scheme), db: Session = Depends(get_db)):
    auth_required(db, token)
    groups = crud.get_ship_log_groups(db)
    return groups


class PingPong(BaseModel):
    access_token: str
@app.post("/ping")
async def ping(pingPong: PingPong, token: bool = Depends(http_scheme)):
    auth_required(db, token)
    return "pong"

#user = crud.create_user(SessionLocal(),"oliver.olmaru@gmail.com","Oliver","123456")
#print(user)