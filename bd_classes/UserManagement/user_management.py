from bd_classes.tables.UserTable import UserTable


class UserManagement:
    def __init__(self, session):
        self.session = session

    def create_new_user(self, user_id, user_name, user_photo_path) -> bool:
        if self.find_user_by_id(user_id):
            return False

        new_user = UserTable(
            user_id=user_id,
            user_name=user_name,
            user_photo_path=user_photo_path
        )

        self.session.add(new_user)
        self.session.commit()

        return True

    def find_user_by_id(self, user_id):
        user = self.session.query(UserTable).filter(UserTable.user_id == user_id).first()
        return user

