import logging
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.services import user as user_service
from app.schemas.user import UserCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    db = SessionLocal()
    create_first_superuser(db)
    db.close()


def create_first_superuser(db: Session) -> None:
    user = user_service.get_by_email(db, email="admin@example.com")
    if not user:
        user_in = UserCreate(
            email="admin@example.com",
            username="admin",
            password="admin123",  # Change this in production!
            is_superuser=True,
        )
        user = user_service.create(db, obj_in=user_in)
        logger.info(f"Superuser created: {user.email}")
    else:
        logger.info(f"Superuser already exists: {user.email}")


if __name__ == "__main__":
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")
