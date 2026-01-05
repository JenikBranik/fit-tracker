from datetime import datetime
from src.database.connection import DbConnection
from src.models.repositories.workoutrepositories import WorkoutRepository
from src.models.repositories.exerciserepository import ExerciseRepository
from src.models.entities.workoutitem import WorkoutItem
from src.views.workoutview import WorkoutView

from src.commands.workoutcommands import StartWorkoutCommand, AddWorkoutItemCommand


class WorkoutController:

    def __init__(self, invoker, session_manager):
        """
        Initializes the controller with dependencies.
        :param invoker: The command invoker for executing.
        :param session_manager: The session manager to
        ensure actions are performed for the correct user.
        """
        self.invoker = invoker
        self.session_manager = session_manager
        self.db_conn = DbConnection.get_instance()

        self.repo = WorkoutRepository(self.db_conn)
        self.ex_repo = ExerciseRepository(self.db_conn)

        self.view = WorkoutView()

    def create_full_workout(self):
        """
        """
        if not self.session_manager.is_logged_in():
            print("You need to login.")
            return

        user = self.session_manager.get_current_user()

        note = self.view.get_workout_header_input()
        start_time = datetime.now()

        try:
            start_command = StartWorkoutCommand(self.repo, user.id, note, start_time)

            workout_id = self.invoker.execute_command(start_command)

            print(f"Created.")

            while True:
                all_exercises = self.ex_repo.get_all()
                if not all_exercises:
                    print("Nothing.")
                    break

                item_data = self.view.get_workout_item_input(all_exercises)

                item_entity = WorkoutItem(
                    workout_id=workout_id,
                    exercise_id=item_data['exercise_id'],
                    sets=item_data['sets'],
                    reps=item_data['reps'],
                    weight_kg=item_data['weight_kg']
                )

                add_item_command = AddWorkoutItemCommand(self.repo, workout_id, item_entity)
                self.invoker.execute_command(add_item_command)

                print("Saved.")

                if not self.view.ask_to_continue():
                    break

        except Exception as e:
            print(f"Error: {e}")

    def show_workout_history(self):
        """
        Retrieves and displays the complete
        workout history for the logged-in user.
        """
        if not self.session_manager.is_logged_in():
            print("Login.")
            return

        user = self.session_manager.get_current_user()

        try:
            workouts = self.repo.get_all_by_user(user.id)
            full_history = []

            for w in workouts:
                items = self.repo.get_items_with_names(w.id)
                full_history.append((w, items))

            self.view.show_history(full_history)

        except Exception as e:
            print(f"Error: {e}")