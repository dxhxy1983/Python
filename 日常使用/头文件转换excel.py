import openpyxl
workbook=openpyxl.Workbook()
sheet=workbook.active
# fPath=r"F:\myDoc\github\Python\日常使用\add.txt"
fPath=r"C:\Users\DXHQXX\Documents\gitee\日常使用\add.txt"

try:
    f = open(fPath)
    # print(f)
except:    
    print("open excel file failed!")
ls = f.readlines()
# ls = ls[::-1] #内容倒序

lt = []
i=0
for item in ls:
    i=i+1
    item = item.strip("\n")
    # item = item.replace(" ", "")
    lt = item.split(" ")
    # print(lt)
    # lt = lt[::-1]
    for j in range(len(lt)):
        sheet.cell(row=i,column=j+1).value=lt[j]
        
workbook.save("output.xlsx")
workbook.close()

    
f.close()