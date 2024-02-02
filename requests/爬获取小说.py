import requests
from lxml import etree 
# url="https://www.xiaoyaoshuge.com/xiaoshuo/1/3.html"
url="http://www.baidu.com"
header={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763'
}
resp=requests.get(url,headers=header)
resp.encodeing='utf-8'
e=etree.HTML(resp.text)
print(resp.text)
