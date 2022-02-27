from models import SettingTournament
from models import SettingRound
from models import SettingMatch
from models import InfoNewPlayer
from views import ShowMod, InputTournaments, InputPlayers, ShowTournaments, ShowModRank, ShowAllPlayers, \
    ShowMatchsToDo, ShowResultInput, ShowPlayerChoose, ShowWinner, ShowAllPlayersId, ShowSortAlph, ShowSortRank, \
    TournamentToLoad, PlayernbToPick, ShowNbRound, InputRanking, ModInput, ModRankInput, ModSortInput, PickInput
from tinydb import TinyDB, Query
from collections import OrderedDict


class ApplicationController:

    def __init__(self):
        pass

    def start(self):
        self.controller = MainMenuController()
        while self.controller:
            self.controller = self.controller()


class StartTournament:
    def __init__(self, db_info_player, db_tournament, db_round, db_match):
        self.db_info_player = db_info_player
        self.db_tournament = db_tournament
        self.db_round = db_round
        self.db_match = db_match

    def __call__(self):
        input_tournaments = InputTournaments(self.db_tournament)
        id_tournament, name_tournament, place_tournament, date_tournament, nb_round, pace = input_tournaments()
        if pace == "1":
            pace = "bullet"
        elif pace == "2":
            pace = "blitz"
        elif pace == "3":
            pace = "fast"
        setting_tournament = SettingTournament(id_tournament, name_tournament, place_tournament, date_tournament,
                                               nb_round, pace)

        return PickPerId(setting_tournament, self.db_info_player, self.db_round, self.db_match, self.db_tournament)


class PairPlayers:

    def __init__(self, setting_tournament, db_info_player):
        self.setting_tournament = setting_tournament
        self.db_info_player = db_info_player
        self.players_wins = {}

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
            players_rank_game[int(self.setting_tournament.players['player ' + str(i + 1)])] = dic_rank_id[int(
                self.setting_tournament.players['player ' + str(i + 1)])]
            sorted_players_rank_game = sorted(players_rank_game.items(), key=lambda kv: kv[1])

        if self.setting_tournament.result == {}:

            for player in range(int(self.setting_tournament.NB_PLAYERS / 2)):
                match_to_do[sorted_players_rank_game[player][0]] = sorted_players_rank_game[player + int(
                    self.setting_tournament.NB_PLAYERS / 2)][0]

            return match_to_do, self.players_wins

        elif self.setting_tournament.result != {}:

            for player in range(len(self.setting_tournament.players)):
                self.players_wins[list(self.setting_tournament.players.values())[player]] = \
                    list(self.setting_tournament.result.values()).count(list(
                        self.setting_tournament.players.values())[player])

            self.players_wins = {k: v for k, v in sorted(self.players_wins.items(), key=lambda item: item[1])}

            list_match = []
            for maxpoint in range(list(self.players_wins.values())[-1] + 1):
                point = []
                rank = {}

                for nb_player in range(len(self.players_wins)):
                    if list(self.players_wins.values())[nb_player] == maxpoint:
                        point.append(list(self.players_wins.keys())[nb_player])

                for i in range(len(point)):
                    player = self.db_info_player.table("Players").get(Query().id == int(point[i]))
                    rank[point[i]] = player["ranking"]

                rank_sorted = {k: v for k, v in sorted(rank.items(), key=lambda item: item[1])}

                for u in range(len(rank_sorted)):
                    list_match.append(list(rank_sorted.keys())[u])

            list_match = list(zip(*[iter(list_match)] * 2))

            for nb_match in range(len(list_match)):
                match_to_do[int(list_match[nb_match][0])] = int(list_match[nb_match][1])

            return match_to_do, self.players_wins


