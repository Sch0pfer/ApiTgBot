import json
import os

from User import User
from typing import List
from uuid import UUID

users: List[User] = []

def export_users_to_json(filename: str = "users.json") -> None:
    class UUIDEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, UUID):
                return str(obj)
            return super().default(obj)

    with open(filename, "w") as f:
        users_data = [user.model_dump() for user in users]
        json.dump({"users": users_data}, f, cls=UUIDEncoder)

def import_users_from_json(filename: str = "users.json") -> None:
    global users

    if os.path.getsize(filename) == 0:
        return

    with open(filename) as f:
        users_data = json.load(f)

        users.clear()

        for user_dict in users_data.values():
            for user in user_dict:
                for field, value in user.items():
                    if isinstance(value, str):
                        try:
                            user[field] = UUID(value)
                        except ValueError:
                            pass

            users.append(User(**user))