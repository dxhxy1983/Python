
from PIL import Image
import numpy as np
import jieba
from matplotlib import get_backend
from wordcloud import WordCloud
with open(r'C:\Users\DXHQXX\Documents\gitee\北京理工Python\二十大报告.txt', 'r',encoding="utf_8") as file1:
    txt= file1.read() 
# txt="这是中国胜利得时候,同志们,我们五年来辛苦了"
stp_words=["同志","五年","十年",'们','来']  
   
words = jieba.cut(txt)     #精确分词
stayed_line=""
for word in words:
    if word not in stp_words:
        stayed_line+=word

# newtxt = ''.join(words)    #空格拼接
newtxt = ''.join(stayed_line)
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