class LoadTournament:
    def __init__(self, db_info_player, db_tournament, db_round,
                 db_match):
        self.db_info_player = db_info_player
        self.db_tournament = db_tournament
        self.db_round = db_round
        self.db_match = db_match

    def __call__(self):
        tournament_list = self.db_tournament.table("tournaments").search(
            Query().status == 0)

        tournaments_to_load = TournamentToLoad(tournament_list)
        tournament_loaded = tournaments_to_load()

        if len(tournament_list) == 0:
            return MainMenuController

        tournament_loaded = self.db_tournament.table("tournaments").get(Query().id_tournament == int(
            tournament_loaded))

        setting_tournament = SettingTournament(tournament_loaded["id_tournament"],
                                               tournament_loaded["name_tournament"],
                                               tournament_loaded["place_tournament"],
                                               tournament_loaded["date_tournament"],
                                               tournament_loaded["nb_round"], tournament_loaded["pace"],
                                               tournament_loaded["result"], **tournament_loaded["players"])

        round_do = len(setting_tournament.result) // (len(setting_tournament.players) / 2)
        start_round = StartRound(setting_tournament, self.db_info_player, self.db_round, self.db_match,
                                 self.db_tournament, int(round_do))
        start_round()


class InputRankingController:
    def __init__(self, setting_tournament, db_tournament, db_info_player):
        self.setting_tournament = setting_tournament
        self.db_tournament = db_tournament
        self.db_info_player = db_info_player

    def __call__(self):
        input_ranking = InputRanking()
        after_round_input = input_ranking()
        players = self.db_info_player.table("Players")

        if after_round_input == "R":
            pick_player_id = PickPlayerId(self.db_tournament, self.db_info_player, self.setting_tournament,
                                          after_round_input)
            while 1:

                player, point = pick_player_id()

                if player == 'E':
                    break
                else:
                    try:
                        float(point)
                        players.update({'ranking': float(player["ranking"]) + float(point)}, Query().id == int(
                            player["id"]))
                    except ValueError:
                        print("incorrect input")
                        pass

        elif after_round_input == "C":
            pass


class PickPlayerId:
    def __init__(self, db_tournament, db_info_player, setting_tournament,
                 after_round_input):
        self.db_tournament = db_tournament
        self.db_info_player = db_info_player
        self.setting_tournament = setting_tournament
        self.after_round_input = after_round_input

    def __call__(self):
        tournament = self.db_tournament.table("tournaments").get(Query().id_tournament == int(
            self.setting_tournament.id_tournament))
        show_player_choose = ShowPlayerChoose(tournament, self.db_info_player)
        player_choose, point = show_player_choose()

        if player_choose == 'E':
            return player_choose, point
        else:
            player = self.db_info_player.table("Players").get(Query().id == int(player_choose))

        return player, point


class MainMenuController:

    def __call__(self):
        db_info_player = TinyDB("Players_saved.json")
        db_tournament = TinyDB("info_tournaments.json")
        db_round = TinyDB("info_db_round.json")
        db_match = TinyDB("info_db_match.json")

        show_mod = ShowMod()
        show_mod()

        while True:
            mod_input = ModInput()
            mod = mod_input()

            option = {
                1: StartTournament(db_info_player, db_tournament, db_round, db_match),
                2: LoadTournament(db_info_player, db_tournament, db_round, db_match),
                3: RankMenuController(db_tournament, db_info_player),
                0: CreatePlayer(db_info_player),
            }

            return option[int(mod)]()


class RankMenuController:
    def __init__(self, db_tournament, db_info_player):
        self.db_tournament = db_tournament
        self.db_info_player = db_info_player

    def __call__(self):

        show_mod_rank = ShowModRank()
        show_mod_rank()

        while True:

            mod_rank_input = ModRankInput()
            mod = mod_rank_input()

            option = {1: ShowAllPlayers(self.db_info_player),
                      2: ShowTournaments(self.db_tournament, mod, self.db_info_player),
                      3: ShowTournaments(self.db_tournament, mod, self.db_info_player),
                      4: ShowTournaments(self.db_tournament, mod, self.db_info_player),
                      5: ShowTournaments(self.db_tournament, mod, self.db_info_player),
                      }

            if int(mod) in [1, 2]:
                list_players = option[int(mod)]()
                sort_controller = SortController(list_players, self.db_info_player)
                sort_controller()
                break

            else:
                option[int(mod)]()
                break


