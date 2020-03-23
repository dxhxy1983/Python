import jieba
allstudents=open('C:\\Users\\D\\Documents\\Python\\学生名单.txt', 'r').read()
allList=allstudents.split()
jieba.load_userdict(allList)
namelist=open('C:\\Users\\D\\Documents\\Python\\接龙内容.txt', 'r').read()
namelist=jieba.lcut(namelist)

inList=[]
for keyword in allList:
    if keyword in namelist:
        inList.append(keyword)
print(namelist)
b=set(allList)-set(inList)
print(b)