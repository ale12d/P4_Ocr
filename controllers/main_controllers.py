from models import SettingTournament
from models import InfoNewPlayer
from views import ShowMod, InputTournaments, InputPlayers, ShowTournaments, \
    ShowModRank, ShowAllPlayers, ShowMatchsToDo, ShowResultInput
from tinydb import TinyDB, Query


class ApplicationController:

    def __init__(self):
        pass

    def start(self):
        self.controller = MainMenuController()
        while self.controller:
            self.controller = self.controller()


class StartTournament:
    def __init__(self, db_info_player, db_tournament):
        self.db_info_player = db_info_player
        self.db_tournament = db_tournament

    def __call__(self):
        input_tournaments = InputTournaments(self.db_tournament)
        id_tournament, name_tournament, place_tournament, date_tournament, \
            nb_round = input_tournaments()
        setting_tournament = SettingTournament(id_tournament, name_tournament,
                                               place_tournament,
                                               date_tournament,
                                               nb_round)

        return PickPerId(setting_tournament, self.db_info_player)


class PairPlayers:

    def __init__(self, setting_tournament, db_info_player, result):
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
            dic_rank_id[players.all()[nb_players]["id"]] = \
                players.all()[nb_players]["ranking"]

        for i in range(self.setting_tournament.NB_PLAYERS):
            list_players.append(
                self.setting_tournament.players['player ' + str(i + 1)])
            players_rank_game[
                int(self.setting_tournament.players['player ' + str(i + 1)])] \
                = dic_rank_id[int(self.setting_tournament.players[
                                      'player ' + str(i + 1)])]
            sorted_players_rank_game = sorted(players_rank_game.items(),
                                              key=lambda kv: kv[1])

        if self.result == {}:

            for player in range(int(self.setting_tournament.NB_PLAYERS / 2)):
                match_to_do[sorted_players_rank_game[player][0]] = \
                    sorted_players_rank_game[
                        player + int(self.setting_tournament.NB_PLAYERS / 2)][
                        0]
            return match_to_do

        elif self.result != {}:

            for player in range(int(self.setting_tournament.NB_PLAYERS / 2)):
                match_to_do[sorted_players_rank_game[player][0]] = \
                    sorted_players_rank_game[
                        player + int(self.setting_tournament.NB_PLAYERS / 2)][
                        0]
            return match_to_do


class LoadTournament:
    def __init__(self, db_tournament):
        self.db_tournament = db_tournament

    def __call__(self):
        tournament = self.db_tournament.table("tournaments").get(
            Query().status == 0)
        print("[" + str(tournament['id_tournament']) + "] " + tournament[
            'name_tournament'])


class MainMenuController:

    def __call__(self):
        db_info_player = TinyDB("Players_saved.json")
        db_tournament = TinyDB("info_tournaments.json")
        show_mod = ShowMod()
        show_mod()

        while True:

            mod = input('\nChoose an option from among these (1,2,3,0) :')

            option = {1: StartTournament(db_info_player, db_tournament),
                      2: LoadTournament(db_tournament),
                      3: RankMenuController(db_tournament, db_info_player),
                      0: CreatePlayer(db_info_player),
                      }

            if int(mod) in [1, 2, 3, 0]:
                return option[int(mod)]()

            else:
                print('That\'s not an option!')


class RankMenuController:
    def __init__(self, db_tournament, db_info_player):
        self.db_tournament = db_tournament
        self.db_info_player = db_info_player

    def __call__(self):

        show_mod_rank = ShowModRank()
        show_mod_rank()

        while True:

            mod = input('\nChoose an option from among these (1,2,3,4,5) :')

            option = {1: ShowAllPlayers(self.db_info_player),
                      2: ShowTournaments(self.db_tournament, mod,
                                         self.db_info_player),
                      3: ShowTournaments(self.db_tournament, mod,
                                         self.db_info_player),
                      4: ShowTournaments(self.db_tournament, mod,
                                         self.db_info_player),
                      5: ShowTournaments(self.db_tournament, mod,
                                         self.db_info_player),
                      }

            if int(mod) in [1, 2]:
                list_players = option[int(mod)]()
                sort_controller = SortController(list_players,
                                                 self.db_info_player)
                sort_controller()
                break
            elif int(mod) in [3, 4, 5]:
                option[int(mod)]()
                break

            else:
                print('That\'s not an option!')


class SortController:
    def __init__(self, list_players, db_info_player):
        self.list_players = list_players
        self.db_info_player = db_info_player

    def __call__(self):

        while True:

            sort = input(
                '\n[1]:Sort by alphabetical order   [2]:Sort by ranking   '
                '[3]:Exit to main menu\n')

            option = {1: SortAlph(self.list_players, self.db_info_player),
                      2: SortRank(self.list_players, self.db_info_player),
                      3: MainMenuController(),
                      }

            if int(sort) in [1, 2, 3]:
                return option[int(sort)]()

            else:
                print('That\'s not an option!')


