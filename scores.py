import shelve

highscores = []
FILENAME = "highscores.txt"
FILENAME_VAR = FILENAME[:-4]
global PLAYERNAME


def update_playername():
    with shelve.open(FILENAME, writeback=True) as d:
        d['playername'] = PLAYERNAME


def init_shelve():
    global PLAYERNAME
    scores = [['Blaze', 1000], ['Fast Eddy', 900], ['Starcat', 800], ['Hammerhead', 700], ['Mad Hatter', 600],
              ['Primus', 500], ['Tempest', 400], ['Blackbird', 300], ['DragonHawk', 200], ['Wonderboy', 100]]
    d = shelve.open(FILENAME, writeback=True)
    for i in range(0, 10):
        d[FILENAME_VAR + str(i)] = scores[i]
        print(d[FILENAME_VAR + str(i)])
    d['playername'] = 'Player'
    # PLAYERNAME = 'Player'
    d.close()
    load_scores()


def load_scores():
    global PLAYERNAME
    d = shelve.open(FILENAME)
    highscores.clear()
    for i in range(0, 10):
        highscores.append(d[FILENAME_VAR + str(i)])
    PLAYERNAME = d['playername']
    print(PLAYERNAME)
    d.close()


def update_score(gamescore):
    for idx in enumerate(highscores):
        if gamescore >= highscores[idx[0]][1]:
            with shelve.open(FILENAME, writeback=True) as d:
                d[FILENAME_VAR + str(idx[0])][0] = PLAYERNAME
                d[FILENAME_VAR + str(idx[0])][1] = gamescore
            highscores[idx[0]][1] = gamescore
            highscores[idx[0]][0] = PLAYERNAME
            load_scores()
            break
