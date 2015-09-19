import random
start_minus_2 = "START2**"
start_minus_1 = "START1**"
end = "END**"

def model_from_corpus(txt_sent):
    D = {}
    for sent in txt_sent:
        s = [start_minus_2, start_minus_1] + sent.split() + [end]
        trigrams = [(s[i], s[i+1], s[i+2]) for i in range(len(s) - 2)]
        for t in trigrams:
            if (t[0], t[1]) in D:
                if t[2] in D[(t[0], t[1])]:
                    D[(t[0], t[1])][t[2]] += 1
                else:
                     D[(t[0], t[1])] = 1
            else:
                 D[(t[0], t[1])] = {t[2]:1}
    return D
