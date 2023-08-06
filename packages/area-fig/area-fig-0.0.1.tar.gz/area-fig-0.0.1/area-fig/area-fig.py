def square(a):
    a = a**2
    p = a*4
    print(f"Area of square is: {a} & perimeter is: {p}")

def rectangle(l,b):
    a = l*b
    p = 2*(l+b)
    print(f"Area of rectangle is: {a} & perimeter is: {p}")

def triangle(a,b,c,height):
    ar = (1/2)*b*height
    p = a + b + c
    print(f"Area of triangle is: {ar} & perimeter is: {p}")

def circle(r):
    a = 3.14*r*r
    p = 2*3.14*r
    print(f"Area of circle is: {a} & perimeter is: {p}"
