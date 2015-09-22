# -*- coding: utf-8 -*-
import serial,ast
import os, ast, tweepy, random, math, time, sys
reload(sys)
sys.setdefaultencoding('utf-8')
start_minus_2 = "START2**"
start_minus_1 = "START1**"
end = "END**"

ser = serial.Serial("COM8", 9600, timeout = 3)
connected = False
calibrated = False
print('waiting to connect')

while ((not connected) and (not calibrated)):
    newline = ast.literal_eval(ser.readline())
    print('connected')
    print(newline)
    connected = True

minlight = float('inf')
maxlight = -float('inf')
minflex1 = float('inf')
maxflex1 = -float('inf')
minflex2 = float('inf')
maxflex2 = -float('inf')
minflex3 = float('inf')
maxflex3 = -float('inf')
minflex4 = float('inf')
maxflex4 = -float('inf')
minflex5 = float('inf')
maxflex5 = -float('inf')
sensormin = [minlight,minflex1,minflex2,minflex3,minflex4,minflex5]
sensormax = [maxlight,maxflex1,maxflex2,maxflex3,maxflex4,maxflex5]

while (connected and (not calibrated)):
    newline = ast.literal_eval(ser.readline()[0:-1])
    if newline == 'calibration done':
        calibrated = True
        print('calibration done')
        print sensormin
        print sensormax
    else:
        for x in range(0,6):
            sensormin[x] = min(sensormin[x],newline[x])
            sensormax[x] = max(sensormax[x],newline[x])         
#       print(newline)


with open(os.path.expanduser('~/Desktop/model.csv')) as f:
    content = f.readlines()
    wts = ast.literal_eval(str(content[0]))
    model = ast.literal_eval(str(content[1]))
    bigram_failsafe = ast.literal_eval(str(content[2]))
    f.close()

with open(os.path.expanduser('~/Desktop/top_secret.txt')) as f:
    content = f.readlines()
    consumer_key = content[1]
    consumer_secret = content[3]
    access_token = content[5]
    access_token_secret = content[7]

auth = tweepy.OAuthHandler(consumer_key[:-1], consumer_secret[:-1])
auth.set_access_token(access_token[:-1], access_token_secret[:-1])

api = tweepy.API(auth)

def first():
    # [text1,text2]=random.sample(wts.keys(),2)
    text1 = 'potato'
    text2 = 'potato'
    while text1 == text2:
        newline = ast.literal_eval(ser.readline())
        for x in range(0,6):
            newline[x] = float(newline[x]-sensormin[x])/float(sensormax[x]-sensormin[x])
        for x in range(6,8):
            if newline[x]=='HIGH':
                newline[x] = 1
            else:
                newline[x] = 0
        print(newline)
        photot = newline[0]
        flex1t = newline[1]
        flex2t = newline[2]
        flex3t = newline[3]
        flex4t = newline[4]
        flex5t = newline[5]
        tiltt = newline[6]
       # toucht = newline[7]
        text1 = wts.keys()[int(5.0 * float(photot))]
        print photot
        print flex1t
        text2 = wts.keys()[int(5.0 * float(flex1t))]
    return (text1, text2)

def rectify_prob(tx1, tx2, size1, size2, next_word_dist, seed):
    if size1 > size2 * 1.2:
        how_larger = size1/size2
        how_many = 0
        while how_many < how_larger:
            for i in tx2[seed].keys():
                for j in range(tx2[seed][i]):
                    next_word_dist.append(i)
            how_many += 1
    elif size2 > size1 * 1.2:
        how_larger = size2/size1
        how_many = 0
        while how_many < how_larger:
            for i in tx1[seed].keys():
                for j in range(tx1[seed][i]):
                    next_word_dist.append(i)
            how_many += 1
    return next_word_dist

def tweet():
    (text1, text2) = first()
    print text1
    print text2
    dist1 = model[text1]
    dist2 = model[text2]
    bdist1 = bigram_failsafe[text1]
    bdist2 = bigram_failsafe[text2]
    print type(dist1)
    max_tweet_len = 140
    end_reached = False
    most_recent = (start_minus_2, start_minus_1)
    tweet = ''
    seen = set()
    good = True
    start = time.time()
    while end_reached == False and time.time()-start < 15.0:
        newline = ast.literal_eval(ser.readline()[0:-1])
        print newline
        for x in range(0,6):
            newline[x] = float(newline[x]-sensormin[x])/float(sensormax[x]-sensormin[x])
        for x in range(6,8):
            if newline[x]=='HIGH':
                newline[x] = 1
            else:
                newline[x] = 0
#       print(newline)
        photot = newline[0]
        flex1t = newline[1]
        flex2t = newline[2]
        flex3t = newline[3]
        flex4t = newline[4]
        flex5t = newline[5]
        tiltt = newline[6]
        #toucht = newline[7]
        try:
            next_word_dist = []
            if most_recent in dist1:
                for i in dist1[most_recent].keys():
                    for j in range(dist1[most_recent][i]):
                        next_word_dist.append(i)
            elif most_recent in dist2:
                for i in dist2[most_recent].keys():
                    for j in range(dist2[most_recent][i]):
                        next_word_dist.append(i)
            if len(next_word_dist) < 3 or tiltt == 1:
                next_word_dist = []
                if most_recent[1] in bdist1:
                    for k in bdist1[most_recent[1]].keys():
                        for l in range(bdist1[most_recent[1]][k]):
                            next_word_dist.append(k)
                elif most_recent[1] in bdist2:
                    for k in bdist2[most_recent[1]].keys():
                        for l in range(bdist2[most_recent[1]][k]):
                            next_word_dist.append(k)
                            #def rectify_prob(tx1, tx2, size1, size2, next_word_dist, seed):
                rectify_prob(bdist1, bdist2, float(wts[text1]), float(wts[text2]), next_word_dist, most_recent[1])
            else:
                rectify_prob(dist1, dist2, float(wts[text1]), float(wts[text2]), next_word_dist, most_recent)

            ch = random.choice([flex1t, flex2t, flex3t, flex4t, flex5t])
            next_word = next_word_dist[int(round(float(len(next_word_dist)) * float(ch)))-1]
            if next_word == end :
                end_reached = True
            else:
                tweet += next_word + ' '
                most_recent = (most_recent[1], next_word)
        except KeyError:
            pass
    return (tweet, float(int(photot))%2.0)


for i in range(20):
    tw=""
    try:
        tw = tweet()[0]
        if len(tw) <= 140 and len(tw)>0:
            api.update_status(status = str(tw))
        print tw
    except:
        print 'well shit'

##api.update_status(status = "hello world! stay tuned for some dank updates!")

#ser.close()
#print('connection closed')