from polSeoul_category_NaverBlog_bae import *
import sys
keyword = sys.argv[1]
brand = sys.argv[2]
category = sys.argv[3]
sub_keyword = sys.argv[4]
channel = sys.argv[5]
startDate = sys.argv[6]
endDate = sys.argv[7]

quantity = sys.argv[8]

pa = Pol_Analyzer(keyword, brand,category, sub_keyword ,channel,startDate, endDate,quantity)

pa.pol_anaylze()
#pool = Pool(processes=4) # 4개의 프로세스를 사용합니다.
#pool.map(pa, ) # pool에 일을 던져줍니다.
