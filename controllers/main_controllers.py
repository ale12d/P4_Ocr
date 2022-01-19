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
    def __init__(self, db_info_player):
        self.db_info_player = db_info_player

    def __call__(self):

        input_tournaments = InputTournaments()
        name_tournament, place_tournament, date_tournament, nb_round = input_tournaments()
        setting_tournament = SettingTournament(name_tournament, place_tournament, date_tournament, nb_round)

        return PickPerId(setting_tournament, self.db_info_player)


class PairPlayers:

    def __init__(self, setting_tournament, db_info_player,result):
        self.setting_tournament = setting_tournament
        self.db_info_player = db_info_player
        self.result = result

    def __call__(self):
        players = self.db_info_player.table("Players")

        dic_rank_id = {}
        players_rank_game = {}
        list_players = []
        match_to_do = {}

        for nb_players in range(len(players.all())):
            dic_rank_id[players.all()[nb_players]["id"]] = players.all()[nb_players]["ranking"]

        for i in range(self.setting_tournament.NB_PLAYERS):
            list_players.append(self.setting_tournament.players['player ' + str(i + 1)])
            players_rank_game[int(self.setting_tournament.players['player ' + str(i + 1)])] = dic_rank_id[
                int(self.setting_tournament.players['player ' + str(i + 1)])]
            sorted_players_rank_game = sorted(players_rank_game.items(), key=lambda kv: kv[1])

        print(self.result)
        print(self.result.keys())

        if self.result == {}:

            for player in range(int(self.setting_tournament.NB_PLAYERS / 2)):
                match_to_do[sorted_players_rank_game[player][0]] = \
                sorted_players_rank_game[player + int(self.setting_tournament.NB_PLAYERS / 2)][0]
            return (match_to_do)

        elif self.result != {}:

            for player in range(int(self.setting_tournament.NB_PLAYERS / 2)):

                match_to_do[sorted_players_rank_game[player][0]] = \
                sorted_players_rank_game[player + int(self.setting_tournament.NB_PLAYERS / 2)][0]

                match = str(list(match_to_do.keys())[player]) + "-" + str(list(match_to_do.values())[player])
                i = 1

                while match in self.result :

                    if player + int(self.setting_tournament.NB_PLAYERS / 2) + i  == int(self.setting_tournament.NB_PLAYERS) :
                        i= i - self.setting_tournament.NB_PLAYERS
                    else :
                        print(player + int(self.setting_tournament.NB_PLAYERS / 2) + i)

                        if sorted_players_rank_game[player + int(self.setting_tournament.NB_PLAYERS / 2) + i][0] not in match_to_do.keys():
                            match_to_do[sorted_players_rank_game[player][0]] = \
                                sorted_players_rank_game[player + int(self.setting_tournament.NB_PLAYERS / 2) + i][0]
                            match = str(list(match_to_do.keys())[player]) + "-" + str(list(match_to_do.values())[player])
                            i = i + 1
                            print(match_to_do)
                        else :
                            match_to_do[sorted_players_rank_game[player][0]] = 4
                            break
                    if match not in self.result:
                        break

            return(match_to_do)


class LoadTournament:
    def __init__(self, db_tournament):
        self.db_tournament = db_tournament

    def __call__(self):
        show_tournament = ShowTournaments()
        root_directory = os.getcwd()
        show_tournament(root_directory, self.db_tournament)


class MainMenuController:

    def __call__(self):
        db_info_player = TinyDB("Players_saved.json")
        db_tournament = TinyDB("info_tournaments.json")
        show_mod = ShowMod()
        show_mod()

        while True :

            mod = input('\nChoose an option from among these (1,2,3,0) :')

            option = {1: StartTournament(db_info_player),
                      2: LoadTournament(db_tournament),
                      3: 0,
                      0: CreatePlayer(db_info_player),
                      }

            if (int(mod) in [1, 2, 3, 0]) :
                return option[int(mod)]()

            else :
                print('That\'s not an option!')


