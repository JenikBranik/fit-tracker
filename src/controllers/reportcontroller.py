from src.database.connection import DbConnection
from src.models.repositories.reportrepository import ReportRepository
from src.views.reportview import ReportView


class ReportController:
    def __init__(self, invoker, session_manager):
        """
        :param invoker: Command invoker
        :param session_manager: current user session manager
        """
        self.invoker = invoker
        self.session_manager = session_manager

        self.db_conn = DbConnection.get_instance()
        self.repo = ReportRepository(self.db_conn)
        self.view = ReportView()

    def show_my_statistics(self):
        """
        Displays the statistics of the logged in user
        """

        user = self.session_manager.get_current_user()

        summary_data = self.repo.get_user_summary(user.id)

        self.view.show_user_summary(summary_data)
