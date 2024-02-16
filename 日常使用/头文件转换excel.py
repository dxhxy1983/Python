fPath=r"F:\myDoc\github\Python\日常使用\add.txt"

try:
    f = open(fPath)
    # print(f)
except:    
    print("open excel file failed!")
ls = f.readlines()
# ls = ls[::-1] #内容倒序

lt = []
for item in ls:
    item = item.strip("\n")
    # item = item.replace(" ", "")
    lt = item.split(" ")
    # print(lt)
    # lt = lt[::-1]
    print(",".join(lt))
    
f.close()