class SortController:
    def __init__(self, list_players, db_info_player):
        self.list_players = list_players
        self.db_info_player = db_info_player

    def __call__(self):
        while True:
            mod_sort_input = ModSortInput()
            sort = mod_sort_input()

            option = {1: SortAlph(self.list_players, self.db_info_player),
                      2: SortRank(self.list_players, self.db_info_player),
                      3: MainMenuController(),
                      }

            return option[int(sort)]()


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
    def __init__(self, setting_tournament, db_tournament, tournaments_table):
        self.setting_tournament = setting_tournament
        self.db_tournament = db_tournament
        self.tournaments_table = tournaments_table

    def __call__(self):
        serialized_tournament = [{
            'id_tournament': getattr(self.setting_tournament, "id_tournament"),
            'name_tournament': getattr(self.setting_tournament, "name_tournament"),
            'place_tournament': getattr(self.setting_tournament, "place_tournament"),
            'date_tournament': getattr(self.setting_tournament, "date_tournament"),
            'nb_round': getattr(self.setting_tournament, "nb_round"),
            'players': getattr(self.setting_tournament, "players"),
            'pace': getattr(self.setting_tournament, "pace"),
            'result': getattr(self.setting_tournament, "result"),
            'status': 0,
        }]

        self.tournaments_table.insert_multiple(serialized_tournament)


class SaveResult:
    def __init__(self, tournaments_table, setting_tournament):
        self.tournaments_table = tournaments_table
        self.User = Query()
        self.setting_tournament = setting_tournament

    def __call__(self):
        id_tournament = getattr(self.setting_tournament, "id_tournament")
        self.tournaments_table.update({'result': self.setting_tournament.result}, self.User.id_tournament ==
                                      id_tournament)


class SaveRound:

    def __init__(self, setting_round, db_round):
        self.setting_round = setting_round
        self.db_round = db_round

    def __call__(self):
        serialized_info = [{
            'id_tournament': getattr(self.setting_round, "id_tournament"),
            'id_round': getattr(self.setting_round, "id_round"),
            'matchs': getattr(self.setting_round, "matchs"),
        }]
        info_round = self.db_round.table("Rounds")
        info_round.insert_multiple(serialized_info)

        return info_round


class SaveMatch:

    def __init__(self, setting_match, db_match):
        self.setting_match = setting_match
        self.db_match = db_match

    def __call__(self):
        serialized_info = [{
            'id_round': getattr(self.setting_match, "id_round"),
            'id_match': getattr(self.setting_match, "id_match"),
            'match': getattr(self.setting_match, "match"),
        }]
        info_match = self.db_match.table("Match")
        info_match.insert_multiple(serialized_info)

        return info_match


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

    def __init__(self, winner, players_match, setting_tournament):
        self.winner = winner
        self.players_match = players_match
        self.setting_tournament = setting_tournament

    def __call__(self):
        self.setting_tournament.result['-'.join(self.players_match)] = self.winner

        return self.setting_tournament


class PickPerId:

    def __init__(self, setting_tournament, db_info_player, db_round, db_match, db_tournament):
        self.setting_tournament = setting_tournament
        self.db_info_player = db_info_player
        self.db_round = db_round
        self.db_match = db_match
        self.db_tournament = db_tournament

    def __call__(self):

        show_all_playerid = ShowAllPlayersId(self.db_info_player)
        show_all_playerid()

        self.player_dic = {}

        for nb_player in range(int(self.setting_tournament.NB_PLAYERS)):
            self.player_dic['player ' + str(nb_player + 1)] = None

        for player_to_pick in range(self.setting_tournament.NB_PLAYERS):
            playernb_to_pick = PlayernbToPick(player_to_pick)

            pick_input = PickInput(self.db_info_player, self.player_dic, playernb_to_pick)
            pick = pick_input()

            self.player_dic["player " + str(player_to_pick + 1)] = pick

        self.setting_tournament.players = self.player_dic
        round = 0
        return StartRound(self.setting_tournament, self.db_info_player, self.db_round, self.db_match,
                          self.db_tournament, round)


