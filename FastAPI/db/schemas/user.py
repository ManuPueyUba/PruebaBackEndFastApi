# -*- coding: utf-8 -*-


def user_schema(user) -> dict:
    """
    Convert a user object to a dictionary.
    """
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "age": user["age"]
    }

def user_list_schema(user_list) -> list:
    """
    Convert a list of user objects to a list of dictionaries.
    """
    return [user_schema(user) for user in user_list]