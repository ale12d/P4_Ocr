from models.tournament import SettingTournament
from models.player import InfoNewPlayer
from views.__init__ import ShowMod, InputTournaments, InputPlayers, ShowPlayers, ShowTournaments

from tinydb import TinyDB
import json
import os


class ApplicationController:

    def __init__(self):
        pass

    def start(self):
        self.controller = MainMenuController()
        while self.controller:
            self.controller = self.controller()


class StartTournament:

    def __call__(self):

        input_tournaments = InputTournaments()
        name_tournament, place_tournament, date_tournament, nb_round = input_tournaments()
        setting_tournament = SettingTournament(name_tournament, place_tournament, date_tournament, nb_round)

        return PickPerId(setting_tournament)


class PairPlayers:

    def __init__(self,setting_tournament):
        self.setting_tournament = setting_tournament

    def __call__(self):

        dic_rank_id = {}
        players_rank_game = {}
        list_players = []

        for player_attributes in json.load(open(os.getcwd() + "\controllers\Players_saved.json")):
            dic_rank_id[player_attributes["id"]] = player_attributes["ranking"]

        for i in range(self.setting_tournament.NB_PLAYERS):
            list_players.append(self.setting_tournament.players['player ' + str(i+1)])

            players_rank_game[self.setting_tournament.players['player ' + str(i+1)]] = int(dic_rank_id[self.setting_tournament.players['player ' + str(i+1)]])
            sorted_players_rank_game = sorted(players_rank_game.items(), key=lambda kv: kv[1])


        for players in range(int(self.setting_tournament.NB_PLAYERS/2)):
            print(str(sorted_players_rank_game[players]) + ' vs ' + str(sorted_players_rank_game[players+int(self.setting_tournament.NB_PLAYERS/2)]))

        return SaveTournament(self.setting_tournament)


class LoadTournament:
    def __call__(self):
        show_tournament = ShowTournaments()
        root_directory = os.getcwd()
        print("Load tournament :")
        show_tournament(root_directory)


class MainMenuController:

    def __call__(self):
        show_mod = ShowMod()

        show_mod()
        mod = input()

        option = {1: StartTournament(),
                  2: LoadTournament(),
                  3: 0,
                  0: CreatePlayer(),
                  }

        return option[int(mod)]()

class CreatePlayer:

    def __call__(self):
        ranking = 1000
        input_players = InputPlayers()
        first_name, surname, id, date_of_birth, sex = input_players()
        info_players = InfoNewPlayer(first_name, surname, id, ranking, date_of_birth, sex)

        return SaveNewPlayer(info_players)

class SaveTournament:
    def __init__(self,setting_tournament):
        self.setting_tournament = setting_tournament


    def __call__(self):

        serialized_tournament = [{
            'name_tournament': getattr(self.setting_tournament, "name_tournament"),
            'place_tournament': getattr(self.setting_tournament, "place_tournament"),
            'date_tournament': getattr(self.setting_tournament, "date_tournament"),
            'nb_round': getattr(self.setting_tournament, "nb_round"),
            'players': getattr(self.setting_tournament, "players"),
        }]
        db_tournament = TinyDB("info_tournaments.json")
        tournaments_table = db_tournament.table("tournaments")
        tournaments_table.insert_multiple(serialized_tournament)

class SaveNewPlayer:

    def __init__(self,info_new_player):
        self.info_new_player = info_new_player


    def __call__(self):

        serialized_info = [{
            'id': getattr(self.info_new_player, "id"),
            'surname': getattr(self.info_new_player, "surname"),
            'first_name': getattr(self.info_new_player, "first_name"),
            'date_of_birth': getattr(self.info_new_player, "date_of_birth"),
            'ranking': getattr(self.info_new_player, "ranking"),
            'sex': getattr(self.info_new_player, "sex"),
        }]
        db_info_player = TinyDB("Players_saved.json")
        info_player_table = db_info_player.table("Players")
        info_player_table.insert_multiple(serialized_info)


class PickPerId:

    def __init__(self,setting_tournament):
        self.setting_tournament = setting_tournament

    def __call__(self):

        show_players = ShowPlayers()
        self.name_id = {}
        for player_attributes in json.load(open(os.getcwd() + "\controllers\Players_saved.json")):
            show_players(player_attributes['surname'], player_attributes['first_name'],
                             player_attributes['id'])

        self.player_dic = dict.fromkeys(['player 1', 'player 2', 'player 3', 'player 4', 'player 5',
                                         'player 6', 'player 7', 'player 8'])
        for player_to_pick in range(self.setting_tournament.NB_PLAYERS):
            print("\nplayer " + str(player_to_pick + 1))
            pick = input()
            self.player_dic["player " + str(player_to_pick + 1)] = pick

        self.setting_tournament.players = self.player_dic
        return PairPlayers(self.setting_tournament)


class Ranking:
    pass

