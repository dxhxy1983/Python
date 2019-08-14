f=open('latex.log').read()
l=list(f)
r={}
for i in range(len(l)):
    if l[i] not in r:
        r[l[i]]=1
    else:
        r[l[i]]=r[l[i]]+1

sum=0

con={'a','b','c','d','e','f','g','h','i','j','k',
    'l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'}   
new={}    
for word in r:
    if word in con:
        new[word]=r[word]
for key in new:
    if key in ['a','b','c','d','e','f','g','h','i','j','k',\
                'l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']:
            # 'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']:
       sum+=new[key]
# print('共{}字符'.format(sum),end=',')
# for key in sorted(new):
#     if key!='z':
#         print("{}:{}".format(key,new[key]),end='\n')
#     else:
#         print("{}:{}".format(key,new[key]))
for key in sorted(new):
     print("{}".format(new[key]))
# b=list(new.items())
# b.sort(key=lambda x:x[0], reverse=False)
# for i in range(len(b)):
#     print()
# print(b)    
