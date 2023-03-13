import os,sys
import pandas as pd
import shutil
def DFS_file_search(dict_name):
    
    # list.pop() list.append()这两个方法就可以实现栈维护功能
    stack = []
    result_txt = []
    stack.append(dict_name)
    while len(stack) != 0:  # 栈空代表所有目录均已完成访问
        temp_name = stack.pop()
        try:
            temp_name2 = os.listdir(temp_name) # list ["","",...]
            for eve in temp_name2:
                stack.append(temp_name + "\\" + eve)  # 维持绝对路径的表达
        except NotADirectoryError:
            result_txt.append(temp_name)
    return result_txt


if __name__=="__main__":
    #获取当前文件目录
    current_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    file_path=current_path+"\\settings.txt"
    # print(current_path)
    parametersList=[]
    sourceList=[]
    
    with open(file_path,'r',encoding="utf-8") as f:
        line=f.readlines()
        for i in range(len(line)):
            line[i]=line[i].strip('\n')
            parametersList.append(line[i])

    #获得查找源目录
    
    for i in range(len(parametersList)):
        listA=DFS_file_search(parametersList[i])
        sourceList.append(listA)
    #获得要查找的文件名
    IO=current_path+"\\文件查找.xlsx"
    readedExcel=pd.read_excel(io=IO)
    df = pd.DataFrame(readedExcel)
    # print(df)
    fileName=[]
    for index, row in df.iterrows():
        # print(row[1]+"-"+row[0])
        fileName.append(str(row[1])+"-"+str(row[0]))

    #获得要找的文件路径
    listFilePath=[]
    listSuccess=[]
    #获得查到的文件路径
  
    for j in range(len(fileName)):
        for i in range(len(sourceList)):
            for k in range(len(sourceList[i])):
                if fileName[j] in sourceList[i][k]:
                    listFilePath.append(sourceList[i][k])
                    listSuccess.append(fileName[j])


    setFileName=set(fileName)
    setSuccess=set(listSuccess)
    listFailed=setFileName^setSuccess
    # print(listFilePath)
    dstpath=current_path+ r"\\"
    #复制文件到指定目录
    for fPath in listFilePath:
        fpath,fname=os.path.split(fPath)
        # print(dstpath+fname)
        shutil.copy(fPath, dstpath +fname)

    file_path=current_path+"\\查找失败的文件.txt"
    with open(file_path,'a',encoding="utf-8") as f:
        for i in listFailed:
            f.write(i)
            f.write("\n")
    f.close()


    # file_path=current_path+"\\目标文件列表.txt"
    # with open(file_path,'a',encoding="utf-8") as f:
    #     for i in sourceList:
    #         f.write(i)
    #         f.write("\n")
    # f.close()  

    # file_path=current_path+"\\待查列表.txt"
    # with open(file_path,'a',encoding="utf-8") as f:
    #     for i in fileName:
    #         f.write(i)
    #         f.write("\n")
    # f.close()  
    





