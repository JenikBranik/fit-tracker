from src.commands.invoker import Invoker
from src.config.menubuilder import MenuBuilder
from src.utils.sessionmanager import SessionManager
from src.views.mainview import MainView


class AppManager:
    def __init__(self):
        self.invoker = Invoker()
        self.session_manager = SessionManager()
        self.view = MainView()

    def run(self):
        """
        Starts the main application loop.
        """
        self.view.show_welcome()

        while True:
            if self.session_manager.is_logged_in():
                current_user = self.session_manager.get_current_user()
                self.view.show_status(current_user)
                menu_items = MenuBuilder.build_main_menu(self.invoker, self.session_manager)
            else:
                self.view.show_status(None)
                menu_items = MenuBuilder.build_auth_menu(self.invoker, self.session_manager)

            menu_map = {item.key: item for item in menu_items}

            self.view.show_menu(menu_items)

            choice = self.view.get_user_choice()

            if choice in menu_map:
                item = menu_map[choice]

                if item.action is None:
                    self.view.show_exit_message()
                    break

                try:
                    item.action()

                except Exception as e:
                    self.view.show_error(e)
            else:
                self.view.show_invalid_choice()