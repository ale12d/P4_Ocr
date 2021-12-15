import os
import json
from tinydb import TinyDB


class Tournament:

    NB_PLAYERS = 8

    def __init__(self, name_tournament=None, place_tournament=None, date_tournament=None, nb_round=4):
        self.name_tournament = name_tournament
        self.place_tournament = place_tournament
        self.date_tournament = date_tournament
        self.nb_round = nb_round

    def save_tournament(self):

        serialized_tournament = [{
            'name_tournament': self.name_tournament,
            'place_tournament': self.place_tournament,
            'date_tournament': self.date_tournament,
            'nb_round': self.nb_round,
            #'players': players
        }]
        db_tournament = TinyDB("tournaments.json")
        tournaments_table = db_tournament.table("tournaments")
        tournaments_table.insert_multiple(serialized_tournament)

    def start_tournament(self):

        os.system('cls')

        print("Write the name of the tournament")
        self.name_tournament = input()
        print("Write the place of the tournament")
        self.place_tournament = input()
        print("Write the date of the tournament")
        self.date_tournament = input()
        print("Write the number of round of the tournament  (default=4)")
        self.nb_round = input()

        os.system('cls')
        print(self.name_tournament)

        print('\nChoice ' + str(self.NB_PLAYERS) + ' players :' + '\n')
        player = Player()
        player.find_all_players()
        print('\n[C] : Add new players')

        self.save_tournament()

    @staticmethod
    def modify_tournament():
        os.system('cls')
        print("Choice the tournament to modify")


class Round:
    pass


class Player:
    def __init__(self, **player_attributes):

        for attr_name, attr_value in player_attributes.items():
            setattr(self, attr_name, attr_value)

    def find_all_players(self):
        for player_attributes in json.load(open("Players_saved.json")):
            print(player_attributes['surname'] + ' ' + player_attributes['first_name'])


class Ranking:
    def __init__(self):
        pass

    def show_ranking(self):
        pass
