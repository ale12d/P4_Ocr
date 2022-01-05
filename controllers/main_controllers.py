from models import SettingTournament
from models import InfoNewPlayer
from views import ShowMod, InputTournaments, InputPlayers, ShowPlayers, ShowTournaments

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

    def __init__(self, setting_tournament):
        self.setting_tournament = setting_tournament

    def __call__(self):

        dic_rank_id = {}
        players_rank_game = {}
        list_players = []
        match_to_do = {}

        player_attributes = json.load(open(os.getcwd() + "\Players_saved.json"))
        for nm_player in player_attributes["Players"]:
            dic_rank_id[player_attributes["Players"][nm_player]["id"]] = player_attributes["Players"][nm_player][
                "ranking"]

        for i in range(self.setting_tournament.NB_PLAYERS):
            list_players.append(self.setting_tournament.players['player ' + str(i + 1)])
            players_rank_game[int(self.setting_tournament.players['player ' + str(i + 1)])] = dic_rank_id[
                int(self.setting_tournament.players['player ' + str(i + 1)])]
            sorted_players_rank_game = sorted(players_rank_game.items(), key=lambda kv: kv[1])

        for players in range(int(self.setting_tournament.NB_PLAYERS / 2)):
            match_to_do[sorted_players_rank_game[players][0]] = \
            sorted_players_rank_game[players + int(self.setting_tournament.NB_PLAYERS / 2)][0]

        return(match_to_do)


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
    def __init__(self, setting_tournament):
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

    def __init__(self, info_new_player):
        self.info_new_player = info_new_player

    def __call__(self):
        serialized_info = [{
            'id': getattr(self.info_new_player, "id"),
            'surname': getattr(self.info_new_player, "surname"),
            'first_name': getattr(self.info_new_player, "first_name"),
            'date_of_birth': getattr(self.info_new_player, "date_of_birth"),
            'ranking': getattr(self.info_new_player, "ranking"),
            'sex': getattr(self.info_new_player, "sex"),
            "Stats": {'win': getattr(self.info_new_player, "win"),
                      'draw': getattr(self.info_new_player, "draw"),
                      'lose': getattr(self.info_new_player, "lose")}

        }]
        db_info_player = TinyDB("Players_saved.json")
        info_player_table = db_info_player.table("Players")
        info_player_table.insert_multiple(serialized_info)

        return MainMenuController


class SaveStats:
    SCORE_WIN = 1
    SCORE_DRAW = 0.5
    SCORE_LOSE = 0

    def __init__(self, result, players_match):
        self.result = result
        self.players_match = players_match

    def __call__(self):

        with open("Players_saved.json", "r") as jsonFile:
            data = json.load(jsonFile)
        if "N" in self.result:

            for nb_players in data["Players"]:

                if str(data["Players"][nb_players]["id"]) == str(self.players_match[0]):
                    data["Players"][nb_players]["Stats"]["draw"] = data["Players"][nb_players]["Stats"]["draw"] + 1
                    data["Players"][nb_players]["ranking"] = data["Players"][nb_players]["ranking"] + self.SCORE_DRAW

                if str(data["Players"][nb_players]["id"]) == str(self.players_match[1]):
                    data["Players"][nb_players]["Stats"]["draw"] = data["Players"][nb_players]["Stats"]["draw"] + 1
                    data["Players"][nb_players]["ranking"] = data["Players"][nb_players]["ranking"] + self.SCORE_DRAW

            with open("Players_saved.json", "w") as jsonFile:
                json.dump(data, jsonFile)

        if self.players_match[0] in self.result:
            for nb_players in data["Players"]:
                print(data["Players"][nb_players]["id"])

                if str(data["Players"][nb_players]["id"]) == str(self.players_match[0]):
                    data["Players"][nb_players]["Stats"]["win"] = data["Players"][nb_players]["Stats"]["win"] + 1
                    data["Players"][nb_players]["ranking"] = data["Players"][nb_players]["ranking"] + self.SCORE_WIN

                if str(data["Players"][nb_players]["id"]) == str(self.players_match[1]):
                    data["Players"][nb_players]["Stats"]["lose"] = data["Players"][nb_players]["Stats"]["lose"] + 1
                    data["Players"][nb_players]["ranking"] = data["Players"][nb_players]["ranking"] + self.SCORE_LOSE

            with open("Players_saved.json", "w") as jsonFile:
                json.dump(data, jsonFile)

        if self.players_match[1] in self.result:
            for nb_players in data["Players"]:
                print(data["Players"][nb_players]["id"])

                if str(data["Players"][nb_players]["id"]) == str(self.players_match[1]):
                    data["Players"][nb_players]["Stats"]["win"] = data["Players"][nb_players]["Stats"]["win"] + 1
                    data["Players"][nb_players]["ranking"] = data["Players"][nb_players]["ranking"] + self.SCORE_WIN

                if str(data["Players"][nb_players]["id"]) == str(self.players_match[0]):
                    data["Players"][nb_players]["Stats"]["lose"] = data["Players"][nb_players]["Stats"]["lose"] + 1
                    data["Players"][nb_players]["ranking"] = data["Players"][nb_players]["ranking"] + self.SCORE_LOSE

            with open("Players_saved.json", "w") as jsonFile:
                json.dump(data, jsonFile)


class PickPerId:

    def __init__(self, setting_tournament):
        self.setting_tournament = setting_tournament

    def __call__(self):

        show_players = ShowPlayers()
        self.player_dic = {}

        player_attributes = json.load(open(os.getcwd() + "\Players_saved.json"))
        for nm_player in player_attributes["Players"]:
            show_players(player_attributes["Players"][nm_player]['surname'],
                         player_attributes["Players"][nm_player]['first_name'],
                         player_attributes["Players"][nm_player]['id'])

        for nb_player in range(int(self.setting_tournament.NB_PLAYERS)):
            self.player_dic['player ' + str(nb_player + 1)] = None

        for player_to_pick in range(self.setting_tournament.NB_PLAYERS):
            print("\nplayer " + str(player_to_pick + 1))
            pick = input()
            self.player_dic["player " + str(player_to_pick + 1)] = pick

        self.setting_tournament.players = self.player_dic
        return StartRound(self.setting_tournament)


class StartRound:
    def __init__(self, setting_tournament):
        self.setting_tournament = setting_tournament

    def __call__(self):
        save_tournament = SaveTournament(self.setting_tournament)
        pair_players = PairPlayers(self.setting_tournament)
        match_to_do = pair_players()
        save_tournament()

        # print matchs
        for nb_match in range(int(self.setting_tournament.NB_PLAYERS / 2)):
            print("match n°" + str(nb_match + 1) + " : " + str(list(match_to_do.keys())[nb_match]) + " vs " + str(
                list(match_to_do.values())[nb_match]))

        print("\n")

        for nb_match in range(int(self.setting_tournament.NB_PLAYERS / 2)):
            print("result match n°" + str(nb_match + 1) + " ([" + str(
                list(match_to_do.keys())[nb_match]) + "] or " + "[N]" + " or [" + str(
                list(match_to_do.values())[nb_match]) + "]) :")
            result = input()
            players_match = [str(list(match_to_do.keys())[nb_match]), str(list(match_to_do.values())[nb_match])]

            save_stats = SaveStats(result, players_match)
            save_stats()


class Ranking:
    pass
