from models import SettingTournament
from tinydb import Query


class ShowMatchsToDo:

    def __init__(self, setting_tournament, match_to_do, db_info_player):
        self.setting_tournament = setting_tournament
        self.match_to_do = match_to_do
        self.db_info_player = db_info_player

    def __call__(self):
        for nb_match in range(int(self.setting_tournament.NB_PLAYERS / 2)):
            player1 = self.db_info_player.table("Players").get(Query().id == list(self.match_to_do.keys())[nb_match])
            player2 = self.db_info_player.table("Players").get(Query().id == list(self.match_to_do.values())[nb_match])

            print("match n°" + str(nb_match + 1) + " : " + player1["first_name"] + " " + player1["surname"] + " vs " +
                  player2["first_name"] + " " + player2["surname"])

        print("\n")


class ShowNbRound:
    def __init__(self, round, round_do):
        self.round = round
        self.round_do = round_do

    def __call__(self):
        print('\nround ' + str(self.round + 1 + self.round_do) + " : ")


class ShowResultInput:

    def __init__(self, setting_tournament, match_to_do, nb_match, db_info_player):
        self.setting_tournament = setting_tournament
        self.match_to_do = match_to_do
        self.nb_match = nb_match
        self.db_info_player = db_info_player

    def __call__(self):
        player1 = self.db_info_player.table("Players").get(Query().id == list(self.match_to_do.keys())[self.nb_match])
        player2 = self.db_info_player.table("Players").get(Query().id == list(self.match_to_do.values()
                                                                              )[self.nb_match])

        print("result match n°" + str(self.nb_match + 1) + " (" + player1["surname"] + " : [" + str(player1["id"]) +
              "] or " + "[N]" + " or [" + str(player2["id"]) + "] : " + player2["surname"] + ")")
        winner_input = input()

        return winner_input


class ShowAllPlayers:
    def __init__(self, db_info_player):
        self.db_info_player = db_info_player
        self.list_players = []

    def __call__(self):
        players = self.db_info_player.table("Players")

        print("id: name:\n")
        for nm_player in range(len(players.all())):
            print("[" + str(players.all()[nm_player]['id']) + "] " + str(players.all()[nm_player]['first_name']) +
                  " " + str(players.all()[nm_player]['surname']))
            self.list_players.append(str(players.all()[nm_player]['id']))

        return self.list_players


class ShowMatchs:
    def __init__(self, id_input, db_tournament, db_info_player):
        self.id_input = id_input
        self.db_tournament = db_tournament
        self.db_info_player = db_info_player

    def __call__(self):
        tournament = self.db_tournament.table("tournaments").get(Query().id_tournament == int(self.id_input))
        for nb_round in range(tournament["nb_round"]):
            for nb_match in range(int(len(tournament["players"]) / 2)):
                try:

                    winner = self.db_info_player.table("Players").get(Query().id == int(list(tournament["result"][
                                                                                                 list(tournament[
                                                                                                          "result"])[
                                                                                                     nb_match]])[0]))

                    list_match = [int(s) for s in str(
                        list(tournament["result"].keys())[nb_match]).replace('-', ' ').split() if s.isdigit()]

                    player1 = self.db_info_player.table("Players").get(Query().id == list_match[0])

                    player2 = self.db_info_player.table("Players").get(Query().id == list_match[1])

                    print(player1["surname"] + " " + player1["first_name"] + ' vs ' + player2["surname"] + " " +
                          player2["first_name"])

                    print('  winner : ' + winner["first_name"] + " " + winner["surname"] + "\n")

                except IndexError:
                    print("(unfinished)")
                    break
            try:
                list(tournament["result"])[nb_match]
            except IndexError:
                break


class ShowRounds:
    def __init__(self, id_input, db_tournament, db_info_player):
        self.id_input = id_input
        self.db_tournament = db_tournament
        self.db_info_player = db_info_player

    def __call__(self):
        tournament = self.db_tournament.table("tournaments").get(Query().id_tournament == int(self.id_input))

        for nb_round in range(tournament["nb_round"]):

            print("round " + str(nb_round + 1) + ":")
            for nb_match in range(int(len(tournament["players"]) / 2)):
                try:

                    winner = self.db_info_player.table("Players").get(Query().id == int(list(tournament["result"][
                                                                                                 list(tournament[
                                                                                                          "result"])[
                                                                                                     nb_match]])[0]))

                    list_match = [int(s) for s in str(list(tournament["result"].keys())[nb_match]).replace(
                        '-', ' ').split() if s.isdigit()]

                    player1 = self.db_info_player.table("Players").get(Query().id == list_match[0])

                    player2 = self.db_info_player.table("Players").get(Query().id == list_match[1])

                    print(player1["surname"] + " " + player1["first_name"] + ' vs ' + player2["surname"] + " " +
                          player2["first_name"])

                    print('  winner : ' + winner["first_name"] + " " + winner["surname"] + "\n")

                except IndexError:
                    print("(unfinished)")
                    break
            try:
                list(tournament["result"])[nb_match]
            except IndexError:
                break


