import uuid


def is_uuid_valid(uuid_: str) -> bool:
    try:
        uuid.UUID(uuid_)
        return True
    except ValueError:
        return False
