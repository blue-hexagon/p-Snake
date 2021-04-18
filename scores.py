import shelve

scores = []
FILENAME = "highscores.txt"
FILENAME_VAR = FILENAME[:-4]

def init_shelve():
    scores = [['Blaze', 1000], ['Fast Eddy', 900], ['Starcat', 800], ['Hammerhead', 700], ['Mad Hatter', 600],
              ['Primus', 500], ['Tempest', 400], ['Blackbird', 300], ['DragonHawk', 200], ['Wonderboy', 100]]
    d = shelve.open(FILENAME)
    for i in range(0,10):
        d[FILENAME_VAR+str(i)] = scores[i]
        print(d[FILENAME_VAR+ str(i)])
    d.close()
    load_scores()


def load_scores():
    d = shelve.open(FILENAME)
    scores.clear()
    for i in range(0,10):
        scores.append(d[FILENAME_VAR+str(i)])
    d.close()


def update_score(gamescore, player_name="Player"):
    for idx in enumerate(scores):
        if gamescore >= scores[idx[0]][1]:
            with shelve.open(FILENAME,writeback=True) as d:
                d[FILENAME_VAR+str(idx[0])][0] = player_name
                d[FILENAME_VAR+str(idx[0])][1] = gamescore
            scores[idx[0]][1] = gamescore
            scores[idx[0]][0] = player_name
            load_scores()
            break


if __name__ == '__main__':
    pass
