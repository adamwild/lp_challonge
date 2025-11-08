class ChallongeAPI:
    def __init__(self, page):
        from config import CHALLONGE_USERNAME, CHALLONGE_API_KEY

        self.page = page
        self.slug = page.split('/')[-1]

        self.username = CHALLONGE_USERNAME
        self.api_key = CHALLONGE_API_KEY

    def get_participants(self):
        import requests
        from requests.auth import HTTPBasicAuth

        url = f"https://api.challonge.com/v1/tournaments/{self.slug}/participants.json"

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

        response = requests.get(url, auth=HTTPBasicAuth(self.username, self.api_key), headers=headers)
        
        # Will raise an error if status != 200
        response.raise_for_status()

        participants = response.json()
        # player_names = [p["participant"]["name"] for p in participants]

        return participants
        
    
if __name__ == "__main__":
    mnw_29 = "https://challonge.com/fr/MNWeekly18"
    mnw_28 = "https://challonge.com/MNWeekly18"
    pig55 = "https://challonge.com/pigosaur_55"

    ch = ChallongeAPI(mnw_29)
    participants = ch.get_participants()

    for participant in participants:
        print(f"{participant["participant"]['name']}, {participant["participant"]['challonge_user_id']}")
