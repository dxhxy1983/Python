f=open('latex.log')
l=f.readlines()
ly=[]
sumline=0
sumw=0
d = []
for i in range(26):
    d.append(chr(ord('a')+i))
for i in range(26):
    d.append((chr(ord('A')+i)))
# print(d)
for line in l:
    if line not in ['','\n']:
        ly.append(line.replace('\n',''))
print(ly)
for line in ly:
        for i in line:
            if i in d:
              sumw+=1
        sumline+=1
print(round(sumw/sumline))