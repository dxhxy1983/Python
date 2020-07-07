f = open("7034.txt",encoding='utf-8')
ls = f.readlines()
# s = set(ls)
s=ls
title = '查找结果' + '.txt'

for i in range(len(s)):
    # if ('"write_data_11"[9]')in s[i] or '"read_data_11"' in s[i] and not 'PLC4' in s[i]:
      if("PLC_In_Storage_1"in s[i]):
        with open(title, "a") as f:
            f.write(s[i])
    
f.close()
