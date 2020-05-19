from engine_sent import *
keyword = "종로1가동 범죄"
channel = 'Naver Blog'
startDate = '2010-01-01'
endDate = '2014-12-31'
nUrl = 99999
t_1 = TextAnalyzer(keyword,channel, startDate, endDate, "Mecab", nUrl)

t_1.e_sent()
