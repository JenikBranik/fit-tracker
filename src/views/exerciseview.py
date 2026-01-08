import tkinter as tk
from tkinter import filedialog
import os

class ExerciseView:
    def get_new_exercise_input(self):
        """
        Gets input from the user to create a new exercise.
        :return: dict (A dictionary with keys: 'name', 'category', 'description')
        """
        print("\nAdd new exercise")

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

        return {
            "name": name,
            "category": selected_category
        }

    def show_list(self, exercises):
        """
        Displays a list of exercises in a formatted table.
        If the list is empty, it shows a message to the user.
        :param exercises: List[Exercise] (A list of exercise objects to display)
        """
        print("\nExercises")

        if not exercises:
            print("No exercises found in the database.")
        else:
            print(f"{'NAME':} {'CATEGORY'}")
            print("\n")

            for ex in exercises:
                print(f"{ex.name:} {ex.category}")

    def show_success(self, message):
        """
        Success message.
        """
        print(f"{message}")

    def show_error(self, message):
        """
        Error message.
        """
        print(f"Error: {message}")

    def get_csv_file_path(self):
        """
        GUI CSV window.
        """
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)

        file_path = filedialog.askopenfilename(
            title="Chose CSV file",
            filetypes=[("CSV files", "*.csv")],
            initialdir=os.getcwd()
        )
        root.destroy()
        return file_path

    def show_import_success(self):
        print(f"Import done.")

    def get_rename_input(self):
        """
        Rename exercises.
        """
        print("\nRename exercises")
        old_name = input("Enter current exercise name: ").strip()
        new_name = input("Enter new exercise name: ").strip()
        return old_name, new_name