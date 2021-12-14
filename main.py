from listClass import Tournament, Ranking


def main():

    print("[1] : Start a tournaments")
    print("[2] : Modify a tournaments")
    print("[3] : Ranking")

    mod = input()

    def one():
        tournament = Tournament()
        tournament.start_tournament()

    def two():
        tournament = Tournament()
        tournament.modify_tournament()

    def three():
        ranking = Ranking()
        ranking.show_ranking()

    option = {1: one,
              2: two,
              3: three,
              }

    option[int(mod)]()


if __name__ == "__main__":
    main()
