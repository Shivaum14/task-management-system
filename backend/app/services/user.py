from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User


def get_or_create_user(session: Session, sub: str, email: str, name: str) -> User:
    user = session.query(User).filter(User.auth0_id == sub).first()
    if user:
        return user
    return create_user(session, None, sub, email, name)


def create_user(session: Session, owner: Optional[User], auth0_id: str, email: str, name: str) -> User:
    owner_email = owner.email if owner is not None else email
    user = User(
        email=email,
        auth0_id=auth0_id,
        name=name,
        created_by=owner_email,
        updated_by=owner_email,
    )
    session.add(user)
    session.commit()
    return user
