from GameSkeleton.GameoutComes import GameoutComes
from GameSkeleton.Wager import Wager
from pages.ViewTableTab import ViewTableTab
from pages.login_page import LoginPage
from pages.GamesTab import GamesTab
from pages.OverrideTab import OverrideTab
from utils.Expire_And_Adjust_Variance import ExpireAndAdjustVariance
from utils.TableActions import TableActions
from utils.excel_reader import get_buyin_data, get_cards_data, get_wager_data, get_takeBets_data, get_payout_data
from utils.config_read import ConfigUtils
from utils.excel_reader import read_chip_ids_df
from utils.UIUtils import UIUtils
from GameSkeleton.BuyIN import BuyIN
from GameSkeleton.TakeBets import TakeBets
from GameSkeleton.Payouts import Payout
from utils.ConfigurationAPI import ConfigurationAPI
from utils.ScreenshotUtil import ScreenshotUtil

class PPBaseTest:
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
            "tbd_url": config_utils.get_url(),
            "pp_application_url": config_utils.get_ppApplication_Url(),
            "username": config_utils.get_username(),
            "password": config_utils.get_password(),
            "tableIP": config_utils.get_tableIP(),
        }

    def _init_data(self):
        self.chips_df = read_chip_ids_df("data/AutomationChips.xlsx")
        self.buyin_data = get_buyin_data("data/testData.xlsx", self.test_case_id)
        self.wager_data = get_wager_data("data/testData.xlsx", self.test_case_id)
        self.card_data = get_cards_data("data/testData.xlsx", self.test_case_id)
        self.take_bets_data = get_takeBets_data("data/testData.xlsx", self.test_case_id)
        self.payout_data = get_payout_data("data/testData.xlsx", self.test_case_id)

    def _init_pages_and_utils(self):
        setup = self.setup
        self.screenshot_util = ScreenshotUtil(setup)
        self.login_page = LoginPage(setup)
        self.table_actions = TableActions(setup)
        self.games_tab = GamesTab(setup)
        self.view_table_tab = ViewTableTab(setup)
        self.Override_Tab = OverrideTab(setup)
        self.UI_Utils = UIUtils(setup)
        self.expire_and_adjust_variance = ExpireAndAdjustVariance(setup)
        self.buyin_processor = BuyIN(setup)
        self.wager_processor = Wager(setup)
        self.card_processor = GameoutComes()
        self.take_bets_processor = TakeBets(setup)
        self.payout_processor = Payout(setup)
        self.Configuration_API = ConfigurationAPI()

    def _run_base_setup(self):
        self.login_page.navigate(self.config["pp_application_url"])
        self.login_page.login(self.config["username"], self.config["password"])
        self.setup.wait_for_timeout(3000)
