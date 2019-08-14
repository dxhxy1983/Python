import turtle
def drawSnake(rad,angle,len,neckrad):
    for i in range(len):
        turtle.circle(rad,angle)
        turtle.circle(-rad,angle)
    turtle.circle(rad,angle/2)
    turtle.fd(rad)
    turtle.circle(neckrad+1,180)
    turtle.fd(rad*2/3)
def main():
    turtle.setup(800,480,0,0)
    pythonsize=20
    turtle.pensize(pythonsize)
    turtle.pencolor('blue')
    turtle.seth(-40)
    drawSnake(40,80,5,pythonsize/2)
main()
