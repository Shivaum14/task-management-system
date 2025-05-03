from sqlalchemy.orm import Session

from app.models.user import User


def get_or_create_user(session: Session, sub: str, email: str, name: str) -> User:
    user = session.query(User).filter(User.auth0_id == sub).first()
    if user:
        return user
    return create_user(session, sub, email, name)


def create_user(session: Session, auth0_id: str, email: str, name: str) -> User:
    user = User(
        auth0_id=auth0_id,
        email=email,
        name=name,
        created_by="anonymous@example.com",
        updated_by="anonymous@example.com",
    )
    session.add(user)
    session.commit()
    return user
