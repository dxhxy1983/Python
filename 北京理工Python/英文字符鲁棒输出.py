f=input()
# a=eval(f)
d = []
for i in range(26):
    d.append(chr(ord('a')+i))
for i in range(26):
    d.append((chr(ord('A')+i)))
for i in range(len(f)):
    if f[i] in d:
        print(f[i],end='')