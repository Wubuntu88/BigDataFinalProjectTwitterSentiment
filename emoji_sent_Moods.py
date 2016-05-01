#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re
import statistics as st

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def main():
    # sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[1])

    happy_dict = {'😍': 2, '😚': 2, '😃': 2, '😋': 2, '😻': 2, '😘': 2, '💎': 1,
                  '💗': 1, '💖': 1, '💕': 1, '✨': 1, '🌟': 1, '😊': 1,
                  '💝': 1, '💋': 1, '😜': 1, '🎉': 2, '😹': 1, '👏': 1, '👌': 1,
                  '👍': 1, '😛': 1, '😆': 1, '💓': 1, '🌹': 1, '😙': 2, '💙': 1,
                  '😋': 1, '🎈': 1, '💞': 1, '💓': 1, '💍': 1, '👼': 1, '💛': 1,
                  '💚': 1, '😏': 1, '🎂': 1, '🎁': 1, '🎊': 1, '💰': 1, '🏆': 1,
                  '😎': 2, '💟': 1, '👑': 1, '🙏': 1, '🐱': 1, '🍫': 1,
                  '✌️': 2, '☺️': 1, '☺️': 2, '☀️': 1, '❤️': 1, '🍕': 1}

    sad_dict = {'😭': -2, '😔': -1, '💔': -2, '😩': -2, '😢': -2, '😕': -1, '😟': -1,
                '😰': -1, '😝': -1, '😣': -1, '😪': -1, '💤': -1}

    anger_dict = {'😤': -2, '😡': -2, '😠': -1, '😈': -1, '💀': -3, '👊': -1, '🔥': -2,
                  '😾': -2,  '💣': -2, '😼': -1}

    fear_dict = {'😌': 1, '🙈': -1, '😓': -1, '😁': -2, '😖': -2, '😮': -1, '😱': -1,
                 '😒': -1, '😐': -1, '🙉': -1, '🙀': -1, '😶': -1, '😨': -1, '😳': -1,
                 '😷': -3, '🙊': -1}


    happy_sent_count = 0
    sad_sent_count = 0
    anger_sent_count = 0
    fear_sent_count = 0

    happy_sent_level = 0
    sad_sent_level = 0
    anger_sent_level = 0
    fear_sent_level = 0

    # outcomes = []
    # sentiment_level = 0
    en_tweet_count = 0
    sent_freq = 0

    tweet_list = []
    for line in tweet_file:
        tweet_info = json.loads(line)
        tweet_list.append(tweet_info)

    for tweet in tweet_list: # tweet is a dictionary
        if 'lang' not in tweet:
            continue
        elif tweet['lang'] != 'en':
            sentiment_level = 0
            continue

        if 'text' not in tweet:
            continue

        encoded_text = tweet['text'].encode('utf-8')
        sent_found = False
        # happy
        for key in happy_dict.keys():
            matches = re.findall(key, encoded_text)  # list words matched
            count = len(matches)
            if count:
                sent_found = True
                happy_sent_level += happy_dict[key]*count if happy_dict[key] > 0 else -1*happy_dict[key]*count
                happy_sent_count += count
        # sad
        for key in sad_dict.keys():
            matches = re.findall(key, encoded_text)  # list words matched
            count = len(matches)
            if count:
                sent_found = True
                sad_sent_level += sad_dict[key]*count if sad_dict[key] > 0 else -1*sad_dict[key]*count
                sad_sent_count += count

        # anger
        for key in anger_dict.keys():
            matches = re.findall(key, encoded_text)  # list words matched
            count = len(matches)
            if count:
                sent_found = True
                anger_sent_level += anger_dict[key]*count if anger_dict[key] > 0 else -1*anger_dict[key]*count
                anger_sent_count += count

        # fear
        for key in fear_dict.keys():
            matches = re.findall(key, encoded_text)  # list words matched
            count = len(matches)
            if count:
                sent_found = True
                fear_sent_level += fear_dict[key]*count if fear_dict[key] > 0 else -1*fear_dict[key]*count
                fear_sent_count += count

        if sent_found:
            sent_found = False
        en_tweet_count += 1
        #outcomes.append(sentiment_level)
        sentiment_level = 0
    print 'tweet_count: ' + str(en_tweet_count)
    print 'sent_freq: ' + str(sent_freq)
    print 'happy sent count: ' + str(happy_sent_count)
    print 'happy sent level: ' + str(happy_sent_level)

    print 'sad sent count: ' + str(sad_sent_count)
    print 'sad sent level: ' + str(sad_sent_level)

    print 'anger sent count: ' + str(anger_sent_count)
    print 'anger sent level: ' + str(anger_sent_level)

    print 'fear sent count: ' + str(fear_sent_count)
    print 'fear sent level: ' + str(fear_sent_level)
    #mean = st.mean(outcomes)
    #stdev = st.stdev(outcomes)
    #print 'mean: ' + str(mean)
    #print 'stdev: ' + str(stdev)

    # code for generating histogram
    '''
    sns.set_palette("deep", desat=.6)
    my_range = np.arange(int(min(outcomes))-0.5, int(max(outcomes)) + 0.5, 1)
    x_tic_range = np.arange(int(min(outcomes)), int(max(outcomes)), 1)
    plt.hist(outcomes, bins=my_range)
    plt.xticks(x_tic_range)
    plt.xlabel("tweet sentiment score")
    plt.ylabel("quantity of given sentiment")
    plt.title("Frequencies of Sentiment Scores in Tweet Stream")
    plt.show()
    '''
    tweet_file.close()


if __name__ == '__main__':
    main()
