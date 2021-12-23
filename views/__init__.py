import json

class View:

        def ShowPlayers(self, surname, firstname, id):
                print("[" + id + "] " + surname + ' ' +
                      firstname)


        def ShowMod(self):
                print("[1] : Start a tournaments")
                print("[2] : Modify a tournaments")
                print("[3] : Ranking")

        def ShowTournaments(self):

                tournament_attributes = json.load(open(r"C:\Users\AlexC\Desktop\Travail\Projets\P4_objet\controllers\info_tournaments.json"))
                for nm_tournament in tournament_attributes["tournaments"]:
                        print(tournament_attributes["tournaments"][nm_tournament]["name_tournament"])