class StartRound:
    def __init__(self, setting_tournament, db_info_player, db_round, db_match, db_tournament, round_do):
        self.db_tournament = db_tournament
        self.setting_tournament = setting_tournament
        self.db_info_player = db_info_player
        self.db_round = db_round
        self.db_match = db_match
        self.round_do = round_do

    def __call__(self):

        tournaments_table = self.db_tournament.table("tournaments")

        if self.round_do == 0:
            save_tournament = SaveTournament(self.setting_tournament, self.db_tournament, tournaments_table)

            save_tournament()

        for round in range(self.setting_tournament.nb_round - self.round_do):
            show_nb_round = ShowNbRound(round, self.round_do)
            show_nb_round()

            pair_players = PairPlayers(self.setting_tournament, self.db_info_player)
            match_to_do, players_wins = pair_players()

            show_matchs_to_do = ShowMatchsToDo(self.setting_tournament, match_to_do, self.db_info_player)
            show_matchs_to_do()
            def_id_round = DefIdRound(self.db_round)
            id_round = def_id_round()
            setting_round = SettingRound(self.setting_tournament.id_tournament, id_round, match_to_do)
            save_round = SaveRound(setting_round, self.db_round)
            save_round()

            for nb_match in range(int(self.setting_tournament.NB_PLAYERS / 2)):
                def_id_match = DefIdMatch(self.db_match)
                id_match = def_id_match()
                match = str(list(match_to_do.keys())[nb_match]) + "-" + str(list(match_to_do.values())[nb_match])
                setting_match = SettingMatch(setting_round.id_round, id_match, match)
                save_match = SaveMatch(setting_match, self.db_match)
                save_match()

                show_result_input = ShowResultInput(self.setting_tournament, match_to_do, nb_match,
                                                    self.db_info_player)
                winner_input = show_result_input()

                players_match = [str(list(match_to_do.keys())[nb_match]), str(list(match_to_do.values())[nb_match])]

                result_round = ResultRound(winner_input, players_match, self.setting_tournament)
                self.setting_tournament = result_round()

                save_result = SaveResult(tournaments_table, self.setting_tournament)
                save_result()

            input_ranking_controller = InputRankingController(self.setting_tournament, self.db_tournament,
                                                              self.db_info_player)
            input_ranking_controller()

        id_tournament = getattr(self.setting_tournament, "id_tournament")
        tournaments_table.update({'status': 1}, Query().id_tournament == id_tournament)

        show_winner = ShowWinner(players_wins, self.db_info_player)
        show_winner()


class DefIdRound:
    def __init__(self, db_round):
        self.db_round = db_round

    def __call__(self):

        list_id = []
        rounds = self.db_round.table("Rounds")

        for nb_rounds in range(len(rounds.all())):
            list_id.append(rounds.all()[nb_rounds]['id_round'])

        id = 1
        while 1:
            if id in list_id:
                id = id + 1
            else:
                break

        return id


class DefIdMatch:
    def __init__(self, db_match):
        self.db_match = db_match

    def __call__(self):

        list_id = []
        match = self.db_match.table("Match")

        for nb_matchs in range(len(match.all())):
            list_id.append(match.all()[nb_matchs]['id_match'])

        id = 1
        while 1:
            if id in list_id:
                id = id + 1
            else:
                break

        return id


class SortRank:
    def __init__(self, list, db_info_player):
        self.list = list
        self.db_info_player = db_info_player
        self.sorted_list = []

    def __call__(self):
        for nb_players in range(len(self.list)):
            players = self.db_info_player.table("Players").get(Query().id == int(self.list[nb_players]))
            self.sorted_list.append(" [rank:" + str(players["ranking"]) + "] " + players["first_name"] + ' ' +
                                    players["surname"])

        self.sorted_list.sort(reverse=True)

        show_sort_rank = ShowSortRank(self.sorted_list)
        show_sort_rank()

        sort_controller = SortController(self.list, self.db_info_player)
        sort_controller()


class SortAlph:
    def __init__(self, list, db_info_player):
        self.list = list
        self.db_info_player = db_info_player
        self.sorted_list = {}

    def __call__(self):
        for nb_players in range(len(self.list)):
            players = self.db_info_player.table("Players").get(Query().id == int(self.list[nb_players]))
            self.sorted_list[players["first_name"] + ' ' + players["surname"]] = " [" + str(players["id"]) + "] "
        self.sorted_list = OrderedDict(sorted(self.sorted_list.items(), key=lambda t: t[0]))
        show_sort_alph = ShowSortAlph(self.sorted_list)
        show_sort_alph()

        sort_controller = SortController(self.list, self.db_info_player)
        sort_controller()
