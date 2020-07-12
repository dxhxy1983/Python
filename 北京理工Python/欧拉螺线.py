import turtle
def koch(size, angle,n,s):
    while n<s:
        turtle.fd(size)
        
    

def main():
    turtle.setup(600,600)
    turtle.penup()
    turtle.goto(-200, 100)
    s=200
    angle=15
    size=30
    turtle.pendown()
    turtle.speed(100)
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