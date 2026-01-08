import tkinter as tk
from tkinter import filedialog
import os

class WorkoutView:
    def get_workout_header_input(self):
        """
        Starts a new workout session and asks for a note.
        :return: str (The note entered by the user).
        """
        print("\nNew workout session")
        return input("Note: ").strip()

    def get_workout_item_input(self, available_exercises):
        """
        Collects details for a specific exercise set.
        Selection is done by EXERCISE NAME.
        """
        print("\nAdd exercise")

        exercises_map = {}

        print(f"{'NAME':} {'CATEGORY'}")

        for ex in available_exercises:
            print(f"{ex.name} {ex.category}")
            exercises_map[ex.name.strip().lower()] = ex.id


        while True:
            name_input = input("Enter Exercise Name: ").strip().lower()

            if name_input in exercises_map:
                exercise_id = exercises_map[name_input]
                break

            print("Invalid name. Please type the exact name from the list above.")

        while True:
            try:
                sets = int(input("Sets: "))
                reps = int(input("Reps: "))
                weight = float(input("Weight (kg): "))
                if sets > 0 and reps > 0 and weight >= 0:
                    break
                print("Values must be positive.")
            except ValueError:
                print("Invalid input. Please enter numbers.")

        warmup_input = input("Is this a warm-up set? (y/n): ").strip().lower()
        is_warmup = warmup_input in ('y', 'yes')

        return {
            'exercise_id': exercise_id,
            'sets': sets,
            'reps': reps,
            'weight_kg': weight,
            'is_warmup': is_warmup
        }

    def ask_to_continue(self):
        """
        Asks the user if they want to add another exercise.
        """
        choice = input("\nAdd another exercise? (y/n): ").strip().lower()
        return choice in ('y', 'yes')

    def show_history(self, history_data):
        """
        Displays the complete workout history.
        """
        print("Workout history")

        if not history_data:
            print("No workouts recorded yet.")
            return

        for workout, items in history_data:
            date_str = workout.start_time.strftime("%Y-%m-%d %H:%M")
            print(f"\nDate: {date_str}")
            if workout.note:
                print(f"Note: {workout.note}")


            if not items:
                print("   (No exercises in this workout)")
            else:
                for item in items:
                    warmup_tag = " (Warm-up)" if item['is_warmup'] else ""
                    print(f"   • {item['exercise_name']}: "
                          f"{item['sets']} x {item['reps']} @ {item['weight']} kg"
                          f"{warmup_tag}")


    def show_no_exercises_warning(self):
        print("No exercises found in database. Please add exercises first.")

    def show_error(self, message):
        print(f"Error: {message}")

    def show_import_warning(self, message):
        print(f"{message}")

    def show_import_success(self):
        print(f"Import finished.")

    def get_csv_file_path(self):
        """
        Opens a GUI window for selecting CSV
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