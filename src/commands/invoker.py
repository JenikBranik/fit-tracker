class Invoker:
    def __init__(self):
        pass

    def execute_command(self, command):
        """
        Method for running individual commands
        :param command: string input
        :return: called function
        """
        result = command.execute()
        return result