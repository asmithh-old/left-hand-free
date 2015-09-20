# -*- coding: utf-8 -*-
import random, os.path, re, json, ast, sys
reload(sys)
sys.setdefaultencoding('utf-8')
start_minus_2 = "START2**"
start_minus_1 = "START1**"
end = "END**"

all_model_prob = {}
sent_wts = {}
bigram_failsafe = {}

def model_from_corpus(txt_sent):
    D = {}
    B = {}
    for sent in txt_sent:
        s = [start_minus_2, start_minus_1] + sent.split() + [end]
        trigrams = [(s[i], s[i+1], s[i+2]) for i in range(len(s) - 2)]
        bigrams = [(s[i], s[i+1]) for i in range(1, len(s) - 1)]
        for b in bigrams:
            if (b[0]) in B:
                if b[1] in B[b[0]]:
                    B[b[0]][b[1]] += 1
                else:
                    B[b[0]][b[1]] = 1
            else:
                B[b[0]] = {b[1]: 1}
        for t in trigrams:
            if (t[0], t[1]) in D:
                if t[2] in D[(t[0], t[1])]:
                    D[(t[0], t[1])][t[2]] += 1
                else:
                     D[(t[0], t[1])][t[2]] = 1
            else:
                 D[(t[0], t[1])] = {t[2]:1}

    return (D, B)

def make_txt(doc):
    with open(os.path.expanduser(doc)) as f:
        content = f.readlines()
        p =  ' '.join(content)
        p = re.sub("\n|[^a-zA-Z\ .,;:']", '', p).lower()
        p = re.sub(",", " ,", p)
        p = re.sub(":", " :", p)
        p = re.sub(";", " ;", p)
        txt_sent = p.split('.')
        f.close()
    return (txt_sent, len(txt_sent))

txts = [('~/Desktop/meangirls.txt', 'mean girls'), ('~/Desktop/Iliad.txt', 'Iliad'),('~/Desktop/Dostoevsky.txt', 'Dostoevsky'), ('~/Desktop/Shakespeare.txt', 'Shakespeare'), ('~/Desktop/clrs.txt', 'clrs'), ("~/Desktop/jamie.txt", "ja'mie")]

for i in txts:
    (filename, name) = i
    m = make_txt(filename)
    da = model_from_corpus(m[0])
    all_model_prob[name] = da[0]
    bigram_failsafe[name] = da[1]
    sent_wts[name] = m[1]
with open(os.path.expanduser('~/Desktop/model.csv'), 'w') as c:
    c.write(str(sent_wts))
    c.write('\n')
    c.write(str(all_model_prob))
    c.write('\n')
    c.write(str(bigram_failsafe))
    c.close()
