from src.models.entities.exercise import Exercise
from mysql.connector import Error


class ExerciseRepository:
    def __init__(self, db_connection):
        self.db = db_connection

    def get_all(self):
        """
        Retrieves all available exercises from the database.
        :return: List[Exercise]
        """
        conn = self.db.connect()
        cursor = conn.cursor()

        query = "SELECT id, name, category FROM exercises"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()

        results = []
        for row in rows:
            exercise_obj = Exercise(name=row[1],category=row[2],exercise_id=row[0])

            results.append(exercise_obj)

        return results

    def create(self, exercise: Exercise):
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            query = "INSERT INTO exercises (name, category) VALUES (%s, %s)"
            cursor.execute(query, (exercise.name, exercise.category))
            conn.commit()
        except Error as e:
            conn.rollback()
            raise RuntimeError(f"Database error during create exercise: {e}")
        finally:
            cursor.close()

        new_id = cursor.lastrowid
        cursor.close()
        return new_id

    def get_id_by_name(self, name):
        """
        Helper method for Import: Finds exercise ID based on its name.
        Case-insensitive search.
        """
        conn = self.db.connect()
        cursor = conn.cursor()

        query = "SELECT id FROM exercises WHERE LOWER(name) = %s"
        cursor.execute(query, (name.strip().lower(),))
        row = cursor.fetchone()
        cursor.close()

        if row:
            return row[0]
        return None

    def update_name(self, old_name, new_name):
        """
        Rename exercises.
        """
        conn = self.db.connect()
        cursor = conn.cursor()

        query = "UPDATE exercises SET name = %s WHERE name = %s"

        try:
            cursor.execute(query, (new_name, old_name))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise f"Update error: {e}"
        finally:
            cursor.close()