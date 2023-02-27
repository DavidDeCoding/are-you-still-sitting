from __future__ import annotations
from pydantic import BaseModel

import boto3
import os

from boto3.dynamodb.conditions import Key, Attr

VISION_TABLE = os.environ['VISION_TABLE']

db_client = boto3.client('dynamodb')

class User(BaseModel):
    user_id: str
    is_sitting: bool
    timestamp: int
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
                     notified=item['notified']['BOOL']) for item in result['Items']]

    def save(self):
        db_client.put_item(
            TableName=VISION_TABLE,
            Item={
                'userId': {'S': self.user_id},
                'isSitting': {'BOOL': self.is_sitting},
                'timestamp': {'N': str(self.timestamp)},
                'notified': {'BOOL': self.notified}
            }
        )