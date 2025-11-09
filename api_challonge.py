class ChallongeAPI:
    def __init__(self, page):
        from config import CHALLONGE_USERNAME, CHALLONGE_API_KEY

        self.page = page
        self.set_slug_or_id()
        
        self.username = CHALLONGE_USERNAME
        self.api_key = CHALLONGE_API_KEY

    def set_slug_or_id(self):
        """If a challonge url is not provided, we assume it is the tournament id directly"""
        if "challonge" not in self.page:
            self.slug = self.page
            return
        
        self.slug = self.page.split('/')[-1]

        if self.page.split('.')[1] == 'challonge':
            self.slug = self.page.split('.')[0].split('//')[1] + '-' + self.slug

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

        try:
            response = requests.get(url, auth=HTTPBasicAuth(self.username, self.api_key), headers=headers)
            
            # Will raise an error if status != 200
            response.raise_for_status()

        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 404:
                print("404 Client Error")
                print("Please retry using 'tournament_id' instead of the url.")
                print("You should find this information on the source code of the page. It is a code number found after 'tournament_id'.")
                exit(1)
            else:
                # Re-raise other HTTP errors
                raise

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
