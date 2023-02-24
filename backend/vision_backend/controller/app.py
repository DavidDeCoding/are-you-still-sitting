from fastapi import FastAPI
from pydantic import BaseModel

import os
from twilio.rest import Client

from vision_backend.services.user import User

stage = os.environ.get('STAGE', None)
openapi_prefix = f"/{stage}" if stage else "/"

app = FastAPI(title="Are you still sitting?",
              openapi_prefix=openapi_prefix)

class Payload(BaseModel):
    is_sitting: bool

@app.get("/health")
def health() -> int:
    return 1

@app.post("/sitting/{user_id}")
def sitting(user_id: str, payload: Payload) -> str:
    print("Here I am!")
    user = User.get_user_by_id(user_id)

    if not user:
        user = User(user_id, is_sitting)
    elif user.is_sitting != is_sitting:
        user.is_sitting = is_sitting
    else:
        return 'Success'
    
    user.save()
    
    return 'Success'