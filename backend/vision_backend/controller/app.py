from typing import Union

from fastapi import FastAPI, Header, Request
from pydantic import BaseModel

import os
import datetime
from twilio.rest import Client

from vision_backend.services.user import User

stage = os.environ.get('STAGE', None)
openapi_prefix = f"/{stage}" if stage else "/"

app = FastAPI(title="Are you still sitting?",
              openapi_prefix=openapi_prefix)

class InitPayload(BaseModel):
    phone: str

@app.get("/web/health")
def health() -> int:
    return 1

class InitPayload(BaseModel):
    phone: str

@app.post("/web/init")
def init(payload: InitPayload,
         authorization: Union[str, None] = Header(default=None)) -> str:
    
    user = User.get_user_by_access_token(authorization)
    user.phone = payload.phone
    user.save()

    return 'Success'

class SittingPayload(BaseModel):
    is_sitting: bool

@app.post("/web/sitting")
def sitting(payload: SittingPayload,
            authorization: Union[str, None] = Header(default=None)) -> str:

    timestamp = str(int(datetime.datetime.utcnow().timestamp()))

    user = User.get_user_by_access_token(authorization)
    user.timestamp = timestamp
    user.is_sitting = payload.is_sitting
    user.notified = False
    user.save()
    
    return 'Success'