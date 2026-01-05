class Exercise:
    VALID_CATEGORIES = {'Strength', 'Cardio', 'Flexibility'}
    def __init__(self, name, category, description="", exercise_id=None):
        """
        Initializes the Exercise entity.
        :param name: Name of the exercise (max 100 chars).
        :param category: One of 'Strength', 'Cardio', 'Flexibility'.
        :param description: Optional description (max 255 chars).
        :param exercise_id: Database ID.
        """
        self._id = exercise_id
        self.set_name(name)
        self.set_category(category)
        self.set_description(description)

    @property
    def id(self):
        """
        :return: The database ID of the exercise (or None).
        """
        return self._id

    @property
    def name(self):
        return self._name

    def set_name(self, name):
        """
        Sets the exercise name.
        :param name: Non-empty string, max 100 characters.
        """
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        if not name.strip():
            raise ValueError("Name cannot be empty.")
        if len(name) > 100:
            raise ValueError("Name is too long (max 100 chars).")
        self._name = name.strip()

    @property
    def category(self):
        return self._category

    def set_category(self, category):
        """
        Sets the exercise category.
        :param category: Must be one of the
        VALID_CATEGORIES (Strength, Cardio, Flexibility).
        """
        if not isinstance(category, str):
            raise TypeError("Category must be a string.")

        if category not in self.VALID_CATEGORIES:
            raise ValueError(f"Invalid category. Allowed: {self.VALID_CATEGORIES}")

        self._category = category

    @property
    def description(self):
        return self._description

    def set_description(self, description):
        """
        Sets the description.
        :param description: String, max 255 characters. None is converted to an empty string.
        :raises ValueError: If the description exceeds the character limit.
        """
        if description is None:
            description = ""
        if not isinstance(description, str):
            raise TypeError("Description must be a string.")
        if len(description) > 255:
            raise ValueError("Description is too long.")
        self._description = description.strip()

    def __repr__(self):
        return f"<Exercise: {self.name}>"