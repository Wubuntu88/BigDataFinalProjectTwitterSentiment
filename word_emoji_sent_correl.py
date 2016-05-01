#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import re
import statistics as st
import string
import random as random

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    #emoji data structures
    emoji_dict = {'😌': 1, '😤': -2, '😍': 2, '😚': 2, '😭': -2, '😔': -1,
                  '🙈': -1, '😓': -1, '😃': 2, '😋': 2, '😻': 2, '😘': 2, '☺️': 2,
                  '💔': -2, '💗': 1, '💖': 1, '❤️': 1, '💕': 1, '✨': 1, '🌟': 1,
                  '😊': 1, '😁': -2, '😜': 1, '😒': -1, '🎉': 2, '😹': 1, '👏': 1,
                  '🙉': -1, '😆': 1, '🙀': -1, '💝': 1, '💋': 1, '👊': -1, '😋': 1,
                  '😎': 2, '😈': -1, '🎈': 1, '💞': 1, '💀': -3, '😩': -2, '😢': -2,
                  '💓': 1, '💍': 1, '👼': 1, '😕': -1, '😟': -1, '👍': 1, '👌': 1,
                  '💛': 1, '😐': -1, '💚': 1, '🔥': -2, '👑': 1, '😣': -1, '🙏': 1,
                  '😾': -2, '😳': -1, '✌️': 2, '☺️': 1, '😷': -3, '😨': -1, '🍫': 1,
                  '😮': -1, '😱': -1, '🍕': 1, '😼': -1, '💎': 1, '☀️': 1, '😏': 1,
                  '🙊': -1, '💙': 1, '🐱': 1, '💣': -2, '🏆': 1, '😡': -2, '💟': 1,
                  '😶': -1, '💓': 1, '🌹': 1, '😰': -1, '😖': -2, '😝': -1, '😙': 2,
                  '🎂': 1, '🎁': 1, '🎊': 1, '😛': 1, '😠': -1, '💰': 1}

    #emoji_outcomes = []


    word_dict = {}

    for line in sent_file:
        term, score = line.split("\t")
        word_dict[term] = int(score)

    word_outcomes = []
    emoji_outcomes = []
    word_sent_level = 0
    emoji_sent_level = 0
    en_tweet_count = 0
    sent_freq = 0


    tweet_list = []
    for line in tweet_file:
        tweet_info = json.loads(line)
        tweet_list.append(tweet_info)

    for tweet in tweet_list: #tweet is a dictionary
        if 'lang' not in tweet:
            continue
        elif tweet['lang'] != 'en':
            sentiment_level = 0
            continue

        if 'text' not in tweet:
            continue

        encoded_text = tweet['text'].encode('utf-8')

        # calculating emoji sentiment in tweet
        for key in emoji_dict.keys():
            matches = re.findall(key, encoded_text)  # list words matched
            count = len(matches)
            if count:
                emoji_sent_level += emoji_dict[key]*count

        # calculating word sentiment in tweet

        words = encoded_text.split()
        words = [word.translate(None, string.punctuation) for word in words]
        for word in words:
            if word in word_dict:
                word_sent_level += word_dict[word]

        if word_sent_level < -30 or word_sent_level > 17 or emoji_sent_level < -100 or emoji_sent_level > 100:
            print "-------------new outlier-------------"
            print encoded_text
            print 'emoji_sent: ' + str(emoji_sent_level)
            print 'word_sent: ' + str(word_sent_level)

        en_tweet_count += 1
        emoji_outcomes.append(emoji_sent_level)
        word_outcomes.append(word_sent_level)
        emoji_sent_level = 0
        word_sent_level = 0

    emoji_mean = st.mean(emoji_outcomes)
    emoji_stdev = st.stdev(emoji_outcomes)
    word_mean = st.mean(word_outcomes)
    word_stdev = st.stdev(word_outcomes)
    print 'emoji_mean: ' + str(emoji_mean)
    print 'emoji_stdev: ' + str(emoji_stdev)
    print 'word_mean: ' + str(word_mean)
    print 'word_stdev: ' + str(word_stdev)

    '''
    sns.set_palette("muted", desat=.7)
    df = pd.DataFrame()
    df['emoji_sent'] = [outcome+random.random()-0.5 for outcome in emoji_outcomes]
    df['word_sent'] = [outcome+random.random()-0.5 for outcome in word_outcomes]
    #max_pos = max(pos_outcomes)
    #max_neg = max(neg_outcomes)
    #max_num = max_pos if max_pos > max_neg else max_neg

    #df.plot(kind='scatter', x='word_sent', y='emoji_sent', title='emoji_sent vs word_sent correlation')
    sns.jointplot('word_sent', 'emoji_sent', df, color="firebrick")
    #sns.lmplot('word_sent', 'emoji_sent', df)
    plt.show()
    '''
    tweet_file.close()


if __name__ == '__main__':
    main()
