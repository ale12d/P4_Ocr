class SettingTournament:
    NB_PLAYERS = 8

    def __init__(self, id_tournament, name_tournament, place_tournament, date_tournament, nb_round=4, pace=0,
                 result={}, **players, ):
        self.id_tournament = id_tournament
        self.name_tournament = name_tournament
        self.place_tournament = place_tournament
        self.date_tournament = date_tournament
        self.nb_round = nb_round
        self.pace = pace
        self.players = players
        self.result = result
