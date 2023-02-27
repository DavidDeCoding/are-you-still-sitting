from pydantic import BaseModel

import os

TWILIO_ACCOUNT_SID = os.environ['ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['AUTH_TOKEN']
APP_PHONE_NUMBER = os.environ['APP_PHONE_NUMBER']
USER_PHONE_NUMBER = os.environ['USER_PHONE_NUMBER']

account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN
client = Client(account_sid, auth_token)

class Caller(BaseModel):

    @staticmethod
    def make_call():
        call = client.calls.create(
                url="http://demo.twilio.com/docs/voice.xml",
                to=USER_PHONE_NUMBER,
                from_=APP_PHONE_NUMBER
            )
        return call