class ShowPlayers:
    def __init__(self, id_input, db_tournament, db_info_player):
        self.id_input = id_input
        self.db_tournament = db_tournament
        self.db_info_player = db_info_player
        self.list_players = []

    def __call__(self):
        tournament = self.db_tournament.table("tournaments").get(Query().id_tournament == int(self.id_input))
        for nb_players in range(len(list(tournament["players"].values()))):
            players = self.db_info_player.table("Players").get(Query().id == int(list(tournament["players"].values()
                                                                                      )[nb_players]))
            self.list_players.append(players["id"])
        print(self.list_players)
        for nb_player in range(len(self.list_players)):
            player = self.db_info_player.table("Players").get(Query().id == self.list_players[nb_player])
            print('[' + str(player['id']) + '] ' + player['first_name'] + ' ' + player['surname'])

        return self.list_players


class ShowWinner:
    def __init__(self, players_wins, db_info_player):
        self.players_wins = players_wins
        self.db_info_player = db_info_player

    def __call__(self):
        player = self.db_info_player.table("Players").get(Query().id == int(list(self.players_wins.keys())[-1]))

        print("\nwinner : " + player['first_name'] + " " + player['surname'])


class ShowMod:
    def __call__(self):
        print("[1] : Start a tournaments")
        print("[2] : Load a tournaments")
        print("[3] : Report")
        print("\n[0] : Add new player")


class ShowModRank:
    def __call__(self):
        print("[1] : List all players")
        print("[2] : List of tournament players")
        print("[3] : List all tournament")
        print("[4] : List of tournament rounds")
        print("[5] : List of tournament matchs")


class ShowTournaments:
    def __init__(self, db_tournament, mod, db_info_player):
        self.db_tournament = db_tournament
        self.mod = mod
        self.db_info_player = db_info_player

    def __call__(self):

        print("id: name:\n")
        tournament = self.db_tournament.table("tournaments")
        for nb_tournament in range(len(tournament.all())):
            print("[" + str(
                tournament.all()[nb_tournament]["id_tournament"]) + "] " + str(
                tournament.all()[nb_tournament]["name_tournament"]))

        if int(self.mod) == 2:
            id_input = input("Which tournament ? : \n")
            show_players = ShowPlayers(id_input, self.db_tournament, self.db_info_player)
            list_players = show_players()
            return list_players

        if int(self.mod) == 4:
            id_input = input("Which tournament ? : \n")
            show_rounds = ShowRounds(id_input, self.db_tournament, self.db_info_player)
            show_rounds()

        if int(self.mod) == 5:
            id_input = input("Which tournament ? : \n")
            show_matchs = ShowMatchs(id_input, self.db_tournament, self.db_info_player)
            show_matchs()


class ShowAllPlayersId:
    def __init__(self, db_info_player):
        self.db_info_player = db_info_player

    def __call__(self):
        players = self.db_info_player.table("Players")

        for nm_player in range(len(players.all())):
            print("[" + str(players.all()[nm_player]['id']) + "] " + players.all()[nm_player]['surname'] + ' ' +
                  players.all()[nm_player]['first_name'])


class InputTournaments:

    def __init__(self, db_tournament):
        self.db_tournament = db_tournament

    def __call__(self):

        # Input name_tournament
        while True:
            name_tournament = input("Write the name of the tournament : ")

            try:
                name_tournament = str(name_tournament)
                break

            except ValueError:
                print("incorrect input")

        # Input place_tournament
        while True:
            place_tournament = input("Write the place of the tournament : ")

            try:
                place_tournament = str(place_tournament)
                break

            except ValueError:
                print("incorrect input")

        # Input date_tournament
        while True:
            date_entry = input('Enter a date in YYYY-MM-DD format : ')
            try:
                year, month, day = map(int, date_entry.split('-'))
                date_tournament = year, month, day
                break

            except ValueError:
                print("incorrect input")

        # Input nb_round
        while True:
            nb_round = input(
                "Write the number of round of the tournament  (default=4) : ")

            try:
                nb_round = int(nb_round)
                break

            except ValueError:
                print("Don't write letters in the date")

        while True:
            pace = input(
                "Choose the pace of the tournament ([1] : bullet  -  [2] : blitz  -  [3] : fast) : ")
            if pace not in ["1", "2", "3"]:
                print('That\'s not an correct answer (1, 2 or 3)')
            else:
                break

        print('\nChoice ' + str(
            SettingTournament.NB_PLAYERS) + ' players :' + '\n')

        list_id = []
        tournament = self.db_tournament.table("tournaments")

        for nb_tournament in range(len(tournament.all())):
            list_id.append(tournament.all()[nb_tournament]['id_tournament'])

        id_tournament = 1
        while 1:
            if id_tournament in list_id:
                id_tournament = id_tournament + 1
            else:
                break

        return \
            id_tournament, name_tournament, place_tournament, date_tournament, nb_round, pace


