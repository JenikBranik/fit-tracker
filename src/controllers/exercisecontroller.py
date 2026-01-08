import csv
import os
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
        Orchestrates adding a new exercise.
        """
        data = self.view.get_new_exercise_input()

        command = CreateExerciseCommand(
            self.repo,
            data['name'],
            data['category']
        )

        try:
            self.invoker.execute_command(command)
            self.view.show_success("Exercise successfully added.")
        except Exception as e:
            self.view.show_error(str(e))

    def list_exercises(self):
        """
        Retrieves all available exercises from the repository.
        """
        try:
            exercises = self.repo.get_all()
            self.view.show_list(exercises)
        except Exception as e:
            self.view.show_error(str(e))

    def import_exercises_from_csv(self):
        """
        Import exercise from CSV.
        """
        file_path = self.view.get_csv_file_path()

        if not file_path:
            return
        if not os.path.exists(file_path):
            self.view.show_error(f"File '{file_path}' hasnt been found.")
            return

        created_count = 0
        skipped_count = 0

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    name = row['name'].strip()
                    category = row['category'].strip()

                    valid_categories = ['Strength', 'Cardio', 'Flexibility']
                    capitalized_cat = category.capitalize()
                    if capitalized_cat not in valid_categories:
                        print(f"Unknown '{category}' of exercise '{name}', skip.")
                        skipped_count += 1
                        continue

                    existing_id = self.repo.get_id_by_name(name)

                    if existing_id:
                        skipped_count += 1
                        continue

                    command = CreateExerciseCommand(
                        self.repo,
                        name,
                        capitalized_cat
                    )
                    self.invoker.execute_command(command)
                    created_count += 1

            self.view.show_import_success()

        except Exception as e:
            self.view.show_error(str(e))

    def rename_exercise(self):
        """
        Rename exercise
        """
        self.list_exercises()
        old_name, new_name = self.view.get_rename_input()

        if not old_name or not new_name:
            self.view.show_error("Names cannot be empty.")
            return

        success = self.repo.update_name(old_name, new_name)

        if success:
            self.view.show_success(f"Exercise '{old_name}' renamed to '{new_name}'.")
        else:
            self.view.show_error(f"Exercise '{old_name}' not found.")