from models.tournament import SettingTournament
from views.__init__ import View
from tinydb import TinyDB
import json


class ApplicationController:

    def __init__(self):
        pass

    def start(self):
        self.controller = MainMenuController()
        while self.controller:
            self.controller = self.controller()


class StartTournament:

    def __call__(self):
        print("Write the name of the tournament")
        name_tournament = input()

        print("Write the place of the tournament")
        place_tournament = input()

        print("Write the date of the tournament")
        date_tournament = input()

        print("Write the number of round of the tournament  (default=4)")
        nb_round = input()

        setattr(SettingTournament, "name_tournament", name_tournament)
        setattr(SettingTournament, "place_tournament", place_tournament)
        setattr(SettingTournament, "date_tournament", date_tournament)
        setattr(SettingTournament, "nb_round", nb_round)

        print('\nChoice ' + str(SettingTournament.NB_PLAYERS) + ' players :' + '\n')

        return PickPerId()


class LoadTournament:

    def __call__(self):
        view = View()
        print("Load tournament :")
        view.ShowTournaments()


class MainMenuController:

    def __call__(self):
        view = View()

        view.ShowMod()
        mod = input()

        option = {1: StartTournament(),
                  2: LoadTournament(),
                  3: 0,
                  }

        return option[int(mod)]()


class SaveTournament:

    def __call__(self):
        print(getattr(SettingTournament, "name_tournament"))

        serialized_tournament = [{
            'name_tournament': getattr(SettingTournament, "name_tournament"),
            'place_tournament': getattr(SettingTournament, "place_tournament"),
            'date_tournament': getattr(SettingTournament, "date_tournament"),
            'nb_round': getattr(SettingTournament, "nb_round"),
            'players': getattr(SettingTournament, "players"),
        }]
        db_tournament = TinyDB("info_tournaments.json")
        tournaments_table = db_tournament.table("tournaments")
        tournaments_table.insert_multiple(serialized_tournament)


class PickPerId:

    def __call__(self):

        view = View()
        self.name_id = {}

        for player_attributes in json.load(open("Players_saved.json")):
            view.ShowPlayers(player_attributes['surname'], player_attributes['first_name'],
                             player_attributes['id'])
            self.name_id[player_attributes['id']] = player_attributes['surname'] + ' ' + player_attributes['first_name']

        self.player_dic = dict.fromkeys(['player 1', 'player 2', 'player 3', 'player 4', 'player 5',
                                         'player 6', 'player 7', 'player 8'])

        for player_to_pick in range(SettingTournament.NB_PLAYERS):
            print("\nplayer " + str(player_to_pick + 1))
            pick = input()
            self.player_dic["player " + str(player_to_pick + 1)] = self.name_id[pick]

        SettingTournament.players = self.player_dic

        return SaveTournament()
