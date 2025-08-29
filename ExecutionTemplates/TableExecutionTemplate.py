from GameSkeleton.GameOutcomes import GameoutComes
from GameSkeleton.Wager import Wager
from Pages.TablePages.ViewTableTab import ViewTableTab
from Pages.TablePages.LoginPage import LoginPage
from Pages.TablePages.PlayerTab import PlayerTab
from Pages.TablePages.GamesTab import GamesTab
from Pages.TablePages.OverrideTab import OverrideTab
from Pages.TablePages.SessionsTab import SessionsTab
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

class TableExecutionTemplate:
    def __init__(self, setup, test_case_id, feature_name):
        self.setup = setup
        self.feature_name = feature_name
        self.config = self._load_config()
        self.test_case_id = test_case_id
        self._init_data()
        self._init_pages_and_utils()
        self._run_base_setup()
        

    def _load_config(self):
        config_utils = ConfigUtils()
        config_utils.set_feature_name(self.feature_name)  # <-- This must be called!
        return {
            "build_version": config_utils.get_config().get("build_version"),
            "feature_name": self.feature_name,
            "tableIP": config_utils.get_tableIP(),
            "tbd_url": config_utils.get_table_url(),
            "username": config_utils.get_username(),
            "password": config_utils.get_password(),
            "pp_application_url": config_utils.get_ppApplication_Url(),
        }

    def _init_data(self):
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
        self.player_tab = PlayerTab(setup)
        self.table_actions = TableActions(setup, self.feature_name)
        self.games_tab = GamesTab(setup, self.feature_name)
        self.view_table_tab = ViewTableTab(setup)
        self.Override_Tab = OverrideTab(setup,self.feature_name)
        self.sessions_tab = SessionsTab(setup, self.feature_name)
        self.ui_utils = UIUtils(setup)
        self.expire_and_adjust_variance = ExpireAndAdjustVariance(setup, self.feature_name)
        self.buyin_processor = BuyIn(setup, self.feature_name)
        self.wager_processor = Wager(setup, self.feature_name)
        self.card_processor = GameoutComes()
        self.take_bets_processor = TakeBets(setup, self.feature_name)
        self.payout_processor = Payout(setup, self.feature_name)
        self.configuration_api = ConfigurationAPIs()

    def _run_base_setup(self):
        self.login_page.navigate(self.config["tbd_url"])
        self.login_page.login(self.config["username"], self.config["password"])
        self.setup.wait_for_timeout(2000)
        # self.table_actions.table_close_and_open()
        # self.expire_and_adjust_variance.expire_and_adjust()
        # self.setup.wait_for_timeout(3000)

    def void_game(self):
        try:
            self.Override_Tab.click_void_hand()
            print("Void Hand button clicked.")
        except Exception as e:
            print(f"Failed to void hand: {e}")
