from datetime import datetime

class Workout:
    def __init__(self, user_id, start_time, note="", workout_id=None):
        """
        Initializes the Workout entity and performs immediate validation.
        :param user_id: ID of the user who performed the workout.
        :param start_time: datetime object indicating when the workout started.
        :param note: Optional text note (max 255 chars).
        :param workout_id: Database ID (optional, None for new records).
        """
        self._id = workout_id
        self.set_user_id(user_id)
        self.set_start_time(start_time)
        self.set_note(note)

    @property
    def id(self):
        """
        :return: The database ID of the workout.
        """
        return self._id

    @property
    def user_id(self):
        return self._user_id

    def set_user_id(self, user_id):
        """
        Sets the user ID.
        :param user_id: Positive integer.
        :raises TypeError: If user_id is not an integer.
        :raises ValueError: If user_id is not positive.
        """
        if not isinstance(user_id, int):
            raise TypeError("User ID must be an integer.")
        if user_id <= 0:
            raise ValueError("User ID must be positive.")
        self._user_id = user_id

    @property
    def start_time(self):
        return self._start_time

    def set_start_time(self, start_time):
        """
        Sets the workout start time.
        :param start_time: datetime object.
        :raises TypeError: If input is not a datetime object.
        :raises ValueError: If the date is in the future.
        """
        if not isinstance(start_time, datetime):
            raise TypeError("Start time must be a datetime object.")
        if start_time > datetime.now():
             raise ValueError("Workout cannot be in the future.")
        self._start_time = start_time

    @property
    def note(self):
        return self._note

    def set_note(self, note):
        """
        Sets the optional note.
        :param note: String, max 255 chars.
        :raises TypeError: If note is not a string.
        :raises ValueError: If note is too long.
        """
        if note is None:
            note = ""
        if not isinstance(note, str):
            raise TypeError("Note must be a string.")
        if len(note) > 255:
            raise ValueError("Note is too long (max 255 chars).")
        self._note = note.strip()

    def __str__(self):
        return f"Workout [{self.start_time}] - {self.note}"