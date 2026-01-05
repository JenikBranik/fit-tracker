from mysql.connector import Error
from src.models.entities.user import User


class UserRepository:

    def __init__(self, db_connection):
        self.db = db_connection

    def create(self, user: User):
        """
        Create user entity to the database.
        :param user: The User entity instance to be saved.
        :return: int ID.
        """
        if not isinstance(user, User):
            raise TypeError("Object must be instance of User.")

        conn = self.db.connect()
        cursor = conn.cursor()

        query = "INSERT INTO users (username, email) VALUES (%s, %s)"
        values = (user.username, user.email)

        try:
            cursor.execute(query, values)
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            raise RuntimeError(f"Error: {e}")
        finally:
            cursor.close()

    def get_by_email(self, email: str):
        """
        Retrieves a user by their email address.
        :param email: The email address to search for.
        :return: User object or None.
        """
        conn = self.db.connect()
        cursor = conn.cursor()

        query = "SELECT id, username, email FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        row = cursor.fetchone()
        cursor.close()

        if row:
            return User(username=row[1], email=row[2], user_id=row[0])

        return None