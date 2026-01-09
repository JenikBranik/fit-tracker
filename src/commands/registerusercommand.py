from src.commands.icommand import ICommand
from src.models.entities.user import User

class RegisterUserCommand(ICommand):
    def __init__(self, repository, username, email):
        self.repo = repository
        self.username = username
        self.email = email

    def execute(self):
        """
        Creates a new User entity and persists it to the database.
        :return: int (ID of the newly created user)
        """
        new_user_entity = User(self.username,self.email)
        return self.repo.create(new_user_entity)