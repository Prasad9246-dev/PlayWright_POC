import requests
import time

class GameoutComes:
    def __init__(self):
        pass

    def draw_cards(self, cards, table_ip):
        base_url = f"https://{table_ip}:790/api/table/v1"
        for card in cards:
            url = f"{base_url}/drawcard?card={card}"
            print(f"Drawing card: {card} -> {url}")
            response = requests.get(url, verify=False)
            print(f"Response: {response.status_code} {response.text}")
        time.sleep(1)

    def press_shoe_button(self, table_ip):
        base_url = f"https://{table_ip}:790/api/table/v1"
        shoe_url = f"{base_url}/shoebutton"
        print(f"Pressing shoe button: {shoe_url}")
        response = requests.get(shoe_url, verify=False)
        time.sleep(1)
        print(f"Shoe button response: {response.status_code} {response.text}")

    def draw_cards_and_shoe_press(self, cards, table_ip):
        """
        Calls draw_cards and then press_shoe_button.
        """
        self.draw_cards(cards, table_ip)
        self.press_shoe_button(table_ip)
        
    def deal_cards_and_activate_shoe(self, table_ip: str, *cards):
        """
        Deals one or more cards on the table using the drawcard API (GET method).
        After all cards are dealt, activates the shoe button API.
        :param table_ip: The table IP address as a string.
        :param cards: Variable number of card strings (e.g., "4s", "5h", "6d").
        """
        api_url = f"https://{table_ip}:790/api/table/v1/drawcard"
        headers = {'Content-Type': 'application/json'}
        for card in cards:
            try:
                url_with_param = f"{api_url}?card={card}"
                resp = requests.get(url_with_param, headers=headers, verify=False)
                print(f"Deal card '{card}' response: {resp.status_code} {resp.text}")
            except Exception as e:
                print(f"Error dealing card '{card}': {e}")
        # After all cards are dealt, activate the shoe button API
        try:
            shoe_url = f"https://{table_ip}:790/api/table/v1/shoebutton"
            resp_shoe = requests.get(shoe_url, headers=headers, verify=False)
            print(f"Shoe activation API response: {resp_shoe.status_code} {resp_shoe.text}")
        except Exception as e:
            print(f"Error calling shoe activation API: {e}")