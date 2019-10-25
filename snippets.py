import ast
import math
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize
import collections
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet


#These are the files used in the code
idf = pd.read_csv('idf.csv')
max_d = pd.read_csv('max_d.csv')
cd = pd.read_csv('doc_df.csv')
index = pd.read_csv('index.csv', header=None)
index.columns = ['words', 'doc_freq']
data = pd.read_csv('wikipedia_text_files.csv')


lemmatizer = WordNetLemmatizer()
stops = stopwords.words('english')
coll_stops = ["also", "first", "one", "new", "year", "two", "time", "state", "school"]
stops.extend(coll_stops)

def clean(doc):
    doc_low = doc.lower().replace("–", " ")
    words = word_tokenize(doc_low)
    words = [lemmatizer.lemmatize(w).strip() for w in words if not w in stops and wordnet.synsets(w) and w.isalpha()]
    return words

#Takes one document and creates a list containint the title a top 3 realted sentence to a given clean query
def snippet (doc_id, q):
    doc_tfidf = pd.DataFrame()
    sent_doc = pd.DataFrame()
    cosine_df = pd.DataFrame()
    sent_doc_c = pd.DataFrame()
    
    #Create Frame with TF-IDF for every word in the clean doc
    clean_list = ast.literal_eval(cd.clean[doc_id]) 
    doc_tfidf['words'] = list(set(clean_list))
    doc_tfidf['tf-idf'] = [(ast.literal_eval(index.loc[index.words == x, 'doc_freq'].item()).get(doc_id)/ max_d.max_d[doc_id])* idf.loc[idf.word == x, 'idf'].item() for x in doc_tfidf.words]
    
    #Grab Full doc from corpus, since I dont keep periods
    doc = data.loc[cd.index == doc_id, 'content'].item()
    
    #Tokenize into sentences and clean
    sent_doc['sent'] = sent_tokenize(doc)
    sent_doc['clean'] = [clean(x) for x in sent_doc.sent]
    sent_doc_c = sent_doc[sent_doc.astype(str)['clean'] != '[]'].reset_index()
    
    #Create vector from query and sentence
    cosine = []
    for x in sent_doc_c.clean:
        x_set = set(x)
        q_set = set(q)
        vector = x_set.union(q_set)
    
    #Calculate vectore values for both
        q_v = []
        s_v = []
        for w in vector:
            if w in q_set:
                q_v.append(doc_tfidf.loc[doc_tfidf.words == w, 'tf-idf'].item())
            else:
                q_v.append(0)
            if w in x_set:
                s_v.append(doc_tfidf.loc[doc_tfidf.words == w, 'tf-idf'].item())
            else:
                s_v.append(0)
    
    #Calculate cosine simularity
        c = 0
        for i in range(len(vector)):
            c += q_v[i] * s_v[i]
        cosine.append(c / math.sqrt((math.pow(sum(q_v), 2)) * (math.pow(sum(s_v), 2))))
    cosine_df['sim'] = cosine
    cosine_df = cosine_df.sort_values(by=['sim'], ascending=False).reset_index()
    sent_pos = list(cosine_df[0:3]['index'])
    
    #Put together the snippet as a list to return
    snip = []
    para = ""
    snip.append(data.title[doc_id])
    for x in sent_pos:
        para = para + sent_doc_c.sent[x]
    snip.append(para)
    return snip
