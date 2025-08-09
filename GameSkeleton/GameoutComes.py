import requests
import time

class GameoutComes:
    def __init__(self):
        pass

    def draw_cards_and_shoe_press(self, cards, table_ip):
        """
        Draws each card using the API, then presses the shoe button.
        Arguments:
            cards: list of card strings, e.g. ['2s', '4d', '3s', '4d']
            table_ip: IP address of the table as string
        """
        base_url = f"https://{table_ip}:790/api/table/v1"

        for card in cards:
            url = f"{base_url}/drawcard?card={card}"
            print(f"Drawing card: {card} -> {url}")
            response = requests.get(url, verify=False)
            print(f"Response: {response.status_code} {response.text}")

        time.sleep(1)
        # After all cards are drawn, press the shoe button
        shoe_url = f"{base_url}/shoebutton"
        print(f"Pressing shoe button: {shoe_url}")
        response = requests.get(shoe_url, verify=False)
        time.sleep(1)
        print(f"Shoe button response: {response.status_code} {response.text}")