from GameSkeleton.GameoutComes import GameoutComes
from GameSkeleton.Wager import Wager
from pages.InventoryTab import InventoryTab
from pages.ViewTableTab import ViewTableTab
from pages.login_page import LoginPage
from pages.PlayerTab import PlayerTab
from pages.GamesTab import GamesTab
from utils.ConfigurationAPI import ConfigurationAPI
from utils.Expire_And_Adjust_Variance import ExpireAndAdjustVariance
from utils.TableActions import TableActions
from utils.excel_reader import get_buyin_data, get_cards_data, get_wager_data, get_takeBets_data, get_payout_data   
from conftest import get_ppApplication_Url, get_url, get_username, get_password, get_tableIP, get_ppApplication_Url
from utils.excel_reader import read_chip_ids_df
from GameSkeleton.BuyIN import BuyIN
from GameSkeleton.TakeBets import TakeBets
from GameSkeleton.Payouts import Payout

class BaseTest:
    def __init__(self, setup,test_case_id):
        self.setup = setup
        self.url = get_url()
        self.username = get_username()
        self.password = get_password()
        self.tableIP = get_tableIP()
        self.base_url = get_ppApplication_Url()
        self.chips_df = read_chip_ids_df("data/AutomationChips.xlsx")
        self.login_page = LoginPage(setup)
        self.Player_Tab = PlayerTab(setup)
        self.table_actions = TableActions(setup)
        self.View_Table_Tab = ViewTableTab(setup)
        self.games_tab = GamesTab(setup)
        self.inventory_tab = InventoryTab(setup)
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
        self.setup.wait_for_timeout(3000)  # Wait for the setup to complete before
        # proceeding with the test case