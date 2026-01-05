from src.models.entities.exercise import Exercise


class ExerciseRepository:
    def __init__(self, db_connection):
        """
        Initializes the repository with a database connection.
        :param db_connection: Instance of DbConnection
         used to execute SQL queries.
        """
        self.db = db_connection

    def get_all(self):
        """
        Retrieves all available exercises from the database.
        :return: List[Exercise]
        """
        conn = self.db.connect()
        cursor = conn.cursor()

        query = "SELECT id, name, category, description FROM exercises"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()

        results = []
        for row in rows:
            results.append(Exercise(row[1], row[2], row[3], row[0]))

        return results

    def create(self, exercise: Exercise):
        """
        Persists a new exercise entity to the database.

        :param exercise: Exercise entity object containing the data to insert.
        :return: int (The auto-generated ID of the new database row).
        """
        conn = self.db.connect()
        cursor = conn.cursor()

        query = "INSERT INTO exercises (name, category, description) VALUES (%s, %s, %s)"
        cursor.execute(query, (exercise.name, exercise.category, exercise.description))
        conn.commit()

        new_id = cursor.lastrowid
        cursor.close()
        return new_id