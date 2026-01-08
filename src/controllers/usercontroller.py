from src.commands.loginusercommand import LoginUserCommand
from src.models.repositories.userrepository import UserRepository
from src.views.userview import UserView
from src.database.connection import DbConnection
from src.commands.registerusercommand import RegisterUserCommand


class UserController:
    def __init__(self, invoker, session_manager):
        """
        Initializes the controller with the necessary infrastructure.
        """
        self.invoker = invoker
        self.session_manager = session_manager
        self.db_conn = DbConnection.get_instance()

        self.repo = UserRepository(self.db_conn)
        self.view = UserView()

    def register_user(self):
        """
        Orchestrates user registration and auto-login.
        """
        data = self.view.get_new_user_input()

        try:
            command = RegisterUserCommand(
                repository=self.repo,
                username=data['username'],
                email=data['email']
            )
            self.invoker.execute_command(command)

            self.view.show_registration_success()

            new_user = self.repo.get_by_email(data['email'])

            if new_user:
                self.session_manager.login(new_user)
                self.view.show_login_success(new_user.username)
            else:
                self.view.show_error("Auto-login failed. Please try logging in manually.")

        except Exception as e:
            self.view.show_error(str(e))

    def login_user(self):
        """
        Executes the LoginUserCommand which validates credentials.
        """
        email = self.view.get_login_input()

        try:
            command = LoginUserCommand(
                repository=self.repo,
                session_manager=self.session_manager,
                email=email
            )
            logged_user = self.invoker.execute_command(command)

            self.view.show_login_success(logged_user.username)

        except Exception as e:
            self.view.show_error(str(e))