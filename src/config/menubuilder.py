from src.controllers.usercontroller import UserController
from src.controllers.exercisecontroller import ExerciseController
from src.controllers.measurementcontroller import MeasurementController
from src.controllers.workoutcontroller import WorkoutController
from src.utils.menuitem import MenuItem


class MenuBuilder:

    @staticmethod
    def build_auth_menu(invoker, session_manager):
        """
        Constructs the menu for unauthenticated users.
        :param invoker: Instance of the Invoker class for handling commands.
        :param session_manager: Instance of the SessionManager for auth state.
        :return: list of menu items: Login, Register, Exit
        """
        user_controller = UserController(invoker, session_manager)
        items = [
            MenuItem("login",  user_controller.login_user),
            MenuItem("register",  user_controller.register_user),
            MenuItem("exit",  None)  # None = signál pro exit
        ]
        return items

    @staticmethod
    def build_main_menu(invoker, session_manager):
        """
        Constructs the main application menu.
        Initializes all necessary controllers with the required dependencies.
        :param invoker: Instance of the Invoker class.
        :param session_manager: Instance of the SessionManager.
        :return: list of available application actions
        """
        exercise_controller = ExerciseController(invoker)
        measurement_controller = MeasurementController(invoker, session_manager)
        workout_controller = WorkoutController(invoker, session_manager)

        items = [
            MenuItem("exercise list", exercise_controller.list_exercises),
            MenuItem("add new exercise", exercise_controller.add_exercise),
            MenuItem("record weight", measurement_controller.add_measurement),
            MenuItem("weight history", measurement_controller.list_measurements),
            MenuItem("training", workout_controller.create_full_workout),
            MenuItem("history of trainings", workout_controller.show_workout_history),
            MenuItem("log out", session_manager.logout),
            MenuItem("exit", None)
        ]
        return items