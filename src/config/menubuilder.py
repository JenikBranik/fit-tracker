from src.controllers.usercontroller import UserController
from src.controllers.exercisecontroller import ExerciseController
from src.controllers.measurementcontroller import MeasurementController
from src.controllers.workoutcontroller import WorkoutController
from src.controllers.reportcontroller import ReportController
from src.utils.menuitem import MenuItem


class MenuBuilder:

    @staticmethod
    def build_auth_menu(invoker, session_manager):
        user_controller = UserController(invoker, session_manager)
        items = [
            MenuItem("login", user_controller.login_user),
            MenuItem("register", user_controller.register_user),
            MenuItem("exit", None)
        ]
        return items

    @staticmethod
    def build_main_menu(invoker, session_manager):
        exercise_controller = ExerciseController(invoker)
        measurement_controller = MeasurementController(invoker, session_manager)
        workout_controller = WorkoutController(invoker, session_manager)
        report_controller = ReportController(invoker, session_manager)

        items = [
            MenuItem("exercise list", exercise_controller.list_exercises),
            MenuItem("add new exercise", exercise_controller.add_exercise),
            MenuItem("rename exercise", exercise_controller.rename_exercise),
            MenuItem("record weight", measurement_controller.add_measurement),
            MenuItem("weight history", measurement_controller.list_measurements),
            MenuItem("delete weight by date", measurement_controller.delete_measurement_action),
            MenuItem("training", workout_controller.create_full_workout),
            MenuItem("history of trainings", workout_controller.show_workout_history),
            MenuItem("import exercises", exercise_controller.import_exercises_from_csv),
            MenuItem("import training", workout_controller.import_workouts_from_csv),
            MenuItem("my statistics", report_controller.show_my_statistics),
            MenuItem("log out", session_manager.logout),
            MenuItem("exit", None)
        ]
        return items