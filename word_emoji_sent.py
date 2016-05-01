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
    sentiment_level = 0
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

        # calculating word sentiment in tweet

        words = encoded_text.split()
        words = [word.translate(None, string.punctuation) for word in words]
        for word in words:
            if word in word_dict:
                sentiment_level += word_dict[word]
                sent_found = True

        if sent_found:
            sent_freq += 1
            sent_found = False
        en_tweet_count += 1
        outcomes.append(sentiment_level)
        sentiment_level = 0
    print 'tweet_count: ' + str(en_tweet_count)
    print 'sent_freq: ' + str(sent_freq)
    mean = st.mean(outcomes)
    stdev = st.stdev(outcomes)
    print 'mean: ' + str(mean)
    print 'stdev: ' + str(stdev)

    sns.set_palette("colorblind")
    my_range = np.arange(int(min(outcomes))-0.5, int(max(outcomes)) + 0.5, 1)
    x_tic_range = np.arange(int(min(outcomes)), int(max(outcomes)), 1)
    plt.hist(outcomes, bins=my_range)
    plt.xticks(x_tic_range)
    plt.xlabel("tweet sentiment score")
    plt.ylabel("quantity of given sentiment")
    plt.title("Frequencies of Sentiment Scores in Tweet Stream")
    plt.show()

    tweet_file.close()


if __name__ == '__main__':
    main()
