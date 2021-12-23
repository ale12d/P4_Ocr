class SettingTournament:

    NB_PLAYERS = 8

    @staticmethod
    def __init__(self, name_tournament, place_tournament, date_tournament, nb_round=4, **players):

        self.name_tournament = name_tournament
        self.place_tournament = place_tournament
        self.date_tournament = date_tournament
        self.nb_round = nb_round
        self.players = players
