def gettext():
    txt=open('C:\\Users\\D\\Documents\\Python\\hamlet.txt','r').read()
    txt=txt.lower()
    for ch in '~·!@#￥%……&*()\^""/_+-{}[];?:".|,>=<''':
        txt=txt.replace(ch,' ')
    return txt
def main():
    txt=gettext()
    words=txt.split()
    count={}
    for wd in words:
        count[wd]=count.get(wd,0)+1
    items=list(count.items())
    items.sort(key=lambda x:x[1],reverse=True)
    for i in range(10):
        w,d=items[i]
        print("{:<5} {:>4}".format(w,d))

main()