#Building an ETL pipeline in Python
import os
import re
import nltk
import numpy as np
import pandas as pd
import mysql.connector
from textblob import TextBlob
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from wordcloud import WordCloud, STOPWORDS

class tweetObject(object):
    def __init__(self,host,database,user):
        self.password = os.environ['PASSWORD']
        self.host = host
        self.database = database
        self.user = user

    def MySQLConnect(self,query):
        #Connects to database and extracts raw tweets and other
        #Columns that are needed
        try:
                con = mysql.connector.connect(host=self.host,database=self.database,
                                              user = self.user,password = self.password,charset='utf8')
                if con.is_connected():
                    print("Successfully connected to database")
                    cursor = con.cursor()
                    query = query
                    cursor.execute(query)

                    data = cursor.fetchall()
                    #Store in database
                    df = pd.DataFrame(data,columns=['date','tweet'])
                    #print(df.head())
        except Error as e:
            print(e)
        cursor.close()
        con.close()

        return df

    def cleanTweet(self,df):
        #Takes raw tweets and celans them for analysis
        #Text preprocessing
        stop_list = stopwords.words('english')
        ps = PorterStemmer()
        wordnet_lemmatizer = WordNetLemmatizer()
        df['cleanTweets'] = None
        df['len'] = None
        for i in range(0,len(df['tweet'])):
            exclude_list = ['[^a-zA-Z]','rt','http','co','RT']
            exclusions = '|'.join(exclude_list)
            text = re.sub(exclusions,' ',df['tweet'][i])
            text = text.lower()
            words = text.split()
            words = [wordnet_lemmatizer.lemmatize(word) for word in words if not word in stop_list]
            df['cleanTweets'][i] = ' '.join(words)

        #Create column with data length
        df['len'] = np.array([len(tweet) for tweet in data['cleanTweets']])
        return df

    #Define the sentiments in the tweet
    def getSentiment(self,tweet):
        #Returns:
        #1 is positive
        #0 is neutral
        #-1 is negative
        analysis = TextBlob(tweet)
        if analysis.sentiment.polarity>0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def savetofile(self,df):
        #Save cleaned tweets to a csv file
        try:
            df.to_csv("CleanedTweets.csv")
            print("\n")
            print("Tweets saved!\n")
        except Error as e:
            print(e)

    #Generate a wordcloud from the tweets
    def genWordCloud(self,df):
        plt.subplots(figsize=(10,12))
        wordCloud = WordCloud(background_color = 'white',width=1000,
                              height = 800).generate(" ".join(df['cleanTweets']))
        plt.imshow(wordCloud)
        plt.axis('off')
        plt.show()


#Main method
if __name__ == '__main__':
    t = tweetObject(host='localhost',database='twitterdb',user='root')
    data = t.MySQLConnect("SELECT created_at,tweet FROM 'TwitterDB'.'Golf';")
    data['Sentiment'] = np.array([t.sentiment(x) for x in data['cleanTweets']])
    t.genWordCloud(data)
    t.savetofile(data)

    positive_tweets = [tweet for index, tweet in enumerate(data["cleanTweets"]) if data["getSentiment"][index]>0]
    negative_tweets = [tweet for index, tweet in enumerate(data["cleanTweets"]) if data["getSentiment"][index]<0]
    neutral_tweets = [tweet for index, tweet in enumerate(data["cleanTweets"]) if data["getSentiment"][index]==0]
    
    #Print the results
    print("Percentage of positive tweets: {}%".format(100*len(positive_tweets)/len(data['cleanTweets'])))
    print("Percentage of negative tweets: {}%".format(100*len(negative_tweets)/len(data['cleanTweets'])))
    print("Percentage of neutral tweets: {}%".format(100*len(neutral_tweets)/len(data['cleanTweets'])))
