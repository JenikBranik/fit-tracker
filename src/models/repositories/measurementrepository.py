from src.models.entities.bodymeasurement import BodyMeasurement
from mysql.connector import Error

class MeasurementRepository:
    def __init__(self, db_connection):
        self.db = db_connection

    def create(self, measurement: BodyMeasurement):
        """
        Persists a new body measurement entity to the database.

        :param measurement: BodyMeasurement entity containing user_id, date, and weight.
        :return: int (The unique ID of the newly inserted record).
        """
        conn = self.db.connect()
        cursor = conn.cursor()
        query = "INSERT INTO body_measurements (user_id, log_date, weight_kg) VALUES (%s, %s, %s)"
        try:
            cursor.execute(query, (measurement.user_id, measurement.log_date, measurement.weight_kg))
            conn.commit()
            new_id = cursor.lastrowid
            return new_id
        except Error as e:
            conn.rollback()
            raise RuntimeError(f"Database error during measurement create: {e}")
        finally:
            cursor.close()

    def get_by_user(self, user_id):
        """
        Retrieves the complete weight logs for a specific user.
        :param user_id: The ID of the user whose history is being requested.
        :return: List[BodyMeasurement]
        """
        conn = self.db.connect()
        cursor = conn.cursor()

        query = ("SELECT id, user_id, log_date, weight_kg "
                 "FROM body_measurements "
                 "WHERE user_id = %s "
                 "ORDER BY log_date DESC")
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()
        cursor.close()

        measurements = []
        for row in rows:
            m = BodyMeasurement(
                user_id=row[1],
                log_date=row[2],
                weight_kg=row[3],
                measurement_id=row[0]
            )
            measurements.append(m)
        return measurements

    def delete_by_date(self, user_id, date_str):
        """
        Delete weight
        :param date_str: Date in formate 'YYYY-MM-DD'
        """
        conn = self.db.connect()
        cursor = conn.cursor()

        query = "DELETE FROM body_measurements WHERE user_id = %s AND log_date = %s"

        try:
            cursor.execute(query, (user_id, date_str))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise f"Delete error: {e}"
        finally:
            cursor.close()