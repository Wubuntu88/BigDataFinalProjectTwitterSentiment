#!/usr/bin/python
# -*- coding: utf-8 -*-

#import matplotlib.pyplot as plt
#import seaborn as sns
#import numpy as np
#import statistics as st
import sys
import json
import re

import string

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

    outcomes = []
    outcomes_mag = []
    sentiment_level = 0
    total_sentiment_level = 0
    sentiment_mag = 0
    total_sentiment_mag = 0
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

        sent_found = False
        encoded_text = tweet['text'].encode('utf-8')

        # calculating emoji sentiment in tweet
        for key in emoji_dict.keys():
            matches = re.findall(key, encoded_text)  # list words matched
            count = len(matches)
            if count:
                sent_found = True
                sentiment_level += emoji_dict[key]*count
                if emoji_dict[key] < 0:
                    sentiment_mag += (-1)*emoji_dict[key]*count
                else:
                    sentiment_mag += emoji_dict[key]*count
       
        # calculating word sentiment in tweet

        words = encoded_text.split()
        words = [word.translate(None, string.punctuation) for word in words]
        for word in words:
            if word in word_dict:
                sentiment_level += word_dict[word]
                sent_found = True
                if word_dict[word] < 0:
                    sentiment_mag += (-1)*word_dict[word]*count
                else:
                    sentiment_mag += word_dict[word]*count

        if sent_found:
            sent_freq += 1
            sent_found = False
        en_tweet_count += 1
        total_sentiment_level += sentiment_level
        total_sentiment_mag += sentiment_mag
        outcomes.append(sentiment_level)
        outcomes_mag.append(sentiment_mag)
        sentiment_level = 0
        sentiment_mag = 0
    print 'tweet_count: ' + str(en_tweet_count)
    print 'sent_freq: ' + str(sent_freq)
    mean = 0
    for value in outcomes:
        mean += value
    mean /= float(len(outcomes))
    stdev = 0
    for value in outcomes:
        stdev += (value - mean)**2
    stdev = (stdev/len(outcomes))**0.5
    #stdev = st.stdev(outcomes)
    mean_mag = 0
    for value in outcomes_mag:
        mean_mag += value
    mean_mag /= float(len(outcomes_mag))
    #mean_mag = st.mean(outcomes_mag)
    stdev_mag = 0
    for value in outcomes_mag:
        stdev_mag += (value - mean_mag)**2
    stdev_mag = (stdev_mag/len(outcomes_mag))**0.5
    #stdev_mag = st.stdev(outcomes_mag)
    print 'mean_level: ' + str(mean)
    print 'stdev_level: ' + str(stdev)
    print 'mean_magnitude: ' + str(mean_mag)
    print 'stdev_magnitude: ' + str(stdev_mag)
    print 'total_sentiment_level: ' + str(total_sentiment_level)
    print 'total_sentiment_magnitude: ' + str(total_sentiment_mag)

    tweet_file.close()


if __name__ == '__main__':
    main()
