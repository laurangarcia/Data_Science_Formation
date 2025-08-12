import math

def o(n):
    return 1

def o_log(n):
    return math.log(n)

def o_n_log(n):
    return n*math.log(n)

def o_n__2(n):
    return n**2

def o_2__n(n):
    return 2**n

values = [1, 10, 100, 1000, 10000, 100000]

for v in values:
    print(f"Constante:  o({v}) = {o(v)}")
    print(f"Logaritimica : o_log({v}) = {o_log(v)}")
    print(f"Logaritmica lineal: o_n_log({v}) = {o_n_log(v)}")
    print(f"Polinomial: o_n__2({v}) = {o_n__2(v)}")
    print(f"Exponencial:  o_2__n({v}) = {o_2__n(v)}")
