import shelve

scores = []

""" Used to reinitialize the storage """
def init_shelve():
    scores = [['Blaze', 1000], ['Fast Eddy', 900], ['Starcat', 800], ['Hammerhead', 700], ['Mad Hatter', 600],
              ['Primus', 500], ['Tempest', 400], ['Blackbird', 300], ['DragonHawk', 15], ['Wonderboy', 5]]
    d = shelve.open('score.txt')
    for i in range(0,10):
        d['scores'+str(i)] = scores[i]
    for i in range(0,10):
        print("----------------------")
        print(d['scores'+str(i)])
        print("----------------------")
    d.close()


def load_scores():
    d = shelve.open('score.txt')
    scores.clear()
    for i in range(0,10):
        scores.append(d['scores'+str(i)])
    d.close()


def update_score(gamescore, player_name="Player"):
    for idx in enumerate(scores):
        if gamescore >= scores[idx[0]][1]:
            with shelve.open('score.txt',writeback=True) as d:
                d['scores'+str(idx[0])][0] = player_name
                d['scores'+str(idx[0])][1] = gamescore
            scores[idx[0]][1] = gamescore
            scores[idx[0]][0] = player_name
            load_scores()
            break


if __name__ == '__main__':
    pass
    # init_shelve()
    # load_scores()
    # update_score(225)
    # print(scores)
