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

def news_api(keyword):
    '''
    api url : https://developers.naver.com/docs/serviceapi/search/news/news.md#%EB%89%B4%EC%8A%A4 
    method : news_api를 직접적으로 사용하는 함수. description과 title를 json형태로 반환함.
    '''
    client_id = "agXsz69GSRrBcAIVoLhV"
    client_secret = "y6vqdnVADz"
    encText = urllib.parse.quote(keyword)
    url = "https://openapi.naver.com/v1/search/news?query=" + encText+"&display=20&start=1&sort=sim"# json 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        jsonobject = json.loads(response_body.decode('utf-8'))

    
    else:
        print("Error Code:" + rescode)
    return jsonobject
a = "허영"
b = news_api(a)
print(b['items'][0]['description'])

