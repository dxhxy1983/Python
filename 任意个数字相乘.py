
def cmul(a,*b):
    c=a
    for i in b:
        c*=i
    return c

print(("cmul({})".format((input()))))