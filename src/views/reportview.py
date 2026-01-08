class ReportView:
    def show_user_summary(self, summary):
        """
        Summary for users
        :param summary:
        :return:
        """
        print("Stats")

        if summary:
            print(f"User: {summary['username']}")
            print(f"Count of trainings: {summary['total_workouts']}")

            weight = summary['current_weight_kg']
            if weight:
                print(f"Actual weight: {weight} kg")
            else:
                print(f"Actual weight:  not yet added")
        else:
            print("Nothing to show")

