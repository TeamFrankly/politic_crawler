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
from konlpy.tag import Okt
from gensim import corpora, models
import time
import pymysql


def __main__():
    """
    politic_crwaler를 실행함.
    """
    f = open("crawler\list.txt", 'r',encoding='UTF8')
    lines = f.readlines()
    for line in lines:
        input = line.replace("\n","")
        politic_crawler(input).main()

class politic_crawler:
    
    def __init__(self, keyword):
        """
        method : __init__
        explain : 생성자. db를 연결하고, 각 자료구조를 생성함.
        """
        self.start = time.time()
        try:
            self.db = pymysql.connect(host='127.0.0.1',port=3306, user='root', passwd="whdgns1002@"
                                    ,db='test', charset='utf8')
            
            self.cursor = self.db.cursor()
        except Exception as e:
            print("db is not connection")
        self.keyword = keyword
        self.client_id = "agXsz69GSRrBcAIVoLhV"
        self.client_secret = "y6vqdnVADz"
        self.url_list = []

    def main(self):
        """
        method : main
        explain : news_api 함수와 LDA_MODELING을 실행한다. 주요 기능의 실행을 담당한다.
        
        """
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
        # print("결과", result_keywords)
        # print("실행 시간 :", time_required)
        # print("url_list : " self.url_list)
        # print("입력 키워드 : ", self.keyword)
        result_url_list = ""
        result_keyword = ""
        try:
            result_keyword = result_keywords[0] + ", "+result_keywords[1]+", "+ result_keywords[2]+ ", "+result_keywords[3]+ ", "+result_keywords[4]
            result_url_list = self.url_list[0] + ", "+self.url_list[1]+ ", "+self.url_list[2]+ ", "+self.url_list[3]+ ", "+self.url_list[4]
        except Exception as e:
            result_keyword = result_keywords[0] + ", "+result_keywords[1]+", "+ result_keywords[2]
            result_url_list = self.url_list[0] + ", "+self.url_list[1]+ ", "+self.url_list[2]

        print(result_url_list, result_keyword, self.keyword)
        try:
            self.mysql_connection(result_url_list, result_keyword, self.keyword)
        except Exception as e:
            print("mysql error")
            print(e)
    

    def mysql_connection(self, url_list, result_keywords, search_keyword):
        '''
        method : mysql_connection
        explain : mysql을 사용하기 위한 함수.
        '''
        create_sql = """
                CREATE TABLE SRESULT(
                      result_keywords VARCHAR(500) NOT NULL,
                      input_keyword VARCHAR(500) NOT NULL, 
                      NEWS_URL VARCHAR(500) NOT NULL
                )
                
                """
        input_sql = """
          INSERT INTO SRESULT(result_keywords, input_keyword, NEWS_URL) VALUES (%s,%s,%s)
        """
        
        try:
            self.cursor.execute(input_sql,(result_keywords, self.keyword, url_list))
        except:
            self.cursor.execute(create_sql)
            self.cursor.execute(input_sql,(result_keywords, self.keyword, url_list))

        self.db.commit()
        self.db.close()


    def news_api(self, keyword):
        '''
        api url : https://developers.naver.com/docs/serviceapi/search/news/news.md#%EB%89%B4%EC%8A%A4 
        method : news_api를 직접적으로 사용하는 함수. description과 title를 json형태로 반환함.
        '''
        encText = urllib.parse.quote(self.keyword)
        url = "https://openapi.naver.com/v1/search/news?query=" + encText+"&display=100&start=1&sort=sim"# json 결과
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",self.client_id)
        request.add_header("X-Naver-Client-Secret",self.client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            jsonobject = json.loads(response_body.decode('utf-8'))

      
        else:
            print("Error Code:" + rescode)
        return jsonobject
    
    def lda_modeling(self, jsonobject):
        '''
        method : lda_modeling
        explain : lda modeling
        lda 모델링
        1. 어간추출 - konlpy
        2. bow - gensim
        3. tf-idf - gensim
        4. lda - gensim
        '''
        dfPapers = pd.DataFrame(columns=['papers'])
        for i in jsonobject['items']:
            data= pd.DataFrame([i["title"] + i["description"]],columns=['papers'])
            dfPapers = pd.concat([dfPapers,data], ignore_index=True)
        
            if len(self.url_list) < 5:
                self.url_list.append(i['link'])

        documents = dfPapers
        documents['papers'] = documents['papers'].map(lambda x: re.sub(r'[^\w\s]<>',' ',x))
        documents['papers'] = documents['papers'].map(lambda x: x.lower())
        list_of_documents = list(documents['papers'])
        t = Okt()
        pos = lambda d: ['/'.join(p) for p in t.pos(d, stem=True, norm=True)]
        texts_ko = [pos(doc) for doc in list_of_documents]
        ################## 데이터 전처리 ######################3
        dictionary_ko = corpora.Dictionary(texts_ko)

        tf_ko = [dictionary_ko.doc2bow(text) for text in texts_ko]
        ################## BOW 활용 ################333
        tfidf_model_ko = models.TfidfModel(tf_ko)
        tfidf_ko = tfidf_model_ko[tf_ko]
        ################## TF-IDF를 활용한 가중치 부여 ####################333
        lda_model = models.ldamodel.LdaModel(corpus=tf_ko, id2word=dictionary_ko,num_topics=10)
        ################### LDA MODELING 수행 ######################3
        keywords = lda_model.print_topics(-1,15)

        keywords = []
        for topic in lda_model.print_topics(-1,15):
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
        ##################### 모델링 후 필요없는 단어 제거 #########################
        return keywords  
      
__main__()

