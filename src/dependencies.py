from sqlalchemy.orm import Session

from src.database import ENGINE


def get_session():
    session = Session(ENGINE)
    try:
        yield session

    except Exception as e:
        session.rollback()
        raise

    finally:
        session.close()
