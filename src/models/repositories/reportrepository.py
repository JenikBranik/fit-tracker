from mysql.connector import Error

class ReportRepository:
    def __init__(self, db_connection):
        self.db = db_connection

    def get_user_summary(self, user_id):
        """
        Fetches data from 'user_summary' view.
        Returns a dictionary with keys: user_id, username, total_workouts, current_weight_kg.
        """
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM user_summary WHERE user_id = %s"

        try:
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            return result
        except Error as e:
            raise f"Error: {e}"
        finally:
            cursor.close()
