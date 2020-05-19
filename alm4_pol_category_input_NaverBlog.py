from polSeoul_category_NaverBlog import *
import sys
keyword = '스마트폰'
brand = '갤럭시'
category = '사진'
sub_keyword = '사진찍기,앨범,짐벌,셀카,셀피'
channel = 'NaverBlog'
startDate = '2015-01-01'
endDate = '2020-05-19'

quantity = sys.argv[8]

pa = Pol_Analyzer(keyword, brand,category, sub_keyword ,channel,startDate, endDate,quantity)

pa.pol_anaylze()
#pool = Pool(processes=4) # 4개의 프로세스를 사용합니다.
#pool.map(pa, ) # pool에 일을 던져줍니다.
