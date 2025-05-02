import uuid


def generate_uid() -> str:
    """Generate a unique identifier."""
    return uuid.uuid4().hex
