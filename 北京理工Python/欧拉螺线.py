import turtle
def koch(size, angle,n,s):
    while n<s:
        turtle.fd(size)
        
    

def main():
    turtle.setup(1000,800)
    turtle.penup()
    turtle.goto(0, 0)
    s=3000
    angle=31
    size=10
    turtle.pendown()
    turtle.speed(30000)
    # turtle.hideturtle()
    turtle.pensize(1)
    for i in range(s) :
        turtle.fd(size)
        turtle.left(i*angle)

    turtle.done()
main()    
# try:
#     level = eval(input("请输入科赫曲线的阶: "))
#     main(level)
# except:
#     print("输入错误")