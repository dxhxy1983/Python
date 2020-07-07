s=eval(input())
news={}
if type(s)==dict:
    for key,value in s.items():
        key,value=value,key
        news[key]=value
        
else:
    print("输入错误")
if type(s)==dict:
    print(news)