from src.database.connection import DbConnection
from src.models.repositories.measurementrepository import MeasurementRepository
from src.commands.logmeasurementcommand import LogMeasurementCommand


class MeasurementController:
    def __init__(self, invoker, session_manager):
        """
        Initializes the controller with command execution.
        :param invoker: The command invoker for executing.
        :param session_manager: The manager handling the current user's session state.
        """
        self.invoker = invoker
        self.session_manager = session_manager
        self.db_conn = DbConnection.get_instance()
        self.repo = MeasurementRepository(self.db_conn)

    def add_measurement(self):
        """
        weight input, validates it, and executes the LogMeasurementCommand.
        Requires a valid active session.
        """
        if not self.session_manager.is_logged_in():
            print("You need to login first.")
            return

        current_user = self.session_manager.get_current_user()

        print("Measurement")
        try:
            weight_str = input("Entry weight: ").replace(",", ".")
            weight = float(weight_str)

            command = LogMeasurementCommand(self.repo, current_user.id, weight)
            self.invoker.execute_command(command)
            print("Saved.")

        except ValueError:
            print("Number!.")
        except Exception as e:
            print(f"Error: {e}")

    def list_measurements(self):
        """
        Fetches and displays the weight history
        for the currently logged-in user.
        """
        if not self.session_manager.is_logged_in():
            print("You need to login")
            return

        current_user = self.session_manager.get_current_user()
        measurements = self.repo.get_by_user(current_user.id)

        print(f"\nHistory: {current_user.username}")
        for m in measurements:
            print(f"{m.log_date}: {m.weight_kg} kg")