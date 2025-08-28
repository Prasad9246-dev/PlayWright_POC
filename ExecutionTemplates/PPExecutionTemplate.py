from GameSkeleton.GameOutcomes import GameoutComes
from GameSkeleton.Wager import Wager
from Pages.TablePages.ViewTableTab import ViewTableTab
from Pages.TablePages.LoginPage import LoginPage
from Pages.TablePages.GamesTab import GamesTab
from Pages.TablePages.OverrideTab import OverrideTab
from Pages.ConfigurationPages.ConfigurationLoginPage import ConfigurationLoginPage
from Utilites.TableUtils.ExpireAdjustVariance import ExpireAndAdjustVariance
from Utilites.TableUtils.TableActions import TableActions
from Utilites.ExcelRead.ExcelReader import get_buyin_data, get_cards_data, get_wager_data, get_takeBets_data, get_payout_data
from Utilites.ExcelRead.ConfigRead import ConfigUtils
from Utilites.ExcelRead.ExcelReader import read_chip_ids_df
from Utilites.UIUtils import UIUtils
from GameSkeleton.BuyIn import BuyIn
from GameSkeleton.TakeBets import TakeBets
from GameSkeleton.Payouts import Payout
from Utilites.APIs.ConfigurationAPIs import ConfigurationAPIs
from Utilites.Reporting.ScreenshotUtil import ScreenshotUtil


class PPExecutionTemplate:
    def __init__(self, setup, test_case_id):
        self.setup = setup
        self.config = self._load_config()
        self.test_case_id = test_case_id
        self._init_data()
        self._init_pages_and_utils()
        self._run_base_setup()

    def _load_config(self):
        config_utils = ConfigUtils()
        return {
            "tbd_url": config_utils.get_table_url(),
            "pp_application_url": config_utils.get_ppApplication_Url(),
            "username": config_utils.get_username(),
            "password": config_utils.get_password(),
            "tableIP": config_utils.get_tableIP(),
        }

    def _init_data(self):
        # self.excel_path = r"C:\Users\PrasadKamble\Walker Digital Table\u00A0Systems\WDTS INDIA - automation\Playwright\MasterFiles\AutomationChips.xlsx"
        # self.excel_path = self.excel_path.replace(r'\u00A0', '\u00A0')
        self.chips_df = read_chip_ids_df()
        self.buyin_data = get_buyin_data("Configuration/TestData.xlsx", self.test_case_id)
        self.wager_data = get_wager_data("Configuration/TestData.xlsx", self.test_case_id)
        self.card_data = get_cards_data("Configuration/TestData.xlsx", self.test_case_id)
        self.take_bets_data = get_takeBets_data("Configuration/TestData.xlsx", self.test_case_id)
        self.payout_data = get_payout_data("Configuration/TestData.xlsx", self.test_case_id)

    def _init_pages_and_utils(self):
        setup = self.setup
        self.screenshot_util = ScreenshotUtil(setup)
        self.login_page = LoginPage(setup)
        self.table_actions = TableActions(setup)
        self.games_tab = GamesTab(setup)
        self.view_table_tab = ViewTableTab(setup)
        self.override_tab = OverrideTab(setup)
        self.ui_utils = UIUtils(setup)
        self.expire_and_adjust_variance = ExpireAndAdjustVariance(setup)
        self.buyin_processor = BuyIn(setup)
        self.wager_processor = Wager(setup)
        self.card_processor = GameoutComes()
        self.take_bets_processor = TakeBets(setup)
        self.payout_processor = Payout(setup)
        self.configuration_api = ConfigurationAPIs()
        self.configuration_login = ConfigurationLoginPage(setup)

    def _run_base_setup(self):
        self.configuration_login.navigate(self.config["pp_application_url"])
        self.configuration_login.configuration_login(self.config["username"], self.config["password"])
        self.setup.wait_for_timeout(3000)
