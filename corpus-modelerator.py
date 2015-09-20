import random, os.path, re, json, ast
start_minus_2 = "START2**"
start_minus_1 = "START1**"
end = "END**"

all_model_prob = {}
sent_wts = {}

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
                     D[(t[0], t[1])][t[2]] = 1
            else:
                 D[(t[0], t[1])] = {t[2]:1}

    return D

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

txts = [('~/Desktop/Iliad.txt', 'Iliad'),('~/Desktop/Dostoevsky.txt', 'Dostoevsky'), ('~/Desktop/Shakespeare.txt', 'Shakespeare'), ('~/Desktop/clrs chapters 1-6.txt', 'clrs'), ("~/Desktop/Season 1 Ja'mie.txt", "ja'mie")]

for i in txts:
    (filename, name) = i
    m = make_txt(filename)
    all_model_prob[name] = model_from_corpus(m[0])
    sent_wts[name] = m[1]
with open(os.path.expanduser('~/Desktop/model.csv'), 'w') as c:
    c.write(str(sent_wts))
    c.write('\n')
    c.write(str(all_model_prob))
    c.close()
