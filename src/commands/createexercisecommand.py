from src.commands.icommand import ICommand
from src.models.entities.exercise import Exercise

class CreateExerciseCommand(ICommand):
    def __init__(self, repository, name, category, description):
        self.repo = repository
        self.name = name
        self.category = category
        self.description = description

    def execute(self):
        """
        Creates a new Exercise entity and saves it via the repository.
        :return: int (ID of the newly created exercise)
        """
        new_exercise = Exercise(self.name, self.category, self.description)
        return self.repo.create(new_exercise)