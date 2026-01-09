from src.commands.icommand import ICommand
from src.models.entities.workoutitem import WorkoutItem


class StartWorkoutCommand(ICommand):
    """
    Command for creating a new workout header (session).
    """
    def __init__(self, repository, user_id, note, start_time):
        self.repo = repository
        self.user_id = user_id
        self.note = note
        self.start_time = start_time

    def execute(self):
        """
        Creates a new workout header in the database.
        :return: int (ID of the newly created workout)
        """
        return self.repo.create_workout(self.user_id, self.note, self.start_time)


class AddWorkoutItemCommand(ICommand):
    """
    Command for adding a workout item to an existing workout.
    """
    def __init__(self, repository, workout_id, item: WorkoutItem):
        self.repo = repository
        self.workout_id = workout_id
        self.item = item

    def execute(self):
        """
        Adds a workout item to the database.
        """
        self.repo.add_workout_item(self.workout_id, self.item)


class SaveCompleteWorkoutCommand(ICommand):
    """
    Command for saving a complete workout (header + items) as a transaction.
    """
    def __init__(self, repository, user_id, start_time, note, items):
        self.repo = repository
        self.user_id = user_id
        self.start_time = start_time
        self.note = note
        self.items = items

    def execute(self):
        """
        Saves the complete workout as a single atomic transaction.
        :return: int (ID of the newly created workout)
        """
        return self.repo.save_complete_workout(
            self.user_id,
            self.start_time,
            self.note,
            self.items
        )
