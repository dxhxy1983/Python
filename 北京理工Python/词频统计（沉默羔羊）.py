import jieba
s=open('C:\\Users\\D\\Documents\\Python\\沉默的羔羊.txt', 'r', encoding='utf-8').read()
words=jieba.lcut(s)
counts = {}
for word in words:
    if len(word) == 1:
        continue
    else:
        counts[word] = counts.get(word,0) + 1
items = list(counts.items())
items.sort(key=lambda x:x[1], reverse=True) 
for i in range(1):
    word, count = items[i]
    print ("{0}".format(word))