# lp_challonge

## Installation

Clone the repo locally and open `CONFIG_TO_RENAME.py`. Head over to [challonge](https://challonge.com/settings/developer) to get you API key (use the v1 version).
Complete the required information and rename the file to `config.py`.

## Usage

```bash
python main.py -ch <challonge_url>
```

For instance:

```bash
>>> python main.py -ch https://challonge.com/KSLW78

|p1=herO|p1link=HerO (Kim Joon Ho)
|p2=Classic|p2link=Classic (Kim Doh Woo)
|p3=Cure
|p4=Rogue
|p5=Creator
|p6=Percival
|p7=Nice
|p8=prome
|p9=Patches|p9link=Patches (American player)
|p10=ErebusBlack

{{ParticipantTable|hidden=1
|p1=triple|p1flag=kr|p1race=p
}}

Following players are unknown to LP but are tracked by the csv files
aegiseevee

Following players are untracked, please add them to one of the csv files:
guilliman, 7123652
powerpeople, 7600271
```

There are 4 different outputs, based on what table the player belongs in:
 - `notable.csv`: The player has a Liquipedia page and is considered a 'Notable Participant'
 - `non_notable.csv`: The player appears on Liquipedia but does not have a dedicated page, the csv file contains the known flag, race and team.
 - `unknown.csv`: The player does not appear on Liquipedia, no data is available.
 - The last output lists players that appear in none of the `player_data` files and should be added to one of them based on the previous descriptions of the tables.