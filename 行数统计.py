# w=open('latex.log', 'r', encoding='utf-8').readlines()
# line1=set(w)
# m=0
# # for i in range(len(w)):
# #     if w[i] not in ['','\n','[]']:
# #         m+=1
# print(len(line1))
f = open("latex.log")
ls = f.readlines()
s = set(ls)
for i in s:
    ls.remove(i)
t = set(ls)
print(len(s))
print(len(t))
# print("共{}独特行".format(len(s)-len(t)))