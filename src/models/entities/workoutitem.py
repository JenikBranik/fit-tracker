class WorkoutItem:
    def __init__(self, exercise_id, sets, reps, weight_kg, item_id=None, workout_id=None):
        """
        Initializes the WorkoutItem and validates input data.
        :param exercise_id: ID of the exercise being performed.
        :param sets: Number of sets.
        :param reps: Number of repetitions per set.
        :param weight_kg: Weight used in kg.
        :param item_id: Database ID of this item.
        :param workout_id: ID of the parent workout header.
        """
        self._id = item_id
        self._workout_id = workout_id

        self.set_exercise_id(exercise_id)
        self.set_sets(sets)
        self.set_reps(reps)
        self.set_weight_kg(weight_kg)

    @property
    def id(self):
        """
        :return: The database ID of the workout item.
        """
        return self._id

    @property
    def workout_id(self):
        return self._workout_id

    @workout_id.setter
    def workout_id(self, val):
        """
        Sets the ID of the parent workout.
        :param val: Workout ID (int).
        """
        self._workout_id = val

    @property
    def exercise_id(self):
        return self._exercise_id

    def set_exercise_id(self, exercise_id):
        """
        Sets the ID of the exercise.
        :param exercise_id: Positive integer.
        """
        if not isinstance(exercise_id, int):
            raise TypeError("Exercise ID must be an integer.")
        if exercise_id <= 0:
            raise ValueError("Exercise ID must be positive.")
        self._exercise_id = exercise_id

    @property
    def sets(self):
        return self._sets

    def set_sets(self, sets):
        """
        Sets the number of sets.
        :param sets: Integer greater than 0.
        """
        if not isinstance(sets, int):
            raise TypeError("Sets must be an integer.")
        if sets <= 0:
            raise ValueError("Sets count must be at least 1.")
        self._sets = sets

    @property
    def reps(self):
        return self._reps

    def set_reps(self, reps):
        """
        Sets the number of repetitions.
        :param reps: Integer greater than 0.
        """
        if not isinstance(reps, int):
            raise TypeError("Reps must be an integer.")
        if reps <= 0:
            raise ValueError("Reps count must be at least 1.")
        self._reps = reps

    @property
    def weight_kg(self):
        return self._weight_kg

    def set_weight_kg(self, weight):
        """
        Sets the weight used.
        :param weight: Float or int (kg).
        """
        if not isinstance(weight, (int, float)):
            raise TypeError("Weight must be a number.")
        if weight < 0:
            raise ValueError("Weight cannot be negative.")
        self._weight_kg = float(weight)

    def __str__(self):
        return f"{self.sets}x{self.reps} ({self.weight_kg} kg)"