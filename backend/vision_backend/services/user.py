from __future__ import annotations
from pydantic import BaseModel

import boto3
import os
import datetime

from boto3.dynamodb.conditions import Key, Attr

VISION_TABLE = os.environ['VISION_TABLE']

db_client = boto3.client('dynamodb')
cognito_client = boto3.client('cognito-idp')

class User(BaseModel):
    user_id: str
    is_sitting: bool
    timestamp: int
    phone: str
    notified: bool

    @staticmethod
    def get_user_by_id(user_id: str) -> User:
        result = db_client.query(
            TableName=VISION_TABLE,
            KeyConditionExpression='userId = :userId',
            ExpressionAttributeValues={
                ':userId': {'S': user_id}
            }
        )

        if not result['Items'] or not len(result['Items']):
            return None
        
        result = result['Items'][0]

        return User(user_id=result['userId']['S'],
                    is_sitting=result['isSitting']['BOOL'],
                    timestamp=result['timestamp']['N'],
                    phone=result['phone']['S'],
                    notified=result['notified']['BOOL'])

    @staticmethod
    def get_user_by_sitting() -> List[User]:
        result = db_client.scan(
            TableName=VISION_TABLE,
            FilterExpression='isSitting = :isSitting',
            ExpressionAttributeValues={
                ':isSitting': {'BOOL': True}
            }
        )

        if not result['Items'] or not len(result['Items']):
            return []
        
        return [User(user_id=item['userId']['S'], 
                     is_sitting=item['isSitting']['BOOL'],
                     timestamp=item['timestamp']['N'],
                     phone=item['phone']['S'],
                     notified=item['notified']['BOOL']) for item in result['Items']]

    @staticmethod
    def get_user_by_access_token(access_token: str) -> User:
        response = cognito_client.get_user(AccessToken=access_token)

        user = User.get_user_by_id(response['Username'])

        if not user:
            timestamp = str(int(datetime.datetime.utcnow().timestamp()))

            user = User(user_id=response['Username'],
                        is_sitting=False,
                        timestamp=timestamp,
                        phone='',
                        notified=False)
            user.save()
        
        return user

    def save(self):
        db_client.put_item(
            TableName=VISION_TABLE,
            Item={
                'userId': {'S': self.user_id},
                'isSitting': {'BOOL': self.is_sitting},
                'timestamp': {'N': str(self.timestamp)},
                'phone': {'S': self.phone},
                'notified': {'BOOL': self.notified}
            }
        )