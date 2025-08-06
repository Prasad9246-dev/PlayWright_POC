from pages.login_page import LoginPage
from utils.TableActions import TableActions
from conftest import get_url, get_username, get_password, get_tableIP

class BaseTest:
    def __init__(self, setup):
        self.setup = setup
        self.url = get_url()
        self.username = get_username()
        self.password = get_password()
        self.tableIP = get_tableIP()
        self.login_page = LoginPage(setup)
        self.table_actions = TableActions(setup)
        self._run_base_setup()  # Automatically run setup on instantiation

    def _run_base_setup(self):
        self.login_page.navigate(self.url)
        self.login_page.login(self.username, self.password)
        self.setup.wait_for_timeout(2000)
        self.table_actions.table_close_and_open()
        self.table_actions.expire_and_adjust()
        self.setup.wait_for_timeout(3000)