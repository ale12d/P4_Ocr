from models import SettingTournament
import json
import os


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
    def __call__(self, root_directory):
        tournament_attributes = json.load(open(root_directory + "\info_tournaments.json"))
        for nm_tournament in tournament_attributes["tournaments"]:
            print(tournament_attributes["tournaments"][nm_tournament]["name_tournament"])


class InputTournaments:
    def __call__(self):
        print("Write the name of the tournament")
        name_tournament = input()

        print("Write the place of the tournament")
        place_tournament = input()

        print("Write the date of the tournament")
        date_tournament = input()

        print("Write the number of round of the tournament  (default=4)")
        nb_round = input()

        print('\nChoice ' + str(SettingTournament.NB_PLAYERS) + ' players :' + '\n')

        return name_tournament, place_tournament, date_tournament, nb_round


class InputPlayers:

    def __call__(self):

        print("Write your name")
        surname = input()

        print("Write your first name")
        first_name = input()

        print("Write your birthday")
        date_of_birth = input()

        print("Write your sex")
        sex = input()

        list_id = []
        player_id = json.load(open(os.getcwd() + "\Players_saved.json"))
        for nb_id in player_id["Players"]:
            list_id.append(player_id["Players"][nb_id]['id'])

        print(list_id)
        id = 1
        while 1:
            if (id in list_id):
                id = id + 1
            else:
                break
        return first_name, surname, id, date_of_birth, sex
