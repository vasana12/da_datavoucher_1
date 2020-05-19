from threading import Thread
from crawlLibInstagram import *


########################################################################################################################

                                ##      ##        ##        ######    ##      ##
                                ####  ####      ##  ##        ##      ##      ##
                                ##  ##  ##    ##      ##      ##      ####    ##
                                ##  ##  ##    ##      ##      ##      ##  ##  ##
                                ##      ##    ##########      ##      ##    ####
                                ##      ##    ##      ##      ##      ##      ##
                                ##      ##    ##      ##    ######    ##      ##

########################################################################################################################



keyword1 = '제주도맛집'

channel = 'Instagram'



nUrl = 1000


##### URL List 생성
# delete from urllist
# delete from htdocs

InstagramLister1=InstagramLister(nUrl, keyword1, channel)
InstagramLister1.getInstagramUrl()
