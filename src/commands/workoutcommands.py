from src.commands.icommand import ICommand
from src.models.entities.workoutitem import WorkoutItem

class StartWorkoutCommand(ICommand):
    def __init__(self, repository, user_id, note, start_time):
        self.repo = repository
        self.user_id = user_id
        self.note = note
        self.start_time = start_time

    def execute(self):
        """
        Creates a new workout record (header) in the database.
        :return: int (ID of the newly created workout)
        """
        return self.repo.create_workout(self.user_id, self.note, self.start_time)

class AddWorkoutItemCommand(ICommand):
    def __init__(self, repository, workout_id, item_entity: WorkoutItem):
        self.repo = repository
        self.workout_id = workout_id
        self.item_entity = item_entity

    def execute(self):
        """
        Persists a specific exercise item (sets, reps, weight) to the database for the given workout.
        :return: int (ID of the inserted item) or None, depending on repository implementation.
        """
        return self.repo.add_workout_item(self.workout_id, self.item_entity)