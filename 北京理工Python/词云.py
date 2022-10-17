
from PIL import Image
import numpy as np
import jieba
from matplotlib import get_backend
from wordcloud import WordCloud
with open(r'C:\Users\DXHQXX\Documents\gitee\北京理工Python\二十大报告.txt', 'r',encoding="utf_8") as file1:
    txt= file1.read() 
# stp_words=["同志们","五年来"]  
jieba.del_word("同志们")
jieba.del_word("五年来")      
words = jieba.lcut(txt)     #精确分词

newtxt = ''.join(words)    #空格拼接

img = Image.open(r"北京理工Python\20.bmp") # 打开遮罩图片
mask = np.array(img) #将图片转换为数组

wordcloud = WordCloud(font_path =  r"C:\Windows\Fonts\msyh.ttc",
                    #   mask=mask,
                      width=1200,
                      height=800,
                      min_font_size=15,
                      max_font_size=100,
                      background_color="white",

                    ).generate(newtxt)
wordcloud.to_file('20大.jpg')
