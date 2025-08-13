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

class BaseTest:
    def __init__(self, setup,test_case_id):
        self.setup = setup
        self.config_utils = ConfigUtils()
        self.url = self.config_utils.get_url()
        self.username = self.config_utils.get_username()
        self.password = self.config_utils.get_password()
        self.tableIP = self.config_utils.get_tableIP()
        self.base_url = self.config_utils.get_ppApplication_Url()
        self.chips_df = read_chip_ids_df("data/AutomationChips.xlsx")
        self.screenshot_util = ScreenshotUtil(setup)
        self.login_page = LoginPage(setup)
        self.table_actions = TableActions(setup)
        self.games_tab = GamesTab(setup)
        self.view_table_tab = ViewTableTab(setup)
        self.Override_Tab = OverrideTab(setup)
        self.UI_Utils = UIUtils(setup)
        self.expire_and_adjust_variance = ExpireAndAdjustVariance(setup)
        self.buyin_data = get_buyin_data("data/testData.xlsx", test_case_id)
        self.wager_data = get_wager_data("data/testData.xlsx", test_case_id)
        self.card_data = get_cards_data("data/testData.xlsx", test_case_id)
        self.take_bets_data = get_takeBets_data("data/testData.xlsx", test_case_id)
        self.payout_data = get_payout_data("data/testData.xlsx", test_case_id)
        self.buyin_processor = BuyIN(setup)
        self.wager_processor = Wager(setup)
        self.card_processor = GameoutComes()
        self.take_bets_processor = TakeBets(setup)
        self.payout_processor = Payout(setup)
        self.Configuration_API = ConfigurationAPI()
        self._run_base_setup()  # Automatically run setup on instantiation

    def _run_base_setup(self):
        self.login_page.navigate(self.url)
        self.login_page.login(self.username, self.password)
        self.setup.wait_for_timeout(2000)
        self.table_actions.table_close_and_open()
        self.expire_and_adjust_variance.expire_and_adjust()
        self.setup.wait_for_timeout(3000)  # Wait for the setup to complete before proceeding
        
    def void_game(self):
        try:
            self.Override_Tab.click_void_hand()
            print("Void Hand button clicked.")
        except Exception as e:
            print(f"Failed to void hand: {e}")