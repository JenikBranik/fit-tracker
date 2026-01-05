class UserView:
    def get_new_user_input(self):
        """
        Prompts the user for registration details.
        :return: dict ('username' and 'email')
        """
        print("\n--- NEW USER REGISTRATION ---")
        username = input("Enter username: ").strip()
        email = input("Enter email: ").strip()
        return {"username": username, "email": email}

    def show_success(self):
        """
        Displays a success message after creating a new user.
        """
        print(f"User created")

    def show_error(self, message):
        """
        Displays an error message to the user.
        :param message: string error message
        """
        print(f"Error: {message}")

    def get_login_input(self):
        """
        Prompts the user for their email to log in.
        :return: str (The email entered by the user)
        """
        print("\nLOGIN")
        return input("Enter your email: ").strip()