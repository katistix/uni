n = int(input("a: "))
m = int(input("b: "))

while m!=0:
    r = n%m
    n=m
    m=r

print(n)