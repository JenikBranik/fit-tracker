class MeasurementView:
    def get_weight_input(self):
        """
        Values from user
        :return: float
        """
        print("\nRecord weight")
        while True:
            weight_str = input("Enter weight (kg): ").strip().replace(",", ".")

            try:
                weight = float(weight_str)
                if weight > 0:
                    return weight
                print("Weight must be positive.")
            except ValueError:
                print("Invalid input. Please enter a number (e.g. 80.5).")

    def show_history(self, username, measurements):
        """
        Return history of measurements.
        :param username:
        :param measurements: List of objects
        """
        print(f"\nWeight history: {username}")

        if not measurements:
            print("No records found.")
        else:
            for m in measurements:
                print(f"{m.log_date}: {m.weight_kg:.1f} kg")


    def show_success(self, message):
        print(f"{message}")

    def show_error(self, message):
        print(f"Error: {message}")

    def get_delete_date_input(self):
        """
        Ask user to delete date.
        """
        print("\nDelete measurement")
        print("Format: YYYY-MM-DD (for example. 2023-01-15)")
        while True:
            val = input("Enter date to delete: ").strip()
            if len(val) == 10 and val[4] == '-' and val[7] == '-':
                return val
            print("Invalid format. Please use YYYY-MM-DD.")