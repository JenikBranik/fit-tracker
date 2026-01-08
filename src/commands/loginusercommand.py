from src.commands.icommand import ICommand

class LoginUserCommand(ICommand):
    def __init__(self, repository, session_manager, email):
        self.repo = repository
        self.session = session_manager
        self.email = email

    def execute(self):
        """
        Authenticates the user against the database and updates the active session.
        :return: User object (The logged-in user entity)
        """
        user = self.repo.get_by_email(self.email)

        if user:
            self.session.login(user)
            return user
        else:
            raise ValueError("User does not exist.")