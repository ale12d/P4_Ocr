from models import SettingTournament
from tinydb import Query


class ShowMatchsToDo:

    def __init__(self, setting_tournament, match_to_do):
        self.setting_tournament = setting_tournament
        self.match_to_do = match_to_do

    def __call__(self):
        for nb_match in range(int(self.setting_tournament.NB_PLAYERS / 2)):
            print("match n°" + str(nb_match + 1) + " : " + str(
                list(self.match_to_do.keys())[nb_match]) + " vs " + str(
                list(self.match_to_do.values())[nb_match]))


class ShowResultInput:

    def __init__(self, setting_tournament, match_to_do, nb_match):
        self.setting_tournament = setting_tournament
        self.match_to_do = match_to_do
        self.nb_match = nb_match

    def __call__(self):
        print("result match n°" + str(self.nb_match + 1) + " ([" + str(
            list(self.match_to_do.keys())[
                self.nb_match]) + "] or " + "[N]" + " or [" + str(
            list(self.match_to_do.values())[self.nb_match]) + "]) :")
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
            print("[" + str(players.all()[nm_player]['id']) + "] " + str(
                players.all()[nm_player]['first_name']) + " " + str(
                players.all()[nm_player]['surname']))
            self.list_players.append(str(
                players.all()[nm_player]['id']))

        return self.list_players


class ShowMatchs:
    def __init__(self, id_input, db_tournament):
        self.id_input = id_input
        self.db_tournament = db_tournament

    def __call__(self):
        tournament = self.db_tournament.table("tournaments").get(
            Query().id_tournament == int(self.id_input))
        print(tournament["result"])


class ShowRounds:
    def __init__(self, id_input, db_tournament):
        self.id_input = id_input
        self.db_tournament = db_tournament

    def __call__(self):
        tournament = self.db_tournament.table("tournaments").get(
            Query().id_tournament == int(self.id_input))

        for nb_round in range(tournament["nb_round"]):
            print("round " + str(nb_round + 1) + ":")
            for nb_match in range(int(len(tournament["players"]) / 2)):
                try:
                    print(list(tournament["result"])[
                              nb_match] + '  winner : ' +
                          str(list(tournament["result"][
                            list(tournament["result"])[nb_match]])))
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
        tournament = self.db_tournament.table("tournaments").get(
            Query().id_tournament == int(self.id_input))
        for nb_players in range(len(list(tournament["players"].values()))):
            players = self.db_info_player.table("Players").get(
                Query().id == int(
                    list(tournament["players"].values())[nb_players]))
            self.list_players.append(players["id"])
        return self.list_players


class ShowMod:
    def __call__(self):
        print("[1] : Start a tournaments")
        print("[2] : Load a tournaments")
        print("[3] : Ranking")
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
            show_players = ShowPlayers(id_input, self.db_tournament,
                                       self.db_info_player)
            show_players()

        if int(self.mod) == 4:
            id_input = input("Which tournament ? : \n")
            show_rounds = ShowRounds(id_input, self.db_tournament)
            show_rounds()

        if int(self.mod) == 5:
            id_input = input("Which tournament ? : \n")
            show_matchs = ShowMatchs(id_input, self.db_tournament)
            show_matchs()


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
            id_tournament, name_tournament, place_tournament, date_tournament,\
            nb_round


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
