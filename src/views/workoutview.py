class WorkoutView:
    def get_workout_header_input(self):
        """
        Starts a new workout session and asks for a note.
        :return: str (The note entered by the user).
        """
        print("\n--- NEW WORKOUT SESSION ---")
        return input("Note (optional): ").strip()

    def get_workout_item_input(self, available_exercises):
        """
        Collects details for a specific exercise set.
        Selection is done by EXERCISE NAME.
        """
        print("\n--- ADD EXERCISE ---")

        # 1. Vytvoříme mapu: "jmeno cviku" -> ID
        # Příklad: {"honba": 1, "drep": 2}
        exercises_map = {}

        print(f"{'NAME':<20} {'CATEGORY'}")
        print("-" * 30)

        for ex in available_exercises:
            print(f"{ex.name:<20} {ex.category}")
            # Uložíme si název malými písmeny pro snadnější hledání
            exercises_map[ex.name.strip().lower()] = ex.id

        print("-" * 30)

        # 2. Výběr podle jména
        exercise_id = None
        while True:
            # Zeptáme se na jméno a převedeme na malá písmena
            name_input = input("Enter Exercise Name: ").strip().lower()

            if name_input in exercises_map:
                exercise_id = exercises_map[name_input]
                break

            print("❌ Invalid name. Please type the exact name from the list above.")

        # 3. Zbytek (Série, Opakování, Váha)
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

        # 4. Warm-up
        warmup_input = input("Is this a warm-up set? (y/n) [n]: ").strip().lower()
        is_warmup = warmup_input in ('y', 'yes', 'true', '1')

        return {
            'exercise_id': exercise_id,
            'sets': sets,
            'reps': reps,
            'weight_kg': weight,
            'is_warmup': is_warmup
        }

    def ask_to_continue(self):
        """
        Asks the user if they want to add another exercise to the current workout.
        :return: bool (True if yes, False if no).
        """
        choice = input("\nAdd another exercise? (y/n): ").strip().lower()
        return choice in ('y', 'yes', 'true')

    def show_history(self, history_data):
        """
        Displays the complete workout history.

        :param history_data: List of tuples [(WorkoutHeader, [Items...]), ...]
        """
        print("\n" + "=" * 40)
        print("WORKOUT HISTORY")
        print("=" * 40)

        if not history_data:
            print("No workouts recorded yet.")
            return

        for workout, items in history_data:
            date_str = workout.start_time.strftime("%Y-%m-%d %H:%M")
            print(f"\nDate: {date_str}")
            if workout.note:
                print(f"Note: {workout.note}")

            print("-" * 40)

            if not items:
                print("   (No exercises in this workout)")
            else:
                for item in items:
                    warmup_tag = " (Warm-up)" if item['is_warmup'] else ""

                    print(f"   • {item['exercise_name']}: "
                          f"{item['sets']} x {item['reps']} @ {item['weight']} kg"
                          f"{warmup_tag}")
            print("-" * 40)