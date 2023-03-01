# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 13:39:02 2021

@author: Florenthia Kezia - Josie Esthaliani
"""

import spacy
import pickle

## spacy object
nlp = spacy.load("en_core_web_sm")

## input text
TEXT = ["the morning drive was great", "that was a great morning drive", "he saw a beautiful girl with a telescope", "her daughter is beautiful", "great draft and bottle selection, and the pizza's delicious", "the pizza's delicious"]

POSITIVES = pickle.load(open('posDict.pickle', 'rb'))

NEGATIVES = pickle.load(open('negDict.pickle', 'rb'))
    
def getTree():
    ## use this function to trace dep tree, it helps 
    ## (making rules may be very confusing if you don't see the tree)
    for txt in TEXT:
        ## transform txt to nlp object from spacy
        doc = nlp(txt)
        for token in doc:
            # print what you need here
            print(token.text, token.dep_, token.head.text, token.head.pos_,
            [child for child in token.children])
        print("")

def aspectDescriptionExtraction(stc):
    global nlp
    
    ## since 1 text can produce more than 1 pair, use list to store the pair(s) set
    aspDesList = []
    
    # make nlp object for stc
    doc = nlp(stc)
    
## these variables are nodes ---------------------------------------------
    ## object's head node
    objHead = None
    ## object node
    obj = None
    ## description's head node
    desHead = None
    ## description node
    des = None
## -----------------------------------------------------------------------
    
    ## find noun-adj pair(s) in sentence        
    
    ## iterate token in doc (each token is node)
    for token in doc:
        ## check whether token is object (objects can be noun / verb)
        if (token.pos_ in ['NOUN', 'VERB']):
            obj = token
            objHead = token.head
        elif (token.pos_ in ['ADJ', 'ADV']):
            des = token
            desHead = token.head # get description and description head (desHead & des)
        
## structure cases -----------------------------------------------------------
        ## structure 1
        if (objHead == desHead and objHead != None):
            if (obj.pos_ != 'VERB'):
                noun = (' '.join([child.text for child in obj.children
                              if child.pos_ in ['NOUN', 'PRON', 'DET']]).strip() + ' ' + obj.text).strip()
                aspDesList.append((noun,des.text))
            else:
                aspDesList.append((obj.text,des.text))
            #set all nodes back to None
            objHead = None
            obj = None
            desHead = None
            des = None
            
        # structure 2, don't forget: obj can't be None
        elif (obj == desHead and obj != None):
            
            if (objHead.pos_ == 'NOUN'):# obj has noun as head
                aspDesList.append((obj.text +' '+ objHead.text,des.text))# noun phrase (current object token + head), description))
            else:
                aspDesList.append((obj.text,des.text))# object, description
            #set all nodes back to None
            objHead = None
            obj = None
            desHead = None
            des = None
            
        # structure 3, don't forget: des can't be None
        elif (objHead == des and des != None):
            if (obj.pos_ != 'VERB'):
                noun = (' '.join([child.text for child in obj.children
                              if child.pos_ in ['NOUN', 'PRON', 'DET']]).strip() + ' ' + obj.text).strip()
                aspDesList.append((noun, des.text))# object (can be noun phrase), description
            else:
                aspDesList.append((obj.text, des.text))
#-----------------------------------------------------------------------------
    return aspDesList

def getSentiment(aspDesPair):
    ## param: aspDesPair, type: set
    
    aspect = aspDesPair[0]# aspect / object in aspDesPair set
    description = aspDesPair[1]# description in aspDesPair set
    
    ## list of positives word
    pos_word = POSITIVES.keys() # keys in POSITIVES dictionary
    ## list of negatives word
    neg_word = NEGATIVES.keys()# keys in NEGATIVES dictionary
    
    
    if (description in neg_word):# description is in negative words list:
        return (aspect,description,NEGATIVES[description])# set with (aspect, desc, score) format
    elif (description in pos_word):# description is in positive words list:
        return (aspect,description,POSITIVES[description])# set with (aspect, desc, score) format
    else:
        return (aspect,description,0)# set with (aspect, desc, score) format, score = 0
    
    ## Hint: get sentiment score from dictionary. Dicitionary uses key:value format, in this case word:score
    ## Find a way to get the score if you know the word (get value by key)
        
def main():
    ## uncomment line below if you need to check dep tree
    getTree()
    
    for txt in TEXT:
        ## print input text
        print(txt)
        ## get aspect-desc pair(s), store in 'pairs' list
        pairs = aspectDescriptionExtraction(txt)
        
        ## iterate through pair list
        for pair in pairs:
            ## get aspect based sentiment score
            print(getSentiment(pair))
        print("")
    
if __name__ == '__main__':
    main()