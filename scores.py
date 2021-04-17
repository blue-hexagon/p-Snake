scores = [['Blaze', 1000], ['Fast Eddy', 900], ['Starcat', 800], ['Hammerhead', 700], ['Mad Hatter', 600],
          ['Primus', 500], ['Tempest', 400], ['Blackbird', 300], ['DragonHawk', 200], ['Wonderboy', 100]]


def update_score(gamescore, player_name="Player"):
    for idx in enumerate(scores):
        if gamescore >= scores[idx[0]][1]:
            scores[idx[0]][1] = gamescore
            scores[idx[0]][0] = player_name
            break


if __name__ == '__main__':
    update_score(225)
    print(scores)
