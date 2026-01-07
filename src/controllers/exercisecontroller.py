from src.database.connection import DbConnection
from src.models.repositories.exerciserepository import ExerciseRepository
from src.views.exerciseview import ExerciseView
from src.commands.createexercisecommand import CreateExerciseCommand


class ExerciseController:
    def __init__(self, invoker):
        """
        Initializes the controller with necessary dependencies.
        :param invoker: The command invoker instance used to execute.
        """
        self.invoker = invoker
        self.db_conn = DbConnection.get_instance()
        self.repo = ExerciseRepository(self.db_conn)
        self.view = ExerciseView()

    def add_exercise(self):
        """
        """
        data = self.view.get_new_exercise_input()

        command = CreateExerciseCommand(
            self.repo,
            data['name'],
            data['category']
        )

        try:
            self.invoker.execute_command(command)
            print("Exercise successfully added.")
        except Exception as e:
            print(f"Error: {e}")

    def list_exercises(self):
        """
        Retrieves all available exercises from the repository.
        """
        try:
            exercises = self.repo.get_all()
            self.view.show_list(exercises)
        except Exception as e:
            print(f"Error: {e}")