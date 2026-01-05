from datetime import date

class BodyMeasurement:
    def __init__(self, user_id, log_date, weight_kg, measurement_id=None):
        """
        Initializes the measurement entity and validates inputs.

        :param user_id: ID of the user (int).
        :param log_date: Date of the measurement (datetime.date).
        :param weight_kg: Weight value in kilograms (float/int).
        :param measurement_id: Database ID (optional, None for new records).
        """
        self._id = measurement_id
        # Voláme settery pro okamžitou validaci při vytváření objektu
        self.set_user_id(user_id)
        self.set_log_date(log_date)
        self.set_weight_kg(weight_kg)

    @property
    def id(self):
        """
        :return: The database ID of the record.
        """
        return self._id

    @property
    def user_id(self):
        return self._user_id

    def set_user_id(self, user_id):
        """
        Sets the owner of the record.
        :param user_id: Positive integer.
        :raises ValueError: If user_id is invalid.
        """
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("Invalid User ID.")
        self._user_id = user_id

    @property
    def log_date(self):
        return self._log_date

    def set_log_date(self, log_date):
        """
        Sets the date of the record.
        :param log_date: datetime.date object.
        Note: If an invalid type is passed, it defaults to date.today().
        """
        if not isinstance(log_date, date):
            self._log_date = date.today()
        else:
            self._log_date = log_date

    @property
    def weight_kg(self):
        return self._weight_kg

    def set_weight_kg(self, weight):
        """
        Sets the weight value.
        :param weight: float or int representing kilograms.
        """
        if not isinstance(weight, (int, float)):
            raise TypeError("Weight must be a number.")
        if weight <= 0 or weight > 500:
            raise ValueError("Weight looks invalid (must be between 0 and 500 kg).")
        self._weight_kg = float(weight)