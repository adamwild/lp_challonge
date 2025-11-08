class Challonge:
    def __init__(self, page):
        from pathlib import Path
        from api_challonge import ChallongeAPI
        
        current_folder = Path(__file__).parent

        self.page = page
        self.api = ChallongeAPI(page)

        self.path_notables = current_folder / "player_data" /"notable.csv"
        self.path_non_notables = current_folder / "player_data" / "non_notable.csv"
        self.path_unknown = current_folder / "player_data" / "unknown.csv"

        self.participants = ""
        self.notables, self.non_notables, self.unknown = "", "", ""

    def load_player_tables(self):
        """Loads the notable.csv, non_notable.csv and unknown.csv tables"""
        def load_table(path_table):
            import pandas as pd

            df = pd.read_csv(path_table)
            str_cols = df.select_dtypes(include='object').columns
            df[str_cols] = df[str_cols].apply(lambda col: col.str.strip())
            df = df.fillna('')

            return df

        self.notables = load_table(self.path_notables)
        self.non_notables = load_table(self.path_non_notables)
        self.unknown = load_table(self.path_unknown)

    def make_participant_lists(self):
        """From the list of participants, split in players that are notable, non-notable but known and totally unknown players"""
        if not self.participants:
            self.participants = self.api.get_participants()

        if not self.notables or not self.non_notables or not self.unknown:
            self.load_player_tables()

        lp_notable_players = []
        lp_non_notable_players = [r"{{ParticipantTable|hidden=1", r"}}"]
        unknown_players = []
        new_unknown_players = []

        for participant in self.participants:

            # Only consider participants who have checked in
            if not participant["participant"]['checked_in']:
                continue

            # Current player info
            challonge_name = participant["participant"]['name']
            challonge_user_id = participant["participant"]['challonge_user_id']

            # Handle notable players
            if challonge_user_id in self.notables['challonge_user_id'].values:
                row = self.notables.loc[self.notables['challonge_user_id'] == challonge_user_id]
                row = row.iloc[0]

                curr_player_number = len(lp_notable_players) + 1

                to_add = f"|p{curr_player_number}={row['lp_name']}"
                if row['player_link']:
                    to_add += f"|p{curr_player_number}link={row['player_link']}"
                    
                # The Clem exception
                if challonge_user_id == 2073649:
                    to_add += f"|p{curr_player_number}race=t"

                lp_notable_players.append(to_add)

            # Handle non-notable players
            elif challonge_user_id in self.non_notables['challonge_user_id'].values:
                row = self.non_notables.loc[self.non_notables['challonge_user_id'] == challonge_user_id]
                row = row.iloc[0]

                curr_player_number = len(lp_non_notable_players) - 1

                to_add = f"|p{curr_player_number}={row['lp_name']}"
                for element in ['flag', 'race', 'team']:
                    if row[element]:
                        to_add += f"|p{curr_player_number}{element}={row[element]}"
                lp_non_notable_players.insert(-1, to_add)

            # Handle unknown players
            elif challonge_user_id in self.unknown['challonge_user_id'].values:
                unknown_players.append(challonge_name)

            else:
                new_unknown_players.append(f"{challonge_name}, {challonge_user_id}")


        str_lp_notable_players = "\n".join(lp_notable_players)
        str_lp_non_notable_players = "\n".join(lp_non_notable_players)
        str_unknown_players = "\n".join(unknown_players)
        str_new_unknown_players = "\n".join(new_unknown_players)

        return str_lp_notable_players, str_lp_non_notable_players, str_unknown_players, str_new_unknown_players
    
    def print_all_participants(self):
        str_lp_notable_players, str_lp_non_notable_players, str_unknown_players, str_new_unknown_players = self.make_participant_lists()

        if str_lp_notable_players:
            print(str_lp_notable_players)
            print()

        if str_lp_non_notable_players:
            print(str_lp_non_notable_players)
            print()

        if str_unknown_players:
            print("Following players are unknown to LP but are tracked by the csv files")
            print(str_unknown_players)
            print()

        if str_new_unknown_players:
            print("Following players are untracked, please add them to one of the csv files:")
            print(str_new_unknown_players)
            print()
        
if __name__ == "__main__":
    mnw_29 = "https://challonge.com/fr/MNWeekly29"
    mnw_28 = "https://challonge.com/MNWeekly18"
    pig55 = "https://challonge.com/pigosaur_55"

    ch = Challonge(mnw_28)
    ch.print_all_participants()