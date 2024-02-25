from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sys import exit

from ServiceLocator import ServiceLocator
from bd_classes.PointOnTheMapManagement.point_on_the_map_management import PointOnTheMapManagement
from bd_classes.UserManagement.user_management import UserManagement
from get_cred import get_cred


def session_initialization():
    cred = get_cred()
    db_name = cred.get("DB_NAME")
    db_user = cred.get("DB_USER")
    db_password = cred.get("DB_PASSWORD")
    db_host = cred.get("DB_HOST")
    db_port = cred.get("DB_PORT")

    if not any([db_name, db_user, db_password, db_host]):
        exit("Some bd cred lost")

    database_uri = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    engine = create_engine(database_uri)

    Session = sessionmaker(bind=engine)
    session = SessionManager(Session())

    ServiceLocator.register_service("session", session)


class SessionManager:
    def __init__(self, session):
        self.user_management = UserManagement(session)
        self.point_on_the_map_management = PointOnTheMapManagement(session)

    def create_new_user(self, user_id, user_name, user_photo_path):
        return self.user_management.create_new_user(user_id, user_name, user_photo_path)

    def find_user_by_id(self, user_id):
        return self.user_management.find_user_by_id(user_id)