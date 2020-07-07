
trytimes=0
while trytimes<3:
    user=input()
    password=input()
    while user=='Kate' and password=='666666':
        print("登录成功！")
        trytimes=4
        break
        
    else:
        trytimes=trytimes+1
        
if 2<trytimes<4:
    print("3次用户名或者密码均有误！退出程序。")