class CreatePlayer:
    def __init__(self, db_info_player):
        self.db_info_player = db_info_player
    def __call__(self):

        ranking = 1000
        input_players = InputPlayers(self.db_info_player)
        first_name, surname, id, date_of_birth, sex = input_players()
        info_players = InfoNewPlayer(first_name, surname, id, ranking, date_of_birth, sex)

        return SaveNewPlayer(info_players, self.db_info_player)


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

    def __init__(self, info_new_player, db_info_player):
        self.info_new_player = info_new_player
        self.db_info_player = db_info_player

    def __call__(self):
        serialized_info = [{
            'id': getattr(self.info_new_player, "id"),
            'surname': getattr(self.info_new_player, "surname"),
            'first_name': getattr(self.info_new_player, "first_name"),
            'date_of_birth': getattr(self.info_new_player, "date_of_birth"),
            'ranking': getattr(self.info_new_player, "ranking"),
            'sex': getattr(self.info_new_player, "sex"),

        }]
        info_player_table = self.db_info_player.table("Players")
        info_player_table.insert_multiple(serialized_info)

        return MainMenuController


class ResultRound:

    def __init__(self, winner, players_match, result):
        self.winner = winner
        self.players_match = players_match
        self.result = result

    def __call__(self):

        self.result['-'.join(self.players_match)] = self.winner

        if "N" in self.winner:
            pass

        if self.players_match[0] in self.winner:
            pass

        if self.players_match[1] in self.winner:
            pass

        return self.result



class PickPerId:

    def __init__(self, setting_tournament, db_info_player):
        self.setting_tournament = setting_tournament
        self.db_info_player = db_info_player

    def __call__(self):

        players = self.db_info_player.table("Players")

        show_players = ShowPlayers()
        self.player_dic = {}

        for nm_player in range(len(players.all())):
            show_players(players.all()[nm_player]['surname'],
                         players.all()[nm_player]['first_name'],
                         players.all()[nm_player]['id'])

        for nb_player in range(int(self.setting_tournament.NB_PLAYERS)):
            self.player_dic['player ' + str(nb_player + 1)] = None

        for player_to_pick in range(self.setting_tournament.NB_PLAYERS):
            print("\nplayer " + str(player_to_pick + 1))
            pick = input()
            self.player_dic["player " + str(player_to_pick + 1)] = pick

        self.setting_tournament.players = self.player_dic
        return StartRound(self.setting_tournament, self.db_info_player)


class StartRound:
    def __init__(self, setting_tournament, db_info_player):
        self.setting_tournament = setting_tournament
        self.db_info_player = db_info_player
        self.result = {}
        self.players_match = 0

    def __call__(self):
        save_tournament = SaveTournament(self.setting_tournament)
        save_tournament()

        for round in range(self.setting_tournament.nb_round):

            pair_players = PairPlayers(self.setting_tournament, self.db_info_player,self.result )
            match_to_do = pair_players()


            # print matchs
            for nb_match in range(int(self.setting_tournament.NB_PLAYERS / 2)):
                print("match n°" + str(nb_match + 1) + " : " + str(list(match_to_do.keys())[nb_match]) + " vs " + str(
                    list(match_to_do.values())[nb_match]))

            print("\n")

            for nb_match in range(int(self.setting_tournament.NB_PLAYERS / 2)):
                print("result match n°" + str(nb_match + 1) + " ([" + str(
                    list(match_to_do.keys())[nb_match]) + "] or " + "[N]" + " or [" + str(
                    list(match_to_do.values())[nb_match]) + "]) :")
                winner_input = input()
                players_match = [str(list(match_to_do.keys())[nb_match]), str(list(match_to_do.values())[nb_match])]

                result_round = ResultRound(winner_input, players_match, self.result)
                self.result = result_round()


class Ranking:
    pass
