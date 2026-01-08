from src.database.connection import DbConnection
from src.models.repositories.measurementrepository import MeasurementRepository
from src.commands.logmeasurementcommand import LogMeasurementCommand
from src.views.measurementview import MeasurementView  # <-- Nový import


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

        self.view = MeasurementView()

    def add_measurement(self):
        """
        Gets validated input from View and executes the LogMeasurementCommand.
        """
        if not self.session_manager.is_logged_in():
            self.view.show_error("You need to login first.")
            return

        current_user = self.session_manager.get_current_user()

        weight = self.view.get_weight_input()

        try:
            command = LogMeasurementCommand(self.repo, current_user.id, weight)
            self.invoker.execute_command(command)

            self.view.show_success("Weight saved successfully.")

        except Exception as e:
            self.view.show_error(str(e))

    def list_measurements(self):
        """
        Fetches data and sends it to the View for display.
        """
        if not self.session_manager.is_logged_in():
            self.view.show_error("You need to login first.")
            return

        current_user = self.session_manager.get_current_user()

        try:
            measurements = self.repo.get_by_user(current_user.id)

            self.view.show_history(current_user.username, measurements)

        except Exception as e:
            self.view.show_error(str(e))

    def delete_measurement_action(self):
        """
        Delete measurement.
        """
        if not self.session_manager.is_logged_in():
            self.view.show_error("Login required.")
            return

        user = self.session_manager.get_current_user()
        self.list_measurements()
        date_str = self.view.get_delete_date_input()
        success = self.repo.delete_by_date(user.id, date_str)

        if success:
            self.view.show_success(f"Records for {date_str} deleted.")
        else:
            self.view.show_error(f"No records found for date {date_str}.")