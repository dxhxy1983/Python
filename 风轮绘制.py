def main():
    import turtle as t
    t.setup(800, 400)
    t.speed(1)
    t.left(45)

    for i in range(4):
        t.fd(150)
        t.left(90)
        t.circle(150, 45)
        t.left(90)
        t.fd(150)
        t.left(45)
    t.done()

main()
