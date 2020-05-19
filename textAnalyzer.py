import re
import pymysql
import time
from collections import Counter
from konlpy.tag import Okt
from konlpy.tag import Kkma
from konlpy.tag import Komoran
from konlpy.tag import Hannanum
from eunjeon import Mecab
from konlpy.tag import Twitter
from operator import itemgetter
import pandas as pd
import gc
import os

class TextAnalyzer:

    def __init__(self, keyword,channel, startDate, endDate, nlpEngine, nUrl):

        self.keyword = keyword

        self.channel = channel
        self.startDate = startDate
        self.endDate = endDate

        self.nlpEngine = nlpEngine

        self.nUrl = nUrl

        if nlpEngine == "Okt":
            self.konlpy = Okt()
        elif nlpEngine == "Komoran":
            self.konlpy = Komoran()
        elif nlpEngine == "Kkma":
            self.konlpy = Kkma()
        elif nlpEngine == "Hannanum":
            self.konlpy = Hannanum()
        elif nlpEngine == "Mecab":
            self.konlpy = Mecab()
        elif nlpEngine == "Twitter":
            self.konlpy = Twitter()
        else:
            self.konlpy = Okt()

    def kano_read(self):
        conn = pymysql.connect(host='106.246.169.202', user='root', password='robot369',
                               db='crawl', charset='utf8mb4')
        # 192.168.0.105
        # 106.246.169.202
        curs = conn.cursor(pymysql.cursors.DictCursor)
        print("db진입")

        sql = "select * from htdocs where keyword= \'%s\' and channel=\'%s\' and publishtime>=\'%s\' and publishtime<=\'%s\' limit 2000" % \
              (self.keyword, self.channel, self.startDate, self.endDate)  ####해당 keyword 가 들어가있는 text 를 가져온다

        # ('%' + self.keyword + '%', self.channel, self.startDate, self.endDate)  ####해당 keyword 가 들어가있는 text 를 가져온다

        curs.execute(sql)
        print("executeSQL")

        rows = curs.fetchall()
        list = []
        self.text = ''
        for row in rows:
            self.text += row['htmltext']
            list.append(row['htmltext'])
        conn.close()
        return list

    def record(self):
        db = 'crawl' if self.channel != 'Naver News' else 'naver_news'
        conn = pymysql.connect(host='106.246.169.202', user='root', password='robot369',
                               db=db, charset='utf8mb4')

    def read_s(self):
        table = 'htdocs' if self.channel != 'Naver News' else 'naver_news'
        conn = pymysql.connect(host='106.246.169.202', user='root', password='robot369',
                               db='crawl', charset='utf8mb4')
        # 106.246.169.202
        # 192.168.0.105
        # 103.55.190.32 wordcloud ap
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = "select * from %s where (keyword=\'%s\') and channel=\'%s\' and publishtime>=\'%s\' and publishtime<=\'%s\' limit %d" % \
              (table,self.keyword, self.channel ,self.startDate, self.endDate, self.nUrl)
        print('sql=', sql)
        curs.execute(sql)

        rows = curs.fetchall()
        self.text = ''
        print(self.keyword, len(rows))
        self.phrase = []
        self.publishtime = []
        for row in rows:
            self.text += row['htmltext']
            self.phrase.append(row['htmltext'])
            self.publishtime.append(row['publishtime'])

        print('read finish')
        conn.close()

    def read(self):
        table = 'htdocs' if self.channel != 'Naver News' else 'naver_news'
        conn = pymysql.connect(host='106.246.169.202', user='root', password='robot369',
                               db='crawl', charset='utf8mb4')
        # 106.246.169.202
        # 192.168.0.105
        # 103.55.190.32 wordcloud ap
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = "select * from %s where (keyword=\'%s\') and channel=\'%s\' and publishtime>=\'%s\' and publishtime<=\'%s\' limit %d" % \
              (table,self.keyword, self.channel ,self.startDate, self.endDate, self.nUrl)
        print('sql=', sql)
        curs.execute(sql)

        rows = curs.fetchall()
        self.text = ''
        print(self.keyword, len(rows))
        for row in rows:
            if '박지훈' in row['htmltext']:
                pass
            else:
                self.text += row['htmltext']
        print('read finish')
        conn.close()
    def sentiment_read(self):
        table = 'htdocs' if self.channel != 'Naver News' else 'naver_news'
        conn = pymysql.connect(host='106.246.169.202', user='root', password='robot369',
                               db='crawl', charset='utf8mb4')
        # 106.246.169.202
        # 192.168.0.105
        # 103.55.190.32 wordcloud ap
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = "select * from %s where (keyword=\'%s\') and publishtime>=\'%s\' and publishtime<=\'%s\' limit %d" % \
              (table,self.keyword, self.startDate, self.endDate, self.nUrl)
        print('sql=', sql)
        curs.execute(sql)

        rows = curs.fetchall()
        self.text = ''
        print(self.keyword, len(rows))
        self.text_list =[]
        for row in rows:
            self.text += row['htmltext']
            self.text_list.append(row['htmltext'])
        print('read finish')
        conn.close()

    def cleanse(self):
        self.text = re.sub(u"(http[^ ]*)", " ", self.text)
        self.text = re.sub(u"@(.)*\s", " ", self.text)
        self.text = re.sub(u"#", "", self.text)
        self.text = re.sub(u"\\d+", " ", self.text)
        self.text = re.sub(u"[^가-힣A-Za-z]", " ", self.text)
        self.text = re.sub(u"\\s+", " ", self.text)

    def removeCommonWords(self):
        if self.channel == "Instagram":
            self.keywordList = ["인스타그램", "인스타", "팔로우", "맞팔", "인친", "셀스타그램", "그램", "스타"]
        elif self.channel == "Naver Blog":
            self.keywordList = ["포스팅", "블로그", "댓글", "이웃추가"]
        elif self.channel == "Twitter":
            self.keywordList = ["트윗", "RT", "트위터"]
        if self.channel == "Naver News":
            self.keywordList = ["없음", "헤럴드", "역필", "투데이", "머니", "코리아", "기자", "오마이", "구독", "연합", "채널", "네이버", "뉴시스",
                                "금지", "저작", "무단", "뉴스", "재배포"]
        else:
            self.keywordList = []

        # self.keywordList.append(self.keyword)

        for keyword in self.keywordList:
            self.text = re.replace(keyword, " ", self.text)

    def posTag(self):
        print("Getting Meaningful Words for " + self.keyword + "...", end="\t")

        pos = self.konlpy.pos(self.text)
        print("Pos tagging complete. Extracting Nouns, Adjectives, Exclamations ...")

        words = []
        for p in pos:
             if p[1] in ['NNG','NNP']:  # 코모란, Mecab 기준임
            #'MAG'
            #if p[1] in ['IC','VA']:  # 코모란, Mecab 기준임

                # 'VA', 'IC' 위에 대괄호 안에 추가하면 된다
                # if p[1] in ['Noun', 'ProperNoun']:  # Okt, Twitters
                # 'Noun', 'ProperNoun', 'Adjective', 'Exclamation' 위에 대괄호 안에 추가하면 된다!
                # print(p[0],p[1])
                words.append(p[0])

        print("Extracting complete.")

        return words

    def func(self, x):
        if x[1] > 1:
            return x
        else:
            return None

    def getWordCount(self, nRank, minFreq):
        words = self.posTag()

        counter = Counter(words)

        # self.wordDict = counter

        c = counter.most_common(nRank)

        c = list(filter(lambda x: len(x[0]) >= 2, c))

        ###key list 엑셀에 추가
        # df_key = pd.read_excel('keyword_sentiment_matching\광진구num_list_2010-07-01~2018-06-30.xlsx', sheet_name='Sheet1')  ## 매칭할 keyword list 를 가지고 있는 문서
        # basic_keylist = []
        # q=0
        # for i in df_key['keyword']:  # keyword_list keylist 변수에 저장한다.
        #     basic_keylist.append(i)
        #     q = q+1
        #     if q>100:
        #         break
        db_diction = {}
        compare_list = []  # 비교대상 년도의 빈도수를 뽑는다
        q = 0
        # for i in c:
            # compare_dict = {'keyword': i[0], 'count':i[1], 'basic_differentiate': 1 if i[0] in basic_keylist else 0}       #기준년도 keylist 와 일치하는 keyword 를 찾고 식별값을 부여한다(일치: 1 불일치: 0)
            # compare_list.append(compare_dict)
            # compare_dict = {'keyword': i[0], 'count': i[1]}  # 기준년도 keylist 와 일치하는 keyword 를 찾고 식별값을 부여한다(일치: 1 불일치: 0)
            # compare_list.append(compare_dict)
            # # list에 추가한다.
            #
            # # DB에 추가하기 위해 사전 {'K': 'V'} 사전 형태 만들어주기
            # if q < 300:
            #     db_diction[i[0]] = i[1]
            # q += 1

        # db_diction = str(db_diction)
        # db_diction = db_diction.replace("'", "")
        # compare_list_table = pd.DataFrame(compare_list, columns=(
        #     'keyword', 'count'))  # 엑셀에 저장하기 위해 keyword, count, basic_dfferntiate(식별값) 으로 칼럼을 만든다
        # compare_list_table.to_excel(
        #     'keyword_sentiment_matching/' + self.keyword + 'num_list' + '_' + self.startDate + '~' + self.endDate + self.channel+'.xlsx',
        #     encoding="utf-8", index=True)  # 엑셀에 저장한다. 대상 키워드와 비교년도 를 제목으로 하는 파일 생성

        ##DB 에 키워드와 빈도수 리스트 저장하기
        db = 'crawl'
        conn = pymysql.connect(host='106.246.169.202', user='root', password='robot369',
                               db=db, charset='utf8mb4')
        # 106.246.169.202
        # 192.168.0.105
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql0 = "select * from polls_keyword_number where keyword=\'%s\' and channel=\'%s\' and stdate=\'%s\' and endate=\'%s\' and nurl=%d"%\
               (self.keyword, self.channel, self.startDate, self.endDate, self.nUrl)
        curs.execute(sql0)
        rows = curs.fetchall()
        sql = "insert into polls_keyword_number(keyword, channel,stdate, endate, nurl, top300)" \
              + "values (\'%s\', \'%s\', \'%s\',\'%s\', %d, \'%s\')" % \
              (self.keyword, self.channel, self.startDate, self.endDate, self.nUrl, db_diction)
        curs.execute(sql)
        conn.commit()
        conn.close()
        c.sort(key=itemgetter(1), reverse=True)
        except_list =[]
        except_list = self.keyword.split(" ")


        self.freqWordList = []
        nWord = 0
        for i in c:
            if i[1] < minFreq:
                break

            self.freqWordList.append(i)
            nWord += 1
            if nWord >= nRank:
                break
            # print(i)

        self.freqWordDict = dict(self.freqWordList)

    def make_function_excel(self):
        df_key = pd.read_excel('function_keyword/function_keyword.xlsx',
                               sheet_name=self.keyword)  ## 매칭할 keyword list 를 가지고 있는 문서
        with open('df.json', 'w', encoding='utf-8') as file:  ## json 파일로 변환해준다
            df_key.to_json(file, force_ascii=False)
        df_json = pd.read_json('df.json', encoding='utf-8')

        function_list = list(set(df_json['기능']))  ##기능을 리스트로 뽑는다(중복제거)
        print(len(function_list))

        dict_list = []
        for i in range(0, len(df_json)):  ##dict list 로 만들어준다
            dict = {'index': i, 'function': df_json['기능'][i], 'keyword': df_json['keyword'][i]}
            dict_list.append(dict)
        return dict_list, function_list

    def make_pharse(self, pharse_list, keyword_list, function, ntotal):
        good_text = []
        for i in pharse_list:
            for token in keyword_list:
                if token in i:
                    good_text.append(i)
                    self.g_publishtime.append()
        total_text = ''
        for i in good_text:
            total_text += i

        df_token = pd.DataFrame({"text": good_text})
        df_token.to_excel(
            'pharse/' + 'pharse_' + self.keyword + '_' + function + '_' + self.startDate + '~' + self.endDate + '_' + str(
                ntotal) + '.xlsx',
            sheet_name=self.keyword, engine='xlsxwriter')
        # total_text = self.text
        return total_text

    def make_value_table(self, df_group_by):

        df_dict = df_group_by.to_dict()
        column_list = df_dict['count'].keys()
        group_by_list = []
        for i, value in enumerate(column_list):  # type 이 A1 A2 이런거고 sum 은 이거 group by 해서 더한거임
            group_by_dict = {'index': i, 'type': value, 'sum': df_dict['count'].get(value)}
            group_by_list.append(group_by_dict)

        group_by_table = pd.DataFrame(group_by_list, columns=('index', 'type', 'sum'))
        # value dataFrame 만드는 과정

        value_dict_list = []
        values_list = ['경제적가치', '기능적가치', '사회적가치', '학습적가치', '감성적가치', '환경적가치']
        sum_surprise = 0
        sum_happy = 0
        sum_anticipate = 0
        sum_trust = 0
        sum_angry = 0
        sum_disgust = 0
        sum_sad = 0
        sum_fear = 0

        for i, value in enumerate(values_list):  ##영문별로 숫자별로 더하기 위한 과정
            value_total = group_by_table['sum'][0 + i * 8] + group_by_table['sum'][1 + i * 8] + group_by_table['sum'][
                2 + i * 8] + \
                          group_by_table['sum'][3 + i * 8] + group_by_table['sum'][4 + i * 8] + group_by_table['sum'][
                              5 + i * 8] + \
                          group_by_table['sum'][6 + i * 8] + group_by_table['sum'][7 + i * 8]

            value_pos = group_by_table['sum'][0 + i * 8] + group_by_table['sum'][1 + i * 8] + group_by_table['sum'][
                2 + i * 8] + group_by_table['sum'][3 + i * 8]
            value_neg = group_by_table['sum'][4 + i * 8] + group_by_table['sum'][5 + i * 8] + group_by_table['sum'][
                6 + i * 8] + group_by_table['sum'][7 + i * 8]

            sum_surprise += group_by_table['sum'][0 + i * 8]
            sum_happy += group_by_table['sum'][1 + i * 8]
            sum_anticipate += group_by_table['sum'][2 + i * 8]
            sum_trust += group_by_table['sum'][3 + i * 8]
            sum_angry += group_by_table['sum'][4 + i * 8]
            sum_disgust += group_by_table['sum'][5 + i * 8]
            sum_sad += group_by_table['sum'][6 + i * 8]
            sum_fear += group_by_table['sum'][7 + i * 8]

            value_dict = {'놀람': group_by_table['sum'][0 + i * 8],
                          '기쁨': group_by_table['sum'][1 + i * 8],
                          '기대': group_by_table['sum'][2 + i * 8],
                          '신뢰': group_by_table['sum'][3 + i * 8],
                          '분노': group_by_table['sum'][4 + i * 8],
                          '혐오': group_by_table['sum'][5 + i * 8],
                          '슬픔': group_by_table['sum'][6 + i * 8],
                          '두려움': group_by_table['sum'][7 + i * 8],
                          '긍정': str(round(value_pos / value_total * 100, 2)) + '%',
                          '부정': str(round(value_neg / value_total * 100, 2)) + '%'}

            value_dict_list.append((value_dict))
        total_pos = sum_surprise + sum_happy + sum_anticipate + sum_trust

        total_neg = sum_angry + sum_disgust + sum_sad + sum_fear
        total_total = total_pos + total_neg
        value_dict = {'놀람': sum_surprise,
                      '기쁨': sum_happy,
                      '기대': sum_anticipate,
                      '신뢰': sum_trust,
                      '분노': sum_angry,
                      '혐오': sum_disgust,
                      '슬픔': sum_sad,
                      '두려움': sum_fear,
                      '긍정': total_pos,
                      '부정': total_neg}
        value_dict_list.append((value_dict))
        try:
            value_dict = {'놀람': str(round(sum_surprise / total_total * 100, 2)) + '%',
                          '기쁨': str(round(sum_happy / total_total * 100, 2)) + '%',
                          '기대': str(round(sum_anticipate / total_total * 100, 2)) + '%',
                          '신뢰': str(round(sum_trust / total_total * 100, 2)) + '%',
                          '분노': str(round(sum_angry / total_total * 100, 2)) + '%',
                          '혐오': str(round(sum_disgust / total_total * 100, 2)) + '%',
                          '슬픔': str(round(sum_sad / total_total * 100, 2)) + '%',
                          '두려움': str(round(sum_fear / total_total * 100, 2)) + '%',
                          '긍정': str(round(total_pos / total_total * 100, 2)) + '%',
                          '부정': str(round(total_neg / total_total * 100, 2)) + '%'}
            value_dict_list.append((value_dict))
        except Exception as e:
            print(e)
        value_table = pd.DataFrame(value_dict_list,
                                   columns=('놀람', '기쁨', '기대', '신뢰', '분노', '혐오', '슬픔', '두려움', '긍정', '부정'),
                                   index=['경제적가치', '기능적가치', '사회적가치', '학습적가치', '감성적가치', '환경적가치', 'total', 'total_rate'])

        return value_table

    def matching_sentiment_naver(self, sub_key, ntotal):

        self.read()
        self.text = re.sub(u"(http[^ ]*)", " ", self.text)
        self.text = re.sub(u"@(.)*\s", " ", self.text)
        self.text = re.sub(u"#", "", self.text)
        self.text = re.sub(u"\\d+", " ", self.text)
        self.removeCommonWords()

        pharse_list = self.phrase
        df_sentiment_keyword = pd.read_excel('sent_dict/value_sentiment_original.xlsx', sheet_name='Sheet1')

        dict_list, function_list = self.make_function_excel()  ##function 과 keyword 맵 dict 와 fucntion list 를 받아온다.

        n = 0
        sheet_list = []
        while n < len(function_list):  ##각 기능별로 매칭 키워드를 찾는 과정       ##function_list 수만큼 진행
            matching_keyword = []
            matching_count = []
            function = function_list[n]  # 기능을 하나 가지고온다
            print('function', function)

            keyword_list = []
            for i, val in enumerate(dict_list):  #
                if dict_list[i].get('function') == function:  # list 에서 해당 기능과 동일한 값 기능을 가진 row 가 있으면
                    keyword_list.append(dict_list[i].get('keyword'))  # keyword 키값에 해당하는 value 를 keyword_list 에 추가해준다
            print('function,keyword_list', function, keyword_list)

            total_text = self.make_pharse(pharse_list, keyword_list, function,
                                          ntotal)  ### 해당 기능에 대한 키워드가 들어있는 문장을 전부 가져온다
            # total_text = self.text
            sentiment_dict_list = []
            for i, keyword in enumerate(df_sentiment_keyword['keyword']):  ##감정 사전에서 감정 키워드를 가져온다
                count = total_text.count(keyword)  ##기능을 가지고 있는 문장과 감정 키워드 매칭과정
                matching_keyword.append(keyword)  ##count 함수를 이용하여 해당 문장에 keyword 수를 가져온다.
                matching_count.append(count)
                sentiment_dict = {'keyword': keyword, 'type': df_sentiment_keyword['type'][i],
                                  'count': count}  # keyword, type, count 사전을 만든다 type= A1 A2 B1 B2 --- 이런식
                sentiment_dict_list.append(sentiment_dict)
            df_matching = pd.DataFrame(sentiment_dict_list, columns=(
            'keyword', 'type', 'count'))  ##excel 로 만들어 주기 위한 과정 keyword,type , count 와

            df_group_by = df_matching.groupby(by='type', group_keys='count').sum()  ##tyoe 기준으로 group by 하여 sum 을 해준다.

            value_table = self.make_value_table(df_group_by)  ##6X8 표를 만들어주는 과정
            final_df = df_matching.sort_values(by='count', ascending=False)  ##감정사전 용어의 분류와 count 가 나와있는 dataframe
            sheet_list.append((value_table, final_df, function))  ##sheet 를 만들어주기 위해 리스트에 추가한다
            n = n + 1
        self.make_total_excel(sheet_list, ntotal, sub_key)  ###keyword 엑셀파일이 만들어진다.각 기능별로 sheet가 만들어짐(6x8 기능, count 기능)

    def matching_sentiment_youtube(self, sub_key,ntotal):
        self.sentiment_read()
        self.text = re.sub(u"(http[^ ]*)", " ", self.text)
        self.text = re.sub(u"@(.)*\s", " ", self.text)
        self.text = re.sub(u"#", "", self.text)
        self.text = re.sub(u"\\d+", " ", self.text)
        self.removeCommonWords()

        pharse_list = self.text_list
        df_sentiment_keyword = pd.read_excel('sent_dict/value_sentiment_original.xlsx', sheet_name='Sheet1')

        dict_list, function_list = self.make_function_excel()  ##function 과 keyword 맵 dict 와 fucntion list 를 받아온다.

        n = 0
        sheet_list = []
        while n < len(function_list):  ##각 기능별로 매칭 키워드를 찾는 과정       ##function_list 수만큼 진행
            matching_keyword = []
            matching_count = []
            function = function_list[n]  # 기능을 하나 가지고온다
            print('function', function)

            keyword_list = []
            for i, val in enumerate(dict_list):  #
                if dict_list[i].get('function') == function:  # list 에서 해당 기능과 동일한 값 기능을 가진 row 가 있으면
                    keyword_list.append(dict_list[i].get('keyword'))  # keyword 키값에 해당하는 value 를 keyword_list 에 추가해준다
            print('function,keyword_list', function, keyword_list)

            total_text = self.make_pharse(pharse_list, keyword_list, function,
                                          ntotal)  ### 해당 기능에 대한 키워드가 들어있는 문장을 전부 가져온다
            total_text = self.text
            sentiment_dict_list = []
            for i, keyword in enumerate(df_sentiment_keyword['keyword']):  ##감정 사전에서 감정 키워드를 가져온다
                count = total_text.count(keyword)  ##기능을 가지고 있는 문장과 감정 키워드 매칭과정
                matching_keyword.append(keyword)  ##count 함수를 이용하여 해당 문장에 keyword 수를 가져온다.
                matching_count.append(count)
                sentiment_dict = {'keyword': keyword, 'type': df_sentiment_keyword['type'][i],
                                  'count': count}  # keyword, type, count 사전을 만든다 type= A1 A2 B1 B2 --- 이런식
                sentiment_dict_list.append(sentiment_dict)
            df_matching = pd.DataFrame(sentiment_dict_list, columns=(
            'keyword', 'type', 'count'))  ##excel 로 만들어 주기 위한 과정 keyword,type , count 와

            df_group_by = df_matching.groupby(by='type', group_keys='count').sum()  ##tyoe 기준으로 group by 하여 sum 을 해준다.

            value_table = self.make_value_table(df_group_by)  ##6X8 표를 만들어주는 과정
            final_df = df_matching.sort_values(by='count', ascending=False)  ##감정사전 용어의 분류와 count 가 나와있는 dataframe
            sheet_list.append((value_table, final_df, function))  ##sheet 를 만들어주기 위해 리스트에 추가한다
            n = n + 1
        self.make_total_excel(sheet_list, ntotal, sub_key)  ###keyword 엑셀파일이 만들어진다.각 기능별로 sheet가 만들어짐(6x8 기능, count 기능)


    def make_total_excel(self, sheet_list, ntotal, sub_key):
        writer = pd.ExcelWriter(
            'sentiment/' + self.keyword + '_' + sub_key+'_' + self.startDate + '~' + self.endDate + '_'+self.channel+'_' + str(ntotal) + '.xlsx')
        for n, df in enumerate(sheet_list):
            df[0].to_excel(writer, self.keyword + '_' + df[2] + '_6X8', engine='xlsxwriter', index_label='value')
            df[1].to_excel(writer, self.keyword + '_' + df[2] + '_count', engine='xlsxwriter')
        writer.save()

    def extractFrequentWords(self, nRank, minOccur):
        self.read()
        self.cleanse()
        self.removeCommonWords()
        self.getWordCount(nRank, minOccur)
        return self.freqWordDict
