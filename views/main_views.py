from models import SettingTournament



class ShowPlayers:
    def __call__(self, surname, firstname, id):
        print("[" + str(id) + "] " + surname + ' ' +
              firstname)


class ShowMod:
    def __call__(self):
        print("[1] : Start a tournaments")
        print("[2] : Modify a tournaments")
        print("[3] : Ranking")
        print("\n[0] : Add new player")


class ShowTournaments:
    def __call__(self, root_directory, db_tournament):

        print("Load tournament :\n")
        tournament = db_tournament.table("tournaments")
        for nb_tournament in range(len(tournament.all())):
            print(tournament.all()[nb_tournament]["name_tournament"])


class InputTournaments:
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

        #Input nb_round
        while True:
            nb_round = input("Write the number of round of the tournament  (default=4) : ")

            try:
                nb_round = int(nb_round)
                break

            except ValueError:
                print("Don't write letters in the date")

        print('\nChoice ' + str(SettingTournament.NB_PLAYERS) + ' players :' + '\n')

        return name_tournament, place_tournament, date_tournament, nb_round


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
            if (id in list_id):
                id = id + 1
            else:
                break

        return first_name, surname, id, date_of_birth, sex
