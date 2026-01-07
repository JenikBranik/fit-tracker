from src.models.entities.exercise import Exercise


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
            exercise_obj = Exercise(
                name=row[1],
                category=row[2],
                exercise_id=row[0]
            )

            results.append(exercise_obj)

        return results

    def create(self, exercise: Exercise):
        conn = self.db.connect()
        cursor = conn.cursor()

        query = "INSERT INTO exercises (name, category) VALUES (%s, %s)"
        cursor.execute(query, (exercise.name, exercise.category))
        conn.commit()

        new_id = cursor.lastrowid
        cursor.close()
        return new_id