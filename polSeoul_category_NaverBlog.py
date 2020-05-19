from konlpy.tag import Kkma
import pandas as pd
import pymysql
import re
import json
from collections import OrderedDict
import datetime
import pandas as pd
import os
from almaden import *
import kss

class Pol_Analyzer:
    def tagConvert(self, t):
        t = t.replace('/EPH;', '/EP;')
        t = t.replace('/EPT;', '/EP;')
        t = t.replace('/EPP;', '/EP;')
        t = t.replace('/EFN;', '/EF;')
        t = t.replace('/EFQ;', '/EF;')
        t = t.replace('/EFO;', '/EF;')
        t = t.replace('/EFA;', '/EF;')
        t = t.replace('/EFI;', '/EF;')
        t = t.replace('/EFR;', '/EF;')
        t = t.replace('/ECE;', '/EC;')
        t = t.replace('/ECD;', '/EC;')
        t = t.replace('/ECS;', '/EC;')
        t = t.replace('/VXV;', '/VX;')
        t = t.replace('/VXA;', '/VX;')
        t = t.replace('/ETD;', '/ETM;')
        t = t.replace('/MDT;', '/MM;')
        t = t.replace('/MDN;', '/MM;')
        t = t.replace('/MD;', '/MM;')
        t = t.replace('/NNM;', '/NNB;')
        return t

    def __init__(self, keyword, brand,category, sub_keyword, channel,startDate, endDate, quantity):
        self.db_tasksent = Sql('sociallistening', 'tasksent')
        self.id_task = self.db_tasksent.insert('tasksent',
                          keyword=keyword,
                          brand =brand,
                          category=category,
                          sub_keyword=sub_keyword,
                          channel=channel,
                          startDate=startDate,
                          endDate = endDate,
                          status = 'DR',
                          nUrl = quantity)
    # sentiment_intensities = pd.read_csv("intensity.csv")

        self.sentiment_words = pd.read_csv("polarity.csv")
        self.db_in = Sql('sociallistening','sent')
        self.sstime = datetime.datetime.now()
        self.nlp = Kkma()
        self.keyword = keyword
        self.category = category
        self.sub_keyword = sub_keyword
        self.channel = channel
        self.quantity = quantity
        self.brand = brand
        self.startDate = startDate
        self.endDate = endDate
    def pol_anaylze(self):

            conn = pymysql.connect(host='106.246.169.202', user='root', password='robot369',
                                   db='crawl', charset='utf8mb4')
            # 106.246.169.202
            # 192.168.0.105
            curs = conn.cursor(pymysql.cursors.DictCursor)
            sql = "select * from htdocs where keyword=\'%s\' and channel=\'%s\' and publishtime>=\'%s\' and publishtime<=\'%s\' and htmltext like '%s' limit %s" % \
                   (self.keyword, self.channel, self.startDate, self.endDate, '%'+self.brand+'%',self.quantity)
            # sql = "select * from htdocs where keyword=\'%s\'"%(self.keyword)
            curs.execute(sql)
            rows = curs.fetchall()

            total_sum_pos=0
            total_sum_neg=0
            total_sum_neu=0
            for i, row in enumerate(rows):
                self.text=''
                phrase = row['htmltext']
                id_naver = row['postid']
                keyword = row['keyword']
                publishtime = row['publishtime']
                brand = self.brand
                category = self.category
                id_task = self.id_task
                sub_keyword = self.sub_keyword
                channel = self.channel
                content = phrase
                sub_key_list = sub_keyword.split(',')
                #content 문장 분할하기
                splited_lp = kss.split_sentences(phrase)
                for i in splited_lp:
                    for j in sub_key_list:
                        if j in i:
                            self.text+=i
                self.cleanser()
                try:
                    result = self.nlp.pos(self.text)
                except Exception as e:
                    print(e)
                res = ';'
                try:
                    for r in result:
                        res += r[0] + "/" + r[1] + ";"
                    res = self.tagConvert(res)
                except:
                    continue

                n_sent_all=0
                point_pos_all = 0
                point_neg_all = 0
                point_neu_all = 0

                for i in reversed(range(len(self.sentiment_words))):
                    ngram = self.sentiment_words.iloc[i, 0]
                    ngStr = re.sub('/[A-Z]+;', '', ngram + ';')



                    k = res.count(ngram)
                    if k > 0:
                        n_sent_all+=k
                        point_pos = self.sentiment_words.iloc[i, 6]
                        point_neg = self.sentiment_words.iloc[i, 3]
                        point_neu = self.sentiment_words.iloc[i, 4]
                        point_pos_all += point_pos * k
                        point_neg_all += point_neg * k
                        point_neu_all += point_neu * k

                point_pos_avg = point_pos_all/n_sent_all if n_sent_all>0 else 0
                point_neg_avg = point_neg_all/n_sent_all if n_sent_all>0 else 0
                point_neu_avg = point_neu_all/n_sent_all if n_sent_all>0 else 0

                #print('phrase:',phrase)
                print('index:',id_naver,'keyword:',keyword,'category:',category,'sub_keyword:',sub_keyword,'point_pos_avg:',point_pos_avg,'point_neg_avg:',point_neg_avg, 'point_neu_avg:',point_neu_avg)
                if n_sent_all>0:
                    self.db_in.insert('sent',
                        id_naver = id_naver,
                        id_task = id_task,
                        keyword = keyword,
                        brand= brand,
                        category=keyword,
                        sub_keyword=sub_keyword,
                        channel = channel,
                        publishtime = publishtime,
                        content = content,
                        pos = str(point_pos_avg),
                        neg = str(point_neg_avg),
                        neu = str(point_neu_avg)
                    )
                total_sum_pos += point_pos_all
                total_sum_neg += point_neg_all
                total_sum_neu += point_neu_avg
            T_point = total_sum_pos + total_sum_neg + total_sum_neu
            T_Pos_rate = total_sum_pos / T_point
            T_Neg_rate = total_sum_neg / T_point
            T_Neu_rate = total_sum_neu / T_point

            conn = pymysql.connect(host='106.246.169.202', user='root', password='robot369',
                                   db='sociallistening', charset='utf8mb4')
            # 106.246.169.202
            # 192.168.0.105
            curs = conn.cursor(pymysql.cursors.DictCursor)
            sql_u = "update tasksent set status='DF',pos_num=%s, neg_num=%s,neu_num=%s, pos_rate=%s, neg_rate=%s, neu_rate=%s,nurl=%s where id=%s"%\
                    (total_sum_pos, total_sum_neg, total_sum_neu, T_Pos_rate, T_Neg_rate,T_Neu_rate,len(rows), self.id_task)
            curs.execute(sql_u)
            conn.commit()
            conn.close()

    def cleanser(self):
        self.text = re.sub(u"(http[^ ]*)", " ", self.text)
        self.text = re.sub(u"@(.)*\s", " ", self.text)
        self.text = re.sub(u"#", "", self.text)
        self.text = re.sub(u"\\d+", " ", self.text)
        self.text = re.sub(u"[^가-힣A-Za-z]", " ", self.text)
        self.text = re.sub(u"\\s+", " ", self.text)