class InputPlayers:
    def __init__(self, db_info_player):
        self.db_info_player = db_info_player

    def __call__(self):

        # Input surname
        while True:
            surname = input("Write your name : ")

            try:
                surname = str(surname)
                break

            except ValueError:
                print("incorrect input")

        # Input first_name
        while True:
            first_name = input("Write your first name : ")
            try:
                first_name = str(first_name)
                break

            except ValueError:
                print("incorrect input")

        # Input date_of_birth
        while True:
            date_entry = input('Enter a date in YYYY-MM-DD format : ')
            try:
                year, month, day = map(int, date_entry.split('-'))
                date_of_birth = year, month, day
                break

            except ValueError:
                print("incorrect input")

        # Input sex
        while True:
            sex = input("Write your sex (M/W) : ")
            if sex not in ["M", "W"]:
                print('That\'s not an correct answer (M or W)')
            else:
                break

        list_id = []
        players = self.db_info_player.table("Players")

        for nb_players in range(len(players.all())):
            list_id.append(players.all()[nb_players]['id'])

        id = 1
        while 1:
            if id in list_id:
                id = id + 1
            else:
                break

        return first_name, surname, id, date_of_birth, sex


class InputRanking:
    def __call__(self):
        while 1:
            after_round_input = input("edit ranking point - enter [R] | next - enter [N] : ")

            if after_round_input not in ["R", "N"]:
                print("incorrect input")

            else:
                break

        return after_round_input


class ShowPlayerChoose:
    def __init__(self, tournament, db_info_player):
        self.tournament = tournament
        self.db_info_player = db_info_player
        self.point = 0

    def __call__(self):
        for nb_players in range(len(self.tournament['players'])):
            player = self.db_info_player.table("Players").get(Query().id == int(list(self.tournament['players'].
                                                                                     values())[nb_players]))

            print("[" + list(self.tournament['players'].values())[nb_players] + "] " + player["first_name"] + " " +
                  player["surname"])

        player_choose = input("Choose the player to edit rank | E to exit: ")

        if player_choose == 'E':
            return player_choose, self.point
        else:
            player = self.db_info_player.table("Players").get(Query().id == int(player_choose))

            print(player["first_name"] + " " + player['surname'] + " : " + str(player["ranking"]))
            self.point = input("add or remove point : ")

            return player_choose, self.point


class ShowSortAlph:
    def __init__(self, sorted_list):
        self.sorted_list = sorted_list

    def __call__(self):
        for nb_players in range(len(self.sorted_list)):
            print(list(self.sorted_list.values())[nb_players] + " " +
                  list(self.sorted_list.keys())[nb_players])


class ShowSortRank:
    def __init__(self, sorted_list):
        self.sorted_list = sorted_list

    def __call__(self):
        for nb_players in range(len(self.sorted_list)):
            print(self.sorted_list[nb_players])


class TournamentToLoad:
    def __init__(self, tournament_list):
        self.tournament_list = tournament_list

    def __call__(self):

        if len(self.tournament_list) == 0:
            print("\nno tournaments to load \n")

            return

        for nb_tournament in range(len(self.tournament_list)):
            print("[" + str(self.tournament_list[nb_tournament]['id_tournament']) + "] " + self.
                  tournament_list[nb_tournament]['name_tournament'])

        tournament_loaded = input("Which tournament ? : ")

        return tournament_loaded


class PlayernbToPick:
    def __init__(self, player_to_pick):
        self.player_to_pick = player_to_pick

    def __call__(self):
        print("\nplayer " + str(self.player_to_pick + 1) + " :")


class ModInput:
    def __call__(self):
        while 1:
            mod = input('\nChoose an option from among these (1,2,3,0) :')

            if int(mod) in [1, 2, 3, 0]:
                return mod

            else:
                print('That\'s not an option!')


class ModRankInput:
    def __call__(self):
        while 1:
            mod = input('\nChoose an option from among these (1,2,3,4,5) :')

            if int(mod) in [1, 2, 3, 4, 5]:
                return mod

            else:
                print('That\'s not an option!')


class ModSortInput:
    def __call__(self):
        while 1:
            sort = input('\n[1]:Sort by alphabetical order   [2]:Sort by ranking   [3]:Exit to main menu\n')

            if int(sort) in [1, 2, 3]:
                return sort

            else:
                print('That\'s not an option!')


class PickInput:
    def __init__(self, db_info_player, player_dic, playernb_to_pick):
        self.db_info_player = db_info_player
        self.player_dic = player_dic
        self.playernb_to_pick = playernb_to_pick

    def __call__(self):
        while 1:

            self.playernb_to_pick()
            pick = input()

            try:
                player_info = self.db_info_player.table("Players").get(Query().id == int(pick))
                int(player_info["id"])

                if pick in self.player_dic.values():
                    print("Already pick")
                else:
                    return pick

            except TypeError:
                print("invalid id")

            except ValueError:
                print("invalid id")
