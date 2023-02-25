from vision_backend.services.user import User
from datetime import datetime

def process(event, context):
    now = datetime.utcnow()

    users = User.get_user_by_sitting()
    for user in users:
        last_sitting_time = datetime.fromtimestamp(user.timestamp)
        delta_in_mins = (now - last_sitting_time).total_seconds() // 60
        print(f'User {user.user_id} sitting for {delta_in_mins} mins.')
        if int(delta_in_mins) > 30:
            print(f'User {user.user_id} has been sitting for more than 30 mins.')