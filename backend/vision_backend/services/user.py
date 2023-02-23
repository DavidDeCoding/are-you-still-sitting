from pydantic import BaseModel

import boto3

VISION_TABLE = os.environ['VISION_TABLE']

db_client = boto3.client('dynamodb')

class User(BaseModel):
    user_id: str
    is_sitting: bool

    @staticmethod
    def get_user_by_id(user_id: str) -> User:
        result = db_client.query(
            TableName=VISION_TABLE,
            KeyConditionExpression='userId = :userId',
            ExpressionAttributeValues={
                ':userId': {'S': user_id}
            }
        )

        if not result['Items'] and not len(result['Items']):
            return None
        
        result = result['Items'][0]

        return User(user_id=result['userId']['S'],
                    is_sitting: result['isSitting']['S'])


    def save():
        db_client.put_item(
            TableName=COUPONS_TABLE,
            Item={
                'userId': {'S': user_id},
                'isSitting': {'S': is_sitting}
            }
        )