from threading import Thread
from crawlLibNaverBlog import *
#from textAnalyzer import *
from renderWordCloud import *
from setCalculus import *
import matplotlib.pyplot as plt
from datetime import datetime

########################################################################################################################

                                ##      ##        ##        ######    ##      ##
                                ####  ####      ##  ##        ##      ##      ##
                                ##  ##  ##    ##      ##      ##      ####    ##
                                ##  ##  ##    ##      ##      ##      ##  ##  ##
                                ##      ##    ##########      ##      ##    ####
                                ##      ##    ##      ##      ##      ##      ##
                                ##      ##    ##      ##    ######    ##      ##


sstime = datetime.now()
keyword1 = '포도'

channel = 'Naver Blog'


startDate1 = '2010-01-01'
endDate1 = '2019-12-31'


########################################################################################################################







#### 생성된 URL List에 대해 crawling

crawler1 = NaverBlogCrawler(keyword1, channel, startDate1, endDate1)


th1 = Thread(target=crawler1.crawlUrlTexts)

th1.start()

th1.join()

fftime= datetime.now() - sstime

print('fftime=',fftime)
