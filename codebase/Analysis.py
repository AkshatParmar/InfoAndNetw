from matplotlib import pyplot as plt
from server import vote_tally as vt

def plot():
    presidents, senators = vt()

    ##Senators
    plt.figure()
    ax = plt.subplot()

    s_keys= list(senators.keys())
    s_votes = list(senators.values())

    cmap = plt.cm.get_cmap('hsv', 10)
    sen_n = len(s_keys)
    for i in range(sen_n):
        plt.bar(s_keys[i], s_votes[i], color=cmap(i), edgecolor='black')

    ax.get_yaxis().set_ticks([])
    ax.set_xticklabels(s_votes)
    plt.title('Vote Tally')
    ax.legend(labels=s_keys, title='Candidates')
    plt.savefig('senators.png')


    ###Presidents
    plt.figure()
    ax = plt.subplot()

    p_keys = list(presidents.keys())
    p_votes = list(presidents.values())

    cmap = plt.cm.get_cmap('hsv', 10)
    sen_n = len(p_keys)
    for i in range(sen_n):
        plt.bar(p_keys[i], p_votes[i], color=cmap(i), edgecolor='black')

    ax.get_yaxis().set_ticks([])
    ax.set_xticklabels(p_votes)
    plt.title('Vote Tally')
    ax.legend(labels=p_keys, title = 'Candidates')
    plt.savefig('presidents.png')


if __name__ == "__main__":
    plot()