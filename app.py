import pandas as pd
import numpy as np

import nltk
nltk.data.path.append('./nltk_data/')
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
from nltk.stem import PorterStemmer
from fuzzywuzzy import fuzz
from nltk import ne_chunk
from nltk.corpus import stopwords
import re
import json
from flask import Flask,request,Response,jsonify
from flask_jsonpify import jsonpify
def getrec(Dom,Event):
    dataf = pd.read_csv('final.csv')
    reqd=pd.DataFrame(columns=['id','title','url'])
    df=dataf
    df['Domain']= ''
    df['Domtemp']=''
    pst = PorterStemmer()
    punctuation = re.compile(r'[-.!@&,:()|0-9]')
    stop = stopwords.words('english')
    df['title']=df['title'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
    bs=Dom+" "+Event
    indd=0
    for ind,bb in enumerate(df.title) :
        
        ai_tokens = word_tokenize(bb)
       
        fdist=FreqDist()
        for word in ai_tokens:
            fdist[word.lower()]+=1
      
        
        post_pun=[]
        for words in fdist:
            word=punctuation.sub("",words)
            if len(word)>0:
                post_pun.append(word)
        
        gen_docs = [[w.lower() for w in word_tokenize(text)] 
            for text in post_pun]
    
        bi_tok=word_tokenize(bs)
        bdist=FreqDist()
        for word in bi_tok:
            bdist[word.lower()]+=1
        bos_pun=[]
        for words in bdist:
            word=punctuation.sub("",words)
            if len(word)>0:
                bos_pun.append(word)
        
        percent=fuzz.partial_ratio(gen_docs,bos_pun)
        if percent>70:
            reqd.loc[indd,['id']]= df.loc[ind,['id']]
            reqd.loc[indd,['title']]= bb
            reqd.loc[indd,['url']]= df.loc[ind,['url']]
            indd=indd+1
    
    
    return reqd


app = Flask(__name__)

@app.route('/api/upload' , methods=['GET', 'POST'])
def upload():
    data = request.json['key']
    data2 = request.json['key2']
    dataget = getrec(data,data2)
    dataget = dataget.to_json()
    return dataget

if __name__ == "__main__":
    app.run(debug=True)