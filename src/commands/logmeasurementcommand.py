from datetime import date
from src.commands.icommand import ICommand
from src.models.entities.bodymeasurement import BodyMeasurement

class LogMeasurementCommand(ICommand):
    def __init__(self, repository, user_id, weight_kg):
        self.repo = repository
        self.user_id = user_id
        self.weight_kg = weight_kg

    def execute(self):
        """
        Creates a new measurement entity with the current date and saves it to the database.
        :return: int (ID of the newly created measurement record)
        """
        measurement = BodyMeasurement(
            user_id=self.user_id,
            log_date=date.today(),
            weight_kg=self.weight_kg
        )

        return self.repo.create(measurement)