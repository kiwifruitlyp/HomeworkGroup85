import asm3
import random
import time
# 辗转相除法求最大公因子
def gcd(a,b):
    r=a%b
    while(r!=0):
        a=b
        b=r
        r=a%b
    return b

# 扩展欧几里算法求模逆
def inverse(a, m): 
    if gcd(a, m) != 1:
        return None #若a和m不互质，则不存在模逆
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3 
        v1 , v2, v3, u1 , u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1 , v2, v3
    return u1 % m

# 椭圆曲线上的加法
def epoint_add(P,Q):
    if (P == 0):
        return Q
    if (Q == 0):
        return P
    if P == Q:
        t1 = (3 * (P[0]**2) + a)
        t2 = inverse(2 * P[1], p)
        k = (t1 * t2) % p 
    else:
        t1 = (P[1] - Q[1])
        t2 = (P[0] - Q[0])
        k = (t1 * inverse(t2,p)) % p 

    X = (k * k - P[0] - Q[0]) % p 
    Y = (k * (P[0] - X) - P[1]) % p 
    Z = [X,Y]
    return Z


# 椭圆曲线上的点乘
def epoint_mul(k, g):
    if k == 0:
        return 0
    if k == 1:
        return g
    r = g
    while (k >= 2):
        r = epoint_add(r, g)
        k = k - 1
    return r

# SM2签名
def SM2_signature(message):
    global n,g,d,ZA,k
    M = ZA + message
    e = asm3.SM3(M)
    Z = epoint_mul(k,g)
    r = (Z[0] + int(e,16)) % n
    e = hash(message)
    s = (inverse(1 + d, n) * (k - d * r)) % n
    return r,s

# ECDSA签名
def ECDSA_signature(message):
    global n,g,d
    k = random.randint(1,n-1)
    Z = epoint_mul(k,g)
    r = Z[0] % n
    e = hash(message)
    s = (inverse(k, n) * (e + d * r)) % n
    return r,s

#椭圆曲线参数
n = 19
p = 17
a = 2
b = 2    
x = 5
y = 1
g = [x, y]
k = 7

m = '20230324'
start_time = time.perf_counter()
e = hash(m)
d = 5
pk = epoint_mul(d, g)
ID_A = '1321699113'
tmp = str(len(ID_A))+ID_A+str(a)+str(b)+str(g[0])+str(g[1])+str(pk[0])+str(pk[1])
ZA = asm3.SM3(tmp)

# k泄露
r,s = SM2_signature(m)
sk = (inverse(s + r,n) * (k - s))%n
print('\n泄露的k:')
print("私钥:",sk)

# k重用
m1 = '20230324'
m2 = '20230412'
r1,s1 = SM2_signature(m1)
r2,s2 = SM2_signature(m2)
sk = ((s2 - s1) * inverse((s1 - s2 + r1 - r2),n))%n
print('\n重用的k:')
print("私钥:",sk)

# 不同用户重用k
r1,s1 = SM2_signature(m1)
r2,s2 = SM2_signature(m2)
sk1 = ((k - s1) * inverse(s1 + r1,n))%n
sk2 = ((k - s2) * inverse(s2 + r2,n))%n
print('\n不同用户重用k:')
print("推出私钥key1:",sk1)
print("推出私钥key2:",sk2)

# 使用和ECDSA相同的d与k
e1 = hash(m)
r1,s1 = SM2_signature(m1)
r2,s2 = ECDSA_signature(m2)
sk = ((s1 * s2 - e1) * inverse((r1 - s1 * s2 - s1 * r2),n))%n
end_time = time.perf_counter()
print('\n使用和ECDSA相同的d与k:')
print("私钥:",sk)
print('程序运行时间:', end_time - start_time, '秒')
