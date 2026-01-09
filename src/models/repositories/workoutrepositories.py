from mysql.connector import Error
from src.models.entities.workoutitem import WorkoutItem
from src.models.entities.workout import Workout


class WorkoutRepository:
    def __init__(self, db_connection):
        if db_connection is None:
            raise ValueError("Database connection cannot be None")
        self.db = db_connection

    def create_workout(self, user_id, note, start_time):
        """
        Creates a new workout header (session) in the database.
        :param user_id: ID of the user owning the workout.
        :param note: Optional text note regarding the workout.
        :param start_time: Datetime object indicating when the workout started.
        :return: int (The unique ID of the newly created workout).
        """
        conn = self.db.connect()
        cursor = conn.cursor()

        sql = "INSERT INTO workouts (user_id, start_time, note) VALUES (%s, %s, %s)"
        vals = (user_id, start_time, note)

        try:
            cursor.execute(sql, vals)
            conn.commit()
            new_id = cursor.lastrowid
            return new_id
        except Error as e:
            conn.rollback()
            raise RuntimeError(f"Database error when creating workout header: {e}")
        finally:
            cursor.close()

    def add_workout_item(self, workout_id, item: WorkoutItem):
        """
        specific exercise set to an existing workout.
        :param workout_id: The ID of the parent workout header.
        :param item: WorkoutItem entity containing specifics.
        """
        if not isinstance(item, WorkoutItem):
            raise TypeError("Expected WorkoutItem entity.")

        conn = self.db.connect()
        cursor = conn.cursor()

        sql = """
              INSERT INTO workout_items (workout_id, exercise_id, sets, reps, weight_kg, is_warmup)
              VALUES (%s, %s, %s, %s, %s, %s) \
              """
        vals = (
            workout_id,
            item.exercise_id,
            item.sets,
            item.reps,
            item.weight_kg,
            item.is_warmup
        )

        try:
            cursor.execute(sql, vals)
            conn.commit()
        except Error as e:
            conn.rollback()
            raise RuntimeError(f"Database error when inserting item: {e}")
        finally:
            cursor.close()

    def get_items_by_workout_id(self, workout_id):
        """
        Retrieves all raw items associated with a specific workout.
        Maps database rows back to WorkoutItem entities.
        :param workout_id: ID of the workout.
        :return: List[WorkoutItem]
        """
        conn = self.db.connect()
        cursor = conn.cursor()

        sql = ("SELECT exercise_id, sets, reps, weight_kg, is_warmup, id "
               "FROM workout_items "
               "WHERE workout_id = %s")

        try:
            cursor.execute(sql, (workout_id,))
            rows = cursor.fetchall()

            results = []
            for row in rows:
                item = WorkoutItem(
                    exercise_id=row[0],
                    sets=row[1],
                    reps=row[2],
                    weight_kg=row[3],
                    is_warmup=bool(row[4]),
                    item_id=row[5]
                )
                results.append(item)
            return results

        except Error as e:
            raise RuntimeError(f"Database fetch error: {e}")
        finally:
            cursor.close()

    def get_all_by_user(self, user_id):
        """
        Retrieves the history of workout sessions for a user.
        The list is ordered by date descending.
        :param user_id: ID of the user.
        :return: List[Workout]
        """
        conn = self.db.connect()
        cursor = conn.cursor()

        query = ("SELECT id, user_id, start_time, note "
                 "FROM workouts "
                 "WHERE user_id = %s "
                 "ORDER BY start_time DESC")
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()
        cursor.close()

        workouts = []
        for row in rows:
            w = Workout(row[1], row[2], row[3], row[0])
            workouts.append(w)

        return workouts

    def get_items_with_names(self, workout_id):
        """
        Retrieves workout items enriched with exercise names from a VIEW.
        :param workout_id: ID of the workout.
        :return: List[dict]
        """
        conn = self.db.connect()
        cursor = conn.cursor()

        sql = """
              SELECT exercise_name, sets, reps, weight_kg, is_warmup
              FROM workout_details
              WHERE workout_id = %s
              """

        cursor.execute(sql, (workout_id,))
        rows = cursor.fetchall()
        cursor.close()

        results = []
        for row in rows:
            results.append({
                "exercise_name": row[0],
                "sets": row[1],
                "reps": row[2],
                "weight": row[3],
                "is_warmup": bool(row[4])
            })
        return results

    def save_complete_workout(self, user_id, start_time, note, items):
        """
        TRANSAKČNÍ METODA (Splňuje zadání):
        Uloží hlavičku tréninku (tabulka 'workouts') a všechny jeho položky
        (tabulka 'workout_items') jako jednu atomickou operaci.
        """
        conn = self.db.connect()
        conn.autocommit = False
        cursor = conn.cursor()

        try:
            sql_header = "INSERT INTO workouts (user_id, start_time, note) VALUES (%s, %s, %s)"
            cursor.execute(sql_header, (user_id, start_time, note))

            new_workout_id = cursor.lastrowid

            sql_item = """
                       INSERT INTO workout_items (workout_id, exercise_id, sets, reps, weight_kg, is_warmup)
                       VALUES (%s, %s, %s, %s, %s, %s) \
                       """

            for item in items:
                if not isinstance(item, WorkoutItem):
                    raise TypeError("Item must be of type WorkoutItem")

                vals = (
                    new_workout_id,
                    item.exercise_id,
                    item.sets,
                    item.reps,
                    item.weight_kg,
                    item.is_warmup
                )
                cursor.execute(sql_item, vals)

            conn.commit()
            return new_workout_id

        except Error as e:
            conn.rollback()
            raise RuntimeError(f"Transaction failed (Full Workout Save): {e}")

        finally:
            cursor.close()
            conn.autocommit = True