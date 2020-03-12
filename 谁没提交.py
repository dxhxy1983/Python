import jieba
namelist=open('C:\\Users\\D\\Documents\\Python\\namelist.txt', 'r').read()

allstudents=open('C:\\Users\\D\\Documents\\Python\\allstudents.txt', 'r').read()

for keyword in allstudents:
    jieba.add_word(keyword)
jieba.load_userdict
word=jieba.lcut(namelist)
print(word)