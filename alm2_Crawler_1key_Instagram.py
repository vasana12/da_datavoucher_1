from threading import Thread
#from crawlLibNaverBlog import *
#from crawlLibYouTube import *
#from textAnalyzer import *
#from renderWordCloud import *
#from setCalculus import *
from crawlLibInstagram import * 
import matplotlib.pyplot as plt
import pymysql

########################################################################################################################

                                ##      ##        ##        ######    ##      ##
                                ####  ####      ##  ##        ##      ##      ##
                                ##  ##  ##    ##      ##      ##      ####    ##
                                ##  ##  ##    ##      ##      ##      ##  ##  ##
                                ##      ##    ##########      ##      ##    ####
                                ##      ##    ##      ##      ##      ##      ##
                                ##      ##    ##      ##    ######    ##      ##

########################################################################################################################



keyword1 = '은평공원'
channel = 'Instagram'






Itcrawler = InstagramCrawler(keyword1, channel)

Itcrawler.crawlUrlTexts()
