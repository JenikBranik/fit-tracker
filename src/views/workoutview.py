class WorkoutView:
    def get_workout_header_input(self):
        """
        Získá základní informace pro vytvoření tréninku (hlavičky).
        """
        print("\n=== NOVÝ TRÉNINK ===")
        # Poznámka může být prázdná, takže stačí obyčejný input
        note = input("Zadejte poznámku k tréninku (např. 'Leg day'): ").strip()
        return note


    def get_workout_item_input(self, available_exercises):
        """
        Získá data pro cvik.
        Místo zadávání ID uživatel vybírá ze seznamu.

        :param available_exercises: Seznam objektů Exercise načtený z DB
        """
        print("\n--- PŘIDAT CVIK DO TRÉNINKU ---")

        # 1. VÝBĚR CVIKU (Mapování Index -> Objekt)
        print("Dostupné cviky:")
        for index, ex in enumerate(available_exercises, 1):
            # Vypíše např.: "1. Bench Press (Strength)"
            print(f"{index}. {ex.name} ({ex.category})")

        selected_exercise = None

        while True:
            try:
                # Uživatel zadá pořadové číslo (např. 1)
                user_choice = int(input("Vyberte číslo cviku: "))

                # Ověříme, zda je číslo v rozsahu seznamu
                if 1 <= user_choice <= len(available_exercises):
                    # Získáme skutečný objekt (v poli je index o 1 menší)
                    selected_exercise = available_exercises[user_choice - 1]
                    print(f"-> Vybráno: {selected_exercise.name}")
                    break
                else:
                    print(f"❌ Prosím zadejte číslo mezi 1 a {len(available_exercises)}.")
            except ValueError:
                print("❌ Zadejte platné číslo.")

        # Nyní už známe skutečné ID cviku z objektu
        real_exercise_id = selected_exercise.id

        # 2. ZBYTEK JE STEJNÝ (Série, Opakování, Váha)
        while True:
            try:
                sets = int(input("Počet sérií: "))
                if sets > 0: break
                print("Musí být alespoň 1.")
            except ValueError:
                print("❌ Číslo!")

        while True:
            try:
                reps = int(input("Počet opakování: "))
                break
            except ValueError:
                print("❌ Číslo!")

        while True:
            try:
                weight = float(input("Váha (kg): ").replace(",", "."))
                break
            except ValueError:
                print("❌ Číslo!")

        return {
            "exercise_id": real_exercise_id,  # Vracíme už správné DB ID
            "sets": sets,
            "reps": reps,
            "weight_kg": weight
        }

    def ask_to_continue(self):
        """
        Zjistí, zda chce uživatel přidat další cvik.
        """
        while True:
            choice = input("\nChcete přidat další cvik? (a = ano / n = ne): ").lower().strip()
            if choice in ['a', 'ano']:
                return True
            if choice in ['n', 'ne']:
                return False
            # Pokud zadal nesmysl, smyčka se opakuje

    def show_success_message(self, message):
        print(f"✅ {message}")

    def show_error(self, message):
        print(f"❌ {message}")

    def show_history(self, history_data):
        """
        Vypíše kompletní historii.
        history_data je seznam n-tic: (WorkoutEntity, [seznam_položek])
        """
        print("\n=== HISTORIE TRÉNINKŮ ===")

        if not history_data:
            print("Zatím jste nezaznamenali žádný trénink.")
            return

        for workout, items in history_data:
            # Formátování data na hezčí string (např. 2023-10-05 18:30)
            date_str = workout.start_time.strftime("%Y-%m-%d %H:%M")

            print(f"\n📅 {date_str} | ID: {workout.id}")
            if workout.note:
                print(f"   Poznámka: {workout.note}")
            print("   " + "-" * 30)

            if not items:
                print("   (Žádné cviky v tomto tréninku)")
            else:
                for item in items:
                    print(f"   • {item['exercise_name']}: {item['sets']}x{item['reps']} ({item['weight']} kg)")

            print("   " + "=" * 30)