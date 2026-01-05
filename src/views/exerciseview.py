class ExerciseView:
    def get_new_exercise_input(self):
        """
        Gets input from the user to create a new exercise.
        :return: dict (A dictionary with keys: 'name', 'category', 'description')
        """
        print("\nADD NEW EXERCISE")

        while True:
            name = input("Exercise name: ").strip()
            if name:
                break
            print("Name cannot be empty.")

        print("Select category:")
        print("1. Strength")
        print("2. Cardio")
        print("3. Flexibility")

        categories = {
            "1": "Strength",
            "2": "Cardio",
            "3": "Flexibility"
        }

        while True:
            choice = input("Choice (1-3): ").strip()
            if choice in categories:
                selected_category = categories[choice]
                break
            print("Invalid choice, please enter 1, 2, or 3.")

        description = input("Description (optional): ").strip()

        return {
            "name": name,
            "category": selected_category,
            "description": description
        }

    def show_list(self, exercises):
        """
        Displays a list of exercises in a formatted table.
        If the list is empty, it shows a message to the user.

        :param exercises: List[Exercise] (A list of exercise objects to display)
        """
        print("\nEXERCISE LIST")

        if not exercises:
            print("No exercises found in the database.")
        else:
            print(f"{'NAME':} {'CATEGORY'}")
            print("-" * 40)

            for ex in exercises:
                print(f"{ex.name:} {ex.category}")