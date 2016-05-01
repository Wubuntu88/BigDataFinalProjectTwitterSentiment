#!/usr/bin/python
import sys
import json
import matplotlib.pyplot as plt
import numpy as np

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    scores = {}
    sentiment_level = 0
    sent_num = 0
    no_sent_num = 0

    outcomes = []

    for line in sent_file:
        term, score = line.split("\t")
        scores[term] = int(score)

    tweet_list = []
    #limit = 50
    for line in tweet_file:
        tweet_info = json.loads(line)
        tweet_list.append(tweet_info)
        '''
        if limit <= 0:
            break
        else:
            limit -= 1
        '''

    for tweet in tweet_list: #tweet is a dictionary
        items = tweet.items() #items is a list of ...???
        #print "--------------NEW TWEET----------------"
        for item in items:

            #print "item length:" + str(len(item))
            encoded1 = item[0]
            if encoded1 == "lang":
                encoded2 = item[1].encode('utf-8')
                if encoded2 != 'en':
                    continue
            elif encoded1 == "text":
                encoded2 = item[1].encode('utf-8')
                word_list = encoded2.split(" ")
                for word in word_list:
                    if word in scores:
                        sentiment_level += scores[word]
                if sentiment_level != 0:
                    outcomes.append(sentiment_level)
                if sentiment_level:
                    if sentiment_level <= -14:
                        print encoded2
                    #print "-------TWEET WITH SENTIMENT-----------"
                    #print sentiment_level
                    #print encoded1
                    #print encoded2
                    sent_num += 1
                else:
                    no_sent_num += 1

            sentiment_level = 0

    '''
    my_range = np.arange(int(min(outcomes)), int(max(outcomes)) + 1, 1)
    plt.hist(outcomes, bins=my_range)
    plt.xticks(my_range)
    plt.xlabel("tweet sentiment score")
    plt.ylabel("quantity of given sentiment")
    plt.show()
    '''

    #print "# have sentiment: " + str(sent_num)
    #print "# do not have sentiment: " + str(no_sent_num)


if __name__ == '__main__':
    main()
