from typing import List, Optional

from sqlalchemy import exists, select
from sqlalchemy.orm import Session

from app.api.schemas.board import BoardCreate
from app.models import Board


def create_board(session: Session, board_in: BoardCreate) -> Board:
    db_board = Board(title=board_in.title, owner="anonymous@example.com")  # Owner will come from Auth later
    session.add(db_board)
    session.commit()
    return db_board


def get_boards(session: Session) -> List[Board]:
    query = select(Board)
    return session.execute(query).scalars().all()


def get_board_by_uid(session: Session, uid: str) -> Optional[Board]:
    query = select(Board).where(Board.uid == uid)
    return session.execute(query).scalar_one_or_none()


def board_exists(session: Session, uid: str) -> bool:
    query = select(exists().where(Board.uid == uid))
    return session.execute(query).scalar()
