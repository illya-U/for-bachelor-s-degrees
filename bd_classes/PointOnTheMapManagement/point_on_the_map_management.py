from bd_classes.tables.PointOnTheMap import PointOnTheMapTable


class PointOnTheMapManagement:
    def __init__(self, session):
        self.session = session

    def add_point(self, user_id, location, description, photo_path):

        new_report = PointOnTheMapTable(
            photo_path=photo_path,
            latitude=location.get("latitude", 0),
            longitude=location.get("longitude", 0),
            message=description,
            user_id=user_id
        )

        self.session.add(new_report)
        self.session.commit()

