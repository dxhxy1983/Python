import os,sys
import pandas as pd
import shutil
import re
def open_excel(path):
    try:    
        book = pd.read_excel(path)
        return book
    except:
        print("open excel file failed!")

def find_files(folder, extension):
    file_list = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(extension):
                file_list.append(os.path.join(root, file))
    return file_list

if __name__=="__main__":
    #获取当前文件目录
    current_path = os.path.dirname(os.path.realpath(sys.argv[0]))

    
    extension=".xlsx"
    file_list = find_files(current_path, extension)
    # print(file_list)
    # print(current_path)
    if file_list!=None:
        file_path=file_list[0]
    parametersList=[]
    sourceList=[]
    b=open_excel(file_path)
    # b.set_axis(b.iloc[0], axis=1, inplace=True)
    columns_name= b.columns.tolist()
    # print(columns_name)

    # b.drop(0, inplace=True)
    # print(b)
    index1="合同号"
    index2="产品名称"
    # a=b.drop(0)
    dataFrame=b[[index1,index2]]
    print(dataFrame)
    # dataFrame.columns=[index1,index2]
    # print(dataFrame)
    # strName=dataFrame.loc[0,index1]
    for i in range(dataFrame.iloc[:,0].size):
        strName=str(i+1)+"-"+dataFrame.loc[i,index1]+dataFrame.loc[i,index2]
        sourceList.append(strName)
    
    for i in range(len(sourceList)):
        os.path.exists(current_path)
        sourceList_a=re.findall(r'[^\*"/:?\\|<>]',sourceList[i],re.S) 
        sourceList_b="".join(sourceList_a)
        isExists = os.path.exists(current_path+"\\"+sourceList_b)
        if not isExists:
        # 创建文件夹 路径+名称
            os.makedirs(current_path+"\\"+sourceList_b)
            print("%s 目录创建成功"+sourceList_b)
        else:
            print("%s 目录创建失败"+sourceList_b)
            continue
   