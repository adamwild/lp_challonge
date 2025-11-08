import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-ch", "--challonge", help="Make the participants lists from a challonge page", type=str)
args = parser.parse_args()

from challonge import Challonge

if args.challonge:
    challonge = Challonge(args.challonge)
    challonge.print_all_participants()