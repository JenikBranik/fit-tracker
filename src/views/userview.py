class UserView:
    def get_new_user_input(self):
        """
        Prompts the user for registration details.
        :return: dict ('username' and 'email')
        """
        print("\nRegistration:")
        while True:
            username = input("Enter username: ").strip()
            if username:
                break
            print("Username cannot be empty.")

        while True:
            email = input("Enter email: ").strip()
            if email:
                break
            print("Email cannot be empty.")

        return {"username": username, "email": email}

    def get_login_input(self):
        """
        Prompts the user for their email to log in.
        :return: str (The email entered by the user)
        """
        print("\nLogin")
        while True:
            email = input("Enter your email: ").strip()
            if email:
                return email
            print("Email cannot be empty.")

    def show_registration_success(self):
        """
        Displays a success message after creating a new user.
        """
        print("User account successfully created.")

    def show_login_success(self, username):
        """
        Displays a success message after login.
        """
        print(f"Logged in as: {username}")

    def show_error(self, message):
        """
        Displays an error message to the user.
        """
        print(f"Error: {message}")