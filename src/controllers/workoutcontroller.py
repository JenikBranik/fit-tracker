import csv
import os
from datetime import datetime
from src.database.connection import DbConnection
from src.models.repositories.workoutrepositories import WorkoutRepository
from src.models.repositories.exerciserepository import ExerciseRepository
from src.models.entities.workoutitem import WorkoutItem
from src.views.workoutview import WorkoutView
from src.commands.workoutcommands import StartWorkoutCommand, AddWorkoutItemCommand, SaveCompleteWorkoutCommand


class WorkoutController:
    def __init__(self, invoker, session_manager):
        """
        Initializes the controller with dependencies.
        """
        self.invoker = invoker
        self.session_manager = session_manager
        self.db_conn = DbConnection.get_instance()

        self.repo = WorkoutRepository(self.db_conn)
        self.ex_repo = ExerciseRepository(self.db_conn)

        self.view = WorkoutView()

    def create_full_workout(self):
        """
        Orchestrates the creation of a workout session using a TRANSACTION.
        Data is collected in memory and saved atomically at the end.
        """
        if not self.session_manager.is_logged_in():
            self.view.show_error("You need to login first.")
            return

        user = self.session_manager.get_current_user()

        note = self.view.get_workout_header_input()
        start_time = datetime.now()

        items_buffer = []

        try:
            while True:
                all_exercises = self.ex_repo.get_all()
                if not all_exercises:
                    self.view.show_no_exercises_warning()
                    break

                item_data = self.view.get_workout_item_input(all_exercises)

                item_entity = WorkoutItem(
                    workout_id=None,
                    exercise_id=item_data['exercise_id'],
                    sets=item_data['sets'],
                    reps=item_data['reps'],
                    weight_kg=item_data['weight_kg'],
                    is_warmup=item_data['is_warmup']
                )

                items_buffer.append(item_entity)
                if not self.view.ask_to_continue():
                    break

            if items_buffer:

                transaction_command = SaveCompleteWorkoutCommand(
                    repository=self.repo,
                    user_id=user.id,
                    start_time=start_time,
                    note=note,
                    items=items_buffer
                )

                self.invoker.execute_command(transaction_command)

                self.view.show_message("Workout saved.")
            else:
                self.view.show_error("Workout contains no exercises, save cancelled.")

        except Exception as e:
            self.view.show_error(f"Error saving workout: {str(e)}")

    def show_workout_history(self):
        """
        Retrieves and displays the complete workout history.
        """
        if not self.session_manager.is_logged_in():
            self.view.show_error("You need to login first.")
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
            self.view.show_error(str(e))

    def import_workouts_from_csv(self):
        """
        Reads CSV file selected by user and imports data.
        """
        if not self.session_manager.is_logged_in():
            self.view.show_error("You need to login first.")
            return

        user = self.session_manager.get_current_user()

        file_path = self.view.get_csv_file_path()

        if not file_path:
            return

        if not os.path.exists(file_path):
            self.view.show_error(f"File '{file_path}' not found.")
            return

        created_workouts_map = {}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    s_time_str = row['start_time'].strip()
                    note = row['note'].strip()

                    try:
                        s_time = datetime.strptime(s_time_str, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        s_time = datetime.strptime(s_time_str, "%Y-%m-%d %H:%M")

                    workout_key = (s_time_str, note)

                    if workout_key not in created_workouts_map:
                        start_cmd = StartWorkoutCommand(self.repo, user.id, note, s_time)
                        new_workout_id = self.invoker.execute_command(start_cmd)
                        created_workouts_map[workout_key] = new_workout_id

                    current_workout_id = created_workouts_map[workout_key]

                    ex_name = row['exercise_name'].strip()
                    ex_id = self.ex_repo.get_id_by_name(ex_name)

                    if not ex_id:
                        self.view.show_import_warning(f"Exercise '{ex_name}' not found, skipping row.")
                        continue

                    is_warmup_val = row['is_warmup'].strip()
                    is_warmup_bool = is_warmup_val.lower() in ('1', 'true', 'ano', 'y')

                    item_entity = WorkoutItem(
                        workout_id=current_workout_id,
                        exercise_id=ex_id,
                        sets=int(row['sets']),
                        reps=int(row['reps']),
                        weight_kg=float(row['weight_kg']),
                        is_warmup=is_warmup_bool
                    )

                    add_cmd = AddWorkoutItemCommand(self.repo, current_workout_id, item_entity)
                    self.invoker.execute_command(add_cmd)

            self.view.show_import_success()

        except Exception as e:
            self.view.show_error(str(e))