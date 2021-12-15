import os
import json
from tinydb import TinyDB


class Tournament:

    NB_PLAYERS = 8

    def __init__(self, name_tournament=None, place_tournament=None, date_tournament=None, nb_round=4, **players):
        self.name_tournament = name_tournament
        self.place_tournament = place_tournament
        self.date_tournament = date_tournament
        self.nb_round = nb_round
        self.players = players

    def save_tournament(self):

        serialized_tournament = [{
            'name_tournament': self.name_tournament,
            'place_tournament': self.place_tournament,
            'date_tournament': self.date_tournament,
            'nb_round': self.nb_round,
            'players': self.players
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
        self.players = Player.find_all_players()
        print('\n[C] : Add new players')

        self.save_tournament()

    def load_tournament(self):
        os.system('cls')
        print("Load tournament")


class Round:
    pass


class Player:
    def __init__(self, first_name, surname):
        self.surname = surname
        self.first_name = first_name
        self.id = id

    @staticmethod
    def find_all_players():

        name_id = {}

        for player_attributes in json.load(open("Players_saved.json")):
            print("[" + player_attributes['id'] + "] " + player_attributes['surname'] + ' ' +
                  player_attributes['first_name'])

            name_id[player_attributes['id']] = player_attributes['surname'] + ' ' + player_attributes['first_name']

        player_dic = dict.fromkeys(['player 1', 'player 2', 'player 3', 'player 4', 'player 5',
                                    'player 6', 'player 7', 'player 8'])

        for player_to_pick in range(Tournament.NB_PLAYERS):
            print("\nplayer " + str(player_to_pick+1))
            pick = input()
            player_dic["player " + str(player_to_pick+1)] = name_id[pick]

        return player_dic


class Ranking:
    def __init__(self):
        pass

    def show_ranking(self):
        pass
