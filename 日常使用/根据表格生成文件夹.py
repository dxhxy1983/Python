import os,sys
import pandas as pd
import shutil
def open_excel(path):
    try:    
        book = pd.read_excel(path)
        return book
    except:
        print("open excel file failed!")


if __name__=="__main__":
    #获取当前文件目录
    current_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    file_path=current_path+"\\1.xlsx"
    # print(current_path)
    parametersList=[]
    sourceList=[]
    a=open_excel(file_path)
    index1="合同号"
    index2="产品名称"
    dataFrame=a[[index1,index2]]
    # strName=dataFrame.loc[0,index1]
    for i in range(dataFrame.iloc[:,0].size):
        strName=dataFrame.loc[i,index1]+dataFrame.loc[i,index2]
        sourceList.append(strName)
    
    
   