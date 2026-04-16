from sqlalchemy.orm import Session
from fastapi_users.password import PasswordHelper
from fastkit_core.database import get_db_manager, Repository, init_database
from fastkit_core.config import ConfigManager
from app.models import User

configuration = ConfigManager(modules=['database', 'auth'])
password_helper = PasswordHelper()

def seed_admin_user(session: Session) -> User:
    repository = Repository(User, session)

    admin = repository.filter_one(email=configuration.get('auth.ADMIN_EMAIL'))

    if admin:
        print("✓ Admin user already exists")
        return admin

    return repository.create({
        'email': configuration.get('auth.ADMIN_EMAIL'),
        'hashed_password': password_helper.hash(configuration.get('auth.ADMIN_PASSWORD')),
        'is_active': True,
        'is_superuser': True,
        'is_verified': True
    })



if __name__ == "__main__":
    init_database(configuration)
    db_manager = get_db_manager()

    with db_manager.session() as session:
        seed_admin_user(session)