class CreatePlayer:
    def __init__(self, db_info_player):
        self.db_info_player = db_info_player

    def __call__(self):
        ranking = 1000
        input_players = InputPlayers(self.db_info_player)
        first_name, surname, id, date_of_birth, sex = input_players()
        info_players = InfoNewPlayer(first_name, surname, id, ranking,
                                     date_of_birth, sex)

        return SaveNewPlayer(info_players, self.db_info_player)


class SaveTournament:
    def __init__(self, setting_tournament):
        self.setting_tournament = setting_tournament

    def __call__(self):
        serialized_tournament = [{
            'id_tournament': getattr(self.setting_tournament, "id_tournament"),
            'name_tournament': getattr(self.setting_tournament,
                                       "name_tournament"),
            'place_tournament': getattr(self.setting_tournament,
                                        "place_tournament"),
            'date_tournament': getattr(self.setting_tournament,
                                       "date_tournament"),
            'nb_round': getattr(self.setting_tournament, "nb_round"),
            'players': getattr(self.setting_tournament, "players"),
            'result': {},
            'status': 0,
        }]
        db_tournament = TinyDB("info_tournaments.json")
        tournaments_table = db_tournament.table("tournaments")
        tournaments_table.insert_multiple(serialized_tournament)

        return tournaments_table


class SaveResult:
    def __init__(self, result, tournaments_table, setting_tournament):
        self.result = result
        self.tournaments_table = tournaments_table
        self.User = Query()
        self.setting_tournament = setting_tournament

    def __call__(self):
        id_tournament = getattr(self.setting_tournament, "id_tournament")
        self.tournaments_table.update({'result': self.result},
                                      self.User.id_tournament == id_tournament)


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

        return self.result


class PickPerId:

    def __init__(self, setting_tournament, db_info_player):
        self.setting_tournament = setting_tournament
        self.db_info_player = db_info_player

    def __call__(self):

        players = self.db_info_player.table("Players")
        self.player_dic = {}

        for nm_player in range(len(players.all())):
            print("[" + str(players.all()[nm_player]['id']) + "] " +
                  players.all()[nm_player]['surname'] + ' ' +
                  players.all()[nm_player]['first_name'])

        for nb_player in range(int(self.setting_tournament.NB_PLAYERS)):
            self.player_dic['player ' + str(nb_player + 1)] = None

        for player_to_pick in range(self.setting_tournament.NB_PLAYERS):
            while 1:

                print("\nplayer " + str(player_to_pick + 1))
                pick = input()

                try:
                    player_info = self.db_info_player.table("Players").get(
                        Query().id == int(pick))
                    int(player_info["id"])

                    if pick in self.player_dic.values():
                        print("Already pick")
                    else:
                        break

                except TypeError:
                    print("invalid id")

                except ValueError:
                    print("invalid id")

            self.player_dic["player " + str(player_to_pick + 1)] = pick
            print(self.player_dic.values())

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

        tournaments_table = save_tournament()

        for round in range(self.setting_tournament.nb_round):

            pair_players = PairPlayers(self.setting_tournament,
                                       self.db_info_player, self.result)
            match_to_do = pair_players()

            show_matchs_to_do = ShowMatchsToDo(self.setting_tournament,
                                               match_to_do)
            show_matchs_to_do()

            print("\n")

            for nb_match in range(int(self.setting_tournament.NB_PLAYERS / 2)):
                show_result_input = ShowResultInput(self.setting_tournament,
                                                    match_to_do, nb_match)
                winner_input = show_result_input()

                players_match = [str(list(match_to_do.keys())[nb_match]),
                                 str(list(match_to_do.values())[nb_match])]

                result_round = ResultRound(winner_input, players_match,
                                           self.result)
                self.result = result_round()

                save_result = SaveResult(self.result, tournaments_table,
                                         self.setting_tournament)
                save_result()

        id_tournament = getattr(self.setting_tournament, "id_tournament")
        tournaments_table.update({'status': 1},
                                 Query().id_tournament == id_tournament)


class SortRank:
    def __init__(self, list, db_info_player):
        self.list = list
        self.db_info_player = db_info_player
        self.sorted_list = []

    def __call__(self):
        for nb_players in range(len(self.list)):
            players = self.db_info_player.table("Players").get(
                Query().id == int(self.list[nb_players]))
            self.sorted_list.append(
                " [rank:" + str(players["ranking"]) + "] " + players[
                    "first_name"] + ' ' + players["surname"])

        self.sorted_list.sort(reverse=True)

        for nb_players in range(len(self.sorted_list)):
            print(self.sorted_list[nb_players])
        sort_controller = SortController(self.list, self.db_info_player)
        sort_controller()


class SortAlph:
    def __init__(self, list, db_info_player):
        self.list = list
        self.db_info_player = db_info_player
        self.sorted_list = []

    def __call__(self):
        for nb_players in range(len(self.list)):
            players = self.db_info_player.table("Players").get(
                Query().id == int(self.list[nb_players]))
            self.sorted_list.append(
                players["first_name"] + ' ' + players[
                    "surname"] + " [id:" + str(players["id"]) + "] ")

        sorted_list = sorted(self.sorted_list, key=str.lower)

        for nb_players in range(len(sorted_list)):
            print(sorted_list[nb_players])
        sort_controller = SortController(self.list, self.db_info_player)
        sort_controller()
