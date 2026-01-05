from src.commands.loginusercommand import LoginUserCommand
from src.models.repositories.userrepository import UserRepository
from src.views.userview import UserView
from src.database.connection import DbConnection
from src.commands.registerusercommand import RegisterUserCommand


class UserController:
    def __init__(self, invoker, session_manager):
        """
        Initializes the controller with the necessary infrastructure for command execution and state management.
        :param invoker: The command invoker used to execute registration and login commands.
        :param session_manager: The session manager to handle user state (logged in/out).
        """
        self.invoker = invoker
        self.session_manager = session_manager
        self.db_conn = DbConnection.get_instance()

        self.repo = UserRepository(self.db_conn)
        self.view = UserView()

    def register_user(self):
        """
        """
        data = self.view.get_new_user_input()

        try:
            command = RegisterUserCommand(
                repository=self.repo,
                username=data['username'],
                email=data['email']
            )

            user_id = self.invoker.execute_command(command)
            self.view.show_success(user_id)
            new_user = self.repo.get_by_email(data['email'])

            if new_user:
                self.session_manager.login(new_user)
                print(f"Logged in: {new_user.username}")
            else:
                print("Error")

        except ValueError as e:
            self.view.show_error(f"Error: {e}")

        except RuntimeError as e:
            self.view.show_error(f"Error: {e}")

        except Exception as e:
            self.view.show_error(f"Error: {e}")

    def login_user(self):
        """
        executes the LoginUserCommand which validates credentials
        and updates the SessionManager.
        """
        email = self.view.get_login_input()
        try:
            command = LoginUserCommand(
                repository=self.repo,
                session_manager=self.session_manager,
                email=email
            )
            logged_user = self.invoker.execute_command(command)
            print(f"Logged in: {logged_user.username}")
        except ValueError as e:
            self.view.show_error(str(e))
        except Exception as e:
            self.view.show_error(f"Error: {e}")