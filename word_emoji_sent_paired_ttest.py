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
import scipy.stats as stats

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

    t_statistic, t_value = stats.ttest_rel(word_outcomes, emoji_outcomes)
    print 't-statistic: ' + str(t_statistic)
    print 'p-value: ' + str(t_value)

    tweet_file.close()


if __name__ == '__main__':
    main()
