#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re
import statistics as st
import string
import pandas as pd
import random


def hw():
    print 'Hello, world!'


def lines(fp):
    print str(len(fp.readlines()))


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    word_dict = {}

    for line in sent_file:
        term, score = line.split("\t")
        word_dict[term] = int(score)

    pos_outcomes = []
    neg_outcomes = []

    tweet_list = []
    for line in tweet_file:
        tweet_info = json.loads(line)
        tweet_list.append(tweet_info)

    for tweet in tweet_list:  # tweet is a dictionary
        if 'lang' not in tweet:
            continue
        elif tweet['lang'] != 'en':
            sentiment_level = 0
            continue

        if 'text' not in tweet:
            continue

        encoded_text = tweet['text'].encode('utf-8')
        words = encoded_text.split()
        words = [word.translate(None, string.punctuation) for word in words]
        pos_sent = 0
        neg_sent = 0
        for word in words:
            if word in word_dict:
                if word_dict[word] > 0:
                    pos_sent += word_dict[word]
                elif word_dict[word] < 0:
                    neg_sent -= word_dict[word]

        pos_outcomes.append(pos_sent + random.random() - 0.5)
        neg_outcomes.append(neg_sent + random.random() - 0.5)
    '''
    for i in range(0,51):
        print "pos: " + str(pos_outcomes[i]) + ", neg: " + str(neg_outcomes[i])

    '''
    print len(pos_outcomes)
    sns.set_palette("colorblind", desat=.7)
    df = pd.DataFrame()
    df['positive'] = pos_outcomes
    df['negative'] = neg_outcomes
    max_pos = max(pos_outcomes)
    max_neg = max(neg_outcomes)
    max_num = max_pos if max_pos > max_neg else max_neg

    df.plot(kind='scatter', x='positive', y='negative', title='Positive and Negative Word Sentiments', xlim=[-1, max_num],
            ylim=[-1, max_num])
    plt.show()

    #sns.lmplot('pos', 'neg', data=df, scatter_kws={"marker": "D", "s": 25})
    #plt.xlabel('positive')
    #plt.ylabel('negative')
    #plt.show()

    tweet_file.close()


if __name__ == '__main__':
    main()
