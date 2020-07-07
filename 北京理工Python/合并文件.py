# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 16:21:19 2019

@author: D
"""

def main():
    EmailBook=open('C:\\Users\\D\\Documents\\Python\\EmailBook.txt','rb')
    TelBook=open('C:\\Users\\D\\Documents\\Python\\TelBook.txt','rb')
    # EmailBook.readline()
    # TelBook.readline()
    linesEmailBook=EmailBook.readlines()
    linesTelBook=TelBook.readlines()
#    print(EmailBook)
    # print(str(linesEmailBook[0],'utf-8'))
    # print(TelBook)
    # print(linesTelBook[0])
    list1Name=[]
    list1Email=[]
    list2Name=[]
    list2Tel=[]
    line1=[]

    for line in linesEmailBook:
        elements=line.split()
        list1Name.append(str(elements[0],'utf-8'))
        list1Email.append(str(elements[1],'utf-8'))
        print(list1Name)
        print(list1Email)
    for line in linesTelBook:
        elements=line.split()
        list2Name.append(str(elements[0],'utf-8'))
        list2Tel.append(str(elements[1],'utf-8'))
        print(list2Name)
        print(list2Tel)
    for i in range(len(list1Name)):
        s=''
        if list1Name[i] in list2Name:
            j=list2Name.index(list1Name[i])
            s='\t'.join([list1Name[i],list1Email[i],list2Tel[j]] )
            s+='\n'
        else:
            s='\t'.join([list1Name[i],list1Email[i],str('  -----------')])
            s+='\n'
        line1.append(s)
        print(line1)
    for i in range(len(list2Name)):
        s=''
        if list2Name[i] not in list1Name:
            s='\t'.join([list2Name[i],str('  -----------'),list2Tel[i]])
            s+='\n'
        line1.append(s)
        print(line1)
    file=open('C:\\Users\\D\\Documents\\Python\\allbook.txt','w')
    file.writelines(line1)
    file.close()
    EmailBook.close()
    TelBook.close()
    print('join File finish')
main()