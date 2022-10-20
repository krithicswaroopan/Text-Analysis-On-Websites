import os
import re
import pandas as pd
import nltk
from nltk.tokenize import RegexpTokenizer, sent_tokenize
import numpy as np

path = "E:\\Blackcoffee\\Textanalysis\\data\\StopWords"
dir_list = os.listdir(path)#directory list
stopwordlist=[]#list of stop words in all files
for i in range(len(dir_list)):
    with open('E:\\Blackcoffee\\Textanalysis\\data\\StopWords\\'+ dir_list[i] ,'r') as stop_words:
        stopWords = stop_words.read().lower()
        temp = stopWords.split('\n')
        temp[-1:] = []
        stopwordlist = stopwordlist + temp


# positive words list
with open("E:\\Blackcoffee\\Textanalysis\\data\\MasterDictionary\\positive-words.txt",'r') as posfile:
    positivewords=posfile.read().lower()
    positiveWordList=positivewords.split('\n')

# negative words list
with open("E:\\Blackcoffee\\Textanalysis\\data\\MasterDictionary\\negative-words.txt" ,'r') as negfile:
    negativeword=negfile.read().lower()
    negativeWordList=negativeword.split('\n')


#Word count of cleaned text
# Tokenizer
def tokenizer(text):
    text = text.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    filtered_words = list(filter(lambda token: token not in stopwordlist, tokens))
    return filtered_words
    

# positive score 
def positive_score(text):
    numPosWords = 0
    rawToken = tokenizer(text)
    for word in rawToken:
        if word in positiveWordList:
            numPosWords  += 1
    
    sumPos = numPosWords
    return sumPos


# Negative score
def negative_score(text):
    numNegWords=0
    rawToken = tokenizer(text)
    for word in rawToken:
        if word in negativeWordList:
            numNegWords -=1
    sumNeg = numNegWords 
    sumNeg = sumNeg * -1
    return sumNeg


# polarity score
def polarity_score(positiveScore, negativeScore):
    pol_score = (positiveScore - negativeScore) / ((positiveScore + negativeScore) + 0.000001)
    return pol_score


# subjectivity score
def subjectivity_score(positiveScore, negativeScore):
    Sub_Score = (positiveScore + negativeScore) / ((len(fl_words)) + 0.000001)
    return Sub_Score


#average sentence length
def average_sentence_length(text):
    sentence_list = sent_tokenize(text)
    tokens = tokenizer(text)
    totalWordCount = len(tokens)
    totalSentences = len(sentence_list)
    average_sent = 0
    if totalSentences != 0:
        average_sent = totalWordCount / totalSentences
    
    return round(average_sent)


#percentage of complex word
def percentage_complex_word(text):
    tokens = tokenizer(text)
    complexWord = 0
    complex_word_percentage = 0
    
    for word in tokens:
        vowels=0
        if word.endswith(('es','ed')):
            pass
        else:
            for w in word:
                if(w=='a' or w=='e' or w=='i' or w=='o' or w=='u'):
                    vowels += 1
            if(vowels > 2):
                complexWord += 1
    if len(tokens) != 0:
        complex_word_percentage = complexWord/len(tokens)
    
    return (round(complex_word_percentage*100))


#fog Index
def fog_index(averageSentenceLength, percentageComplexWord):
    fogIndex = 0.4 * (averageSentenceLength + percentageComplexWord)
    return fogIndex


#Average Number of Words Per Sentence 
def average_no_words(text):
    sentence_list = sent_tokenize(text)
    tokens = tokenizer(text)
    totalWordCount = len(tokens)
    totalSentences = len(sentence_list)
    if totalSentences != 0:
        average_word = totalWordCount / totalSentences
    
    return round(average_word)


# Counting complex words
def complex_word_count(text):
    tokens = tokenizer(text)
    complexWord = 0
    
    for word in tokens:
        vowels=0
        if word.endswith(('es','ed')):
            pass
        else:
            for w in word:
                if(w=='a' or w=='e' or w=='i' or w=='o' or w=='u'):
                    vowels += 1
            if(vowels > 2):
                complexWord += 1
    return complexWord


#syllable count per word
def syllable_word_count(text):
    tokens = tokenizer(text)
    vowels=0
    for word in tokens:
        if word.endswith(('es','ed')):
            pass
        else:
            for w in word:
                if(w=='a' or w=='e' or w=='i' or w=='o' or w=='u'):
                    vowels += 1
    return vowels



#Personal Pronouns count
def pronoun_count(text):
    tokens = tokenizer(text)
    pronoun = 0
    for w in tokens:
        if(w=='I' or w=='we' or w=='my' or w=='ours' or w=='us'):
            pronoun += 1
    return pronoun



#average word length
def avg_word_length(text):
    tokens = tokenizer(text)
    totalWordCount = len(tokens)
    chars = (text.replace(" ",""))
    totalcharcount = len(chars)
    if totalWordCount !=0:
        avg_len = totalcharcount / totalWordCount
    return(round(avg_len))

    
dirlen = len(os.listdir("E:\\Blackcoffee\\Textanalysis\\Textanalysis\\txt_files"))
ps,ns,pols,subs,asl,pcw,fi,avg_words,cplx_word,Word_count,syll_word,pro_count,wrd_len = ([] for i in range(13))
for i in range(1,dirlen+1):
    text = open(f'E:\\Blackcoffee\\Textanalysis\\Textanalysis\\txt_files\\{i}.txt','r',encoding="utf-8").read()
    fl_words = tokenizer(text)
    ps = ps + [positive_score(text)]
    ns = ns + [negative_score(text)]
    pols = pols + [polarity_score(ps[i-1],ns[i-1])]
    subs = subs + [subjectivity_score(ps[i-1],ns[i-1])]
    asl = asl + [average_sentence_length(text)]
    pcw = pcw + [percentage_complex_word(text)]
    fi = fi + [fog_index(asl[i-1],pcw[i-1])]
    avg_words = avg_words + [average_no_words(text)]
    cplx_word = cplx_word + [complex_word_count(text)]
    Word_count = Word_count+ [len(fl_words)]
    syll_word = syll_word + [syllable_word_count(text)]
    pro_count = pro_count + [pronoun_count(text)]
    wrd_len = wrd_len + [avg_word_length(text)]


df = pd.read_excel('E:\\Blackcoffee\\Textanalysis\\data\\Output Data Structure.xlsx')
df['POSITIVE SCORE'],df['NEGATIVE SCORE'],df['POLARITY SCORE'],df['SUBJECTIVITY SCORE'],df['AVG SENTENCE LENGTH'] = ps,ns,pols,subs,asl
df['PERCENTAGE OF COMPLEX WORDS'],df['FOG INDEX'],df['AVG NUMBER OF WORDS PER SENTENCE'],df['COMPLEX WORD COUNT'],df['WORD COUNT'] = pcw,fi,avg_words,cplx_word,Word_count
df['SYLLABLE PER WORD'],df['PERSONAL PRONOUNS'],df['AVG WORD LENGTH'] = syll_word,pro_count,wrd_len
df.to_excel(excel_writer='E:\Blackcoffee\Textanalysis\Output Data.xlsx')

print("Analysis Completed - Output File Generated")