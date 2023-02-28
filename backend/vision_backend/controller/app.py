from typing import Union

from fastapi import FastAPI, Header
from pydantic import BaseModel

import os
import datetime
from twilio.rest import Client

from vision_backend.services.user import User

stage = os.environ.get('STAGE', None)
openapi_prefix = f"/{stage}" if stage else "/"

app = FastAPI(title="Are you still sitting?",
              openapi_prefix=openapi_prefix)

class Payload(BaseModel):
    phone: str
    is_sitting: bool

@app.get("/health")
def health() -> int:
    return 1

@app.post("/init")
def init(authorization: Union[str, None] = Header(default=None),
         payload: Payload) -> str:
    user_details = User.get_details(authorization)
    user_id = user_details['username']

    timestamp = str(int(datetime.datetime.utcnow().timestamp()))

    user = User(user_id=user_id,
                is_sitting=False,
                timestamp=timestamp,
                phone=payload.phone,
                notified=False)
    user.save()

    return 'Success'

@app.post("/sitting")
def sitting(authorization: Union[str, None] = Header(default=None), 
            payload: Payload) -> str:

    user_details = User.get_details(authorization)
    user_id = user_details['username']

    timestamp = str(int(datetime.datetime.utcnow().timestamp()))
    
    user = User.get_user_by_id(user_id)
    user.timestamp = timestamp
    user.is_sitting = payload.is_sitting
    user.notified = False
    
    user.save()
    
    return 'Success'