class Invoker:
    def __init__(self):
        self._history = []

    def execute_command(self, command):
        """
        Method for running individual commands
        :param command: string input
        :return: called function
        """
        result = command.execute()

        self._history.append(command)
        return result