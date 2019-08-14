from  turtle import  Turtle


def main():
    p=Turtle()
    p.color("green")
    p.pensize(5)
    p.speed(0.0000001)
#    p.hideturtle()
    p.getscreen().tracer(30,0)
    p.left(90)
    p.penup()
    x,y=0,0
    p.goto(x,y)
    p.pendown()
    t=tree([p],210,65,0.6375)
    
def tree(plist,l,a,f):
    if l>5:
        lst=[]
        for p in plist:
            p.forward(l)
            q=p.clone()
            p.left(a)
            q.right(a)
            lst.append(p)
            lst.append(q)
            
        tree(lst,l*f,a,f)
main()
