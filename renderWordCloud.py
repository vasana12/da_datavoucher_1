from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import os
import matplotlib
from matplotlib.colors import LinearSegmentedColormap

matplotlib.use('TkAgg')

class WordCloudRenderer:
    def __init__(self, d, pal):
        self.dict = dict(d)
        self.maskPic = np.array(Image.open("./mask.png"))
        self.palette= pal
        self.dir = os.path.dirname(os.path.realpath(__file__))
        self.fontname = 'RixMGo_QPro Medium.otf'
        # self.colors = ["#75D701","#f9320c","#f9c00c","#0080ff",]

    def setMask(self, filename):
        self.maskPic = np.array(Image.open(filename))

    def getWordCloud(self):
                              ## NanumBarunGothic.ttf',

        # cmap = LinearSegmentedColormap.from_list("mycmap", self.colors)

        wordcloud = WordCloud(font_path=self.dir+"/fonts/"+self.fontname,\
                                  background_color="rgba(255, 255, 255, 0)", mode="RGBA",\
                                  max_font_size=120, \
                                  min_font_size=18, \
                                  mask=self.maskPic, \
                                  width=200, height=200, \
                                  colormap=self.palette)\
                        .generate_from_frequencies(self.dict)
        return wordcloud
    
        
    def draw(self, index , keyword):

        wordcloud = WordCloud(font_path=self.dir+"/fonts/"+self.fontname,\
                              background_color="rgba(255,255,255,0)", mode='RGBA', \
                              max_font_size=120, \
                              min_font_size=18, \
                              mask=self.maskPic, \
                              width=200, height=200, \
                              colormap=self.palette)\
                    .generate_from_frequencies(self.dict)
        wordcloud.to_file("transparent_"+keyword+".png")
        plt.figure(index, figsize=(12, 12))
        plt.imshow(wordcloud, interpolation='bilinear')

        plt.axis('off'), plt.xticks([]), plt.yticks([])
        plt.tight_layout()
        plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)

        plt.savefig('image/'+keyword,  bbox_inces='tight',  pad_inches=0,
            dpi=100, transparent=True)
