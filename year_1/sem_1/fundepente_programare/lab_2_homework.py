# Problema 15: Gasiti cel mai mare numar prim mai mic
# sau egal cu un numar dat. Daca nu exista un astfel
# de numar, tipariti un mesaj

def isPrime(num: int):
    if num < 2: 
        return False

    # for(int d=2; d * d <= num; d++) (C++)
    d = 2
    while d*d <= num:
        if (num % d == 0):
            return False
        d += 1

    return True


def prim_special(n: int):
    i = n

    # optimizare pentru a ignora numerele pare
    # (mai putin 2, singurul numar prim par)
    if i==2: return 2
    if i%2==0:
        i-=1

    while i > 1:
        if isPrime(i):
            return i
        i -= 2

    # daca nu exista
    print("Nu Exista")
    return None


# Teste:

# Teste pentru 'isPrime' helper function
assert isPrime(1) == False
assert isPrime(0) == False
assert isPrime(-3) == False

assert isPrime(2) == True
assert isPrime(4) == False
assert isPrime(17) == True
assert isPrime(21) == False


# Teste pentru rezolvarea cerintei (prim_special)
assert prim_special(10) == 7      # cel mai mare prim <= 10
assert prim_special(2) == 2       # n însuși este prim
assert prim_special(20) == 19
assert prim_special(1) == None    # nu există prim <= 1
assert prim_special(0) == None    # nu există prim <= 0
assert prim_special(29) == 29     # n însuși este prim
assert prim_special(30) == 29     # cel mai mare prim mai mic decât 30
assert prim_special(100) == 97


# Note despre optimizari:
# 1. functia isPrime verifica posibili divizori doar pana la sqrt(n)
# 2. functia prim_special nu mai verifica daca numerele pare sunt prime
# deoarece stim deja ca acestea nu sunt