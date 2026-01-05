import re

class User:
    def __init__(self, username, email, user_id=None):
        """
        Initializes the User entity.
        :param username: String, minimum 3 characters.
        :param email: String, must be a valid email format.
        :param user_id: Database ID (optional, None for new users).
        """
        self._id = user_id
        self.set_username(username)
        self.set_email(email)

    @property
    def id(self):
        """
        :return: The unique database ID of the user.
        """
        return self._id

    @property
    def username(self):
        return self._username

    def set_username(self, username):
        """
        Sets and validates the username.
        :param username: String, must be at least 3 characters long.
        """
        if not isinstance(username, str):
            raise TypeError("Username must be a string.")
        if not username.strip():
            raise ValueError("Username cannot be empty.")
        if len(username) < 3:
            raise ValueError("Username is too short (min 3 chars).")
        self._username = username.strip()

    @property
    def email(self):
        return self._email

    def set_email(self, email):
        """
        Sets and validates the email address using Regex.
        :param email: String in a valid email format.
        """
        if not isinstance(email, str):
            raise TypeError("Email must be a string.")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError(f"Invalid email format: {email}")
        self._email = email.strip()