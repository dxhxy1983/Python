
with open('a.txt','w+',encoding='utf-8') as f:
    lines=['1111\n','222','3333']
    for line in lines:
        f.writelines(line)