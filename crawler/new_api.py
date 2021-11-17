# client_key : agXsz69GSRrBcAIVoLhV
# client_Secret : y6vqdnVADz

import os
import sys
import urllib.request
import json
import pprint
import pandas as pd
import re
import numpy as np
import pandas as pd
import sys
#print(sys.version)

from konlpy.tag import Okt
from gensim import corpora, models
import time

def __main__():
    input = sys.argv[1]
    keyword = "홍준표"
    print(input)
    # keyword = input[1]
    #print("실행1")
    politic_crawler(input).main()
    #print("실행1")

class politic_crawler:
    def __init__(self, keyword):
        self.start = time.time()
        self.keyword = keyword
        self.client_id = "agXsz69GSRrBcAIVoLhV"
        self.client_secret = "y6vqdnVADz"
    
    def main(self):
        #print("실행1")
        try:
            jsonobject = self.news_api(self.keyword)  
        except Exception as e:
            print(e)
            print("NEWS_API_ERROR")            
        try:    
            result_keywords = self.lda_modeling(jsonobject)
        except Exception as e:
            print(e)
            result_keywords = "LDA_MODELING_ERROR"
            print("LDA_MODELING_ERROR")
        time_required = time.time() - self.start    
        print("결과", result_keywords)
        print("실행 시간 :", time_required)
        print("입력 키워드 : ", self.keyword)

    def news_api(self, keyword):
        
        encText = urllib.parse.quote(keyword)
        url = "https://openapi.naver.com/v1/search/news?query=" + encText+"&display=20&start=1&sort=sim"# json 결과
        # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",self.client_id)
        request.add_header("X-Naver-Client-Secret",self.client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            jsonobject = json.loads(response_body.decode('utf-8'))
           # print("아이템 : ",jsonobject['items'])
         #   pprint.pprint(jsonobject)
        else:
            print("Error Code:" + rescode)
        return jsonobject
    
    def lda_modeling(self, jsonobject):
        
        dfPapers = pd.DataFrame(columns=['papers'])
        for i in jsonobject['items']:
            data= pd.DataFrame([i["title"] + i["description"]],columns=['papers'])
            dfPapers = pd.concat([dfPapers,data], ignore_index=True)
        print("출력")
        #print(dfPapers)
        documents = dfPapers
        documents['papers'] = documents['papers'].map(lambda x: re.sub(r'[^\w\s]',' ',x))
        documents['papers'] = documents['papers'].map(lambda x: x.lower())

        list_of_documents = list(documents['papers'])
        list_of_documents[0]
       # print("dlrj",list_of_documents)
        t = Okt()
        pos = lambda d: ['/'.join(p) for p in t.pos(d, stem=True, norm=True)] #t.pos(d, stem=True, norm=True) or t.nouns(d)
        texts_ko = [pos(doc) for doc in list_of_documents]
        # print("dafsdfa",texts_ko[0])

        dictionary_ko = corpora.Dictionary(texts_ko)
        # dictionary_ko.save('ko.dict')
        #from gensim import models
        tf_ko = [dictionary_ko.doc2bow(text) for text in texts_ko]
        #print("afsdfasdfasdf",tf_ko)
        tfidf_model_ko = models.TfidfModel(tf_ko)
        tfidf_ko = tfidf_model_ko[tf_ko]
        # print("tfidf_ko", type(tfidf_ko))
        # for i in tfidf_ko:
        #     print(i)
        
        
        lda_model = models.ldamodel.LdaModel(corpus=tf_ko, id2word=dictionary_ko,num_topics=10)
        keywords = lda_model.print_topics(-1,5)
        #print(keywords)

        keywords = []
        for topic in lda_model.print_topics(-1,10):
            topic_list = topic[1].split('+')
            for i in range(len(topic_list)):
                count = 0
                words = topic_list[i].split('"')
                for j in range(len(words)):
                    if "*" in words[j] or words[j] == "" or words[j] == " ":
                        continue
                    elif words[j] not in keywords:
                        word = words[j].split('/')
                        if word[0] not in keywords and word[1] == "Noun":
                            if len(word[0])==1:
                                break
                            count += 1
                            
                            keywords.append(word[0])
                            break
                if count >= 1:
                    break
        
        return keywords  

    
        
__main__()


# start = time.time()
# client_id = "agXsz69GSRrBcAIVoLhV"
# client_secret = "y6vqdnVADz"
# keyword = "윤석열"
# encText = urllib.parse.quote(keyword)
# url = "https://openapi.naver.com/v1/search/news?query=" + encText+"&display=20&start=1&sort=sim"# json 결과
# # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
# request = urllib.request.Request(url)
# request.add_header("X-Naver-Client-Id",client_id)
# request.add_header("X-Naver-Client-Secret",client_secret)
# response = urllib.request.urlopen(request)
# rescode = response.getcode()
# if(rescode==200):
#     response_body = response.read()
#     jsonobject = json.loads(response_body.decode('utf-8'))
#     print("아이템 : ",jsonobject['items'])
#     pprint.pprint(jsonobject)
# else:
#     print("Error Code:" + rescode)
# # print(jsonobject)
# title = []
# description = []
# new_data = []
# dfPapers = pd.DataFrame(columns=['papers'])

# for i in jsonobject['items']:
#     data= pd.DataFrame([i["title"] + i["description"]],columns=['papers'])
#     dfPapers = pd.concat([dfPapers,data], ignore_index=True)
# print("출력")
# print(dfPapers)
# documents = dfPapers
# documents['papers'] = documents['papers'].map(lambda x: re.sub(r'[^\w\s]',' ',x))
# documents['papers'] = documents['papers'].map(lambda x: x.lower())

# list_of_documents = list(documents['papers'])
# list_of_documents[0]
# print("dlrj",list_of_documents)
# t = Okt()
# pos = lambda d: ['/'.join(p) for p in t.pos(d, stem=True, norm=True)] #t.pos(d, stem=True, norm=True) or t.nouns(d)
# texts_ko = [pos(doc) for doc in list_of_documents]
# # print("dafsdfa",texts_ko[0])

# dictionary_ko = corpora.Dictionary(texts_ko)
# # dictionary_ko.save('ko.dict')
# #from gensim import models
# tf_ko = [dictionary_ko.doc2bow(text) for text in texts_ko]
# #print("afsdfasdfasdf",tf_ko)
# tfidf_model_ko = models.TfidfModel(tf_ko)
# tfidf_ko = tfidf_model_ko[tf_ko]
# print("tf", tfidf_ko)
# #print(corpora.MmCorpus.serialize('ko.mm', tfidf_ko)) # save corpus to file for future use

# # print first 10 elements of first document's tf-idf vector
# print("tesa",tfidf_ko.corpus[0][:10])
# # print top 10 elements of first document's tf-idf vector
# print(sorted(tfidf_ko.corpus[0], key=lambda x: x[1], reverse=True)[:10])
# # print token of most frequent element
# print(dictionary_ko.get(51),dictionary_ko.get(3),dictionary_ko.get(29),dictionary_ko.get(46
# ))
# lda_model = models.ldamodel.LdaModel(corpus=tf_ko, id2word=dictionary_ko,num_topics=10)
# keywords = lda_model.print_topics(-1,5)
# print(keywords)

# keywords = []
# for topic in lda_model.print_topics(-1,10):
#     topic_list = topic[1].split('+')
#     for i in range(len(topic_list)):
#         count = 0
#         words = topic_list[i].split('"')
#         for j in range(len(words)):
#             if "*" in words[j] or words[j] == "" or words[j] == " ":
#                 continue
#             elif words[j] not in keywords:
#                 word = words[j].split('/')
#                 if word[0] not in keywords and word[1] == "Noun":
#                     if len(word[0])==1:
#                         break
#                     count += 1
                    
#                     keywords.append(word[0])
#                     break
#         if count >= 1:
#             break
# print("실행 시간 :", time.time() - start)
# print("입력 키워드 : ", keyword)
# print(keywords)