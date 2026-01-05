class MainView:

    def show_welcome(self):
        """
        Prints the application startup banner.
        """
        print("\n" + "="*30)
        print("FITTRACKER")
        print("="*30)

    def show_status(self, user=None):
        """
        Displays the current login status.
        :param user: User object or None.
        """
        if user:
            print(f"\nLogged in as: {user.username}")
        else:
            print("\nNot logged in")

    def show_menu(self, menu_items):
        """
        Renders the list of available menu options.
        :param menu_items: List of MenuItem objects.
        """
        print("-" * 30)
        for item in menu_items:
            print(f" > {item.key}")
        print("-" * 30)

    def get_user_choice(self):
        """
        Prompts the user to make a selection.
        :return: str (The user's input).
        """
        return input("Your choice: ").strip()

    def show_invalid_choice(self):
        print("Invalid choice.")

    def show_exit_message(self):
        print("\nExit")

    def show_error(self, error):
        """
        Displays an error message and waits for user confirmation.
        """
        print(f"Error: {error}")
        input("Press Enter to continue...")