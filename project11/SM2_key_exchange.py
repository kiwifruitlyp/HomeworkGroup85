from random import randint
import math
from gmpy2 import invert
import random
import binascii
import math
import time
from SM2_Enc_Dec import mul_add,Hash,add,KDF
iv = "7380166F4914B2B9172442D7DA8A0600A96F30BC163138AAE38DEE4DB0FB0E4E"
T = (0x79cc4519, 0x7a879d8a)
index = "0123456789ABCDEF"
W = []
W_ = []

p=0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3    #256
a=0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b=0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
n=0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
Gx=0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
Gy=0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2

da=0x6FCBA2EF9AE0AB902BC3BDE3FF915D44BA4CC78F88E2F8E7F8996D3B8CCEEDEE
db=0x5E35D7D3F3C54DBAC72E61819E730B019A84208CA3A35E4C2E353DFCCB2A3B53


#定义交换方的标识符IDa和IDb
IDa="ALICE123@YAHOO.COM"
#使用椭圆曲线上的点Gx和Gy和私钥da计算公钥Pka
Pka=mul_add(Gx,Gy,da)

IDb="BILL456@YAHOO.COM"
#使用椭圆曲线上的点Gx和Gy和私钥db计算公钥Pkb
Pkb=mul_add(Gx,Gy,db)

w=math.ceil(math.ceil(math.log2(n))/2)-1
h=1
klen=128


#B方进行密钥交换
def B_key_exchange(*Ra):
    #rb为B方私钥
    rb = 0x33FE21940342161C55619C4A0C060293D543C80AF19748CE176D83477DE71C80
    #Rb为B方公钥
    Rb = mul_add(Gx, Gy, rb)
    ida = hex(int(binascii.b2a_hex(IDa.encode()).decode(), 16)).upper()[2:]
    ENTLa = '{:04X}'.format(len(ida) * 4)
    ma = ENTLa + ida + '{:064X}'.format(a) + '{:064X}'.format(b) + '{:064X}'.format(Gx) + '{:064X}'.format(
        Gy) + '{:064X}'.format(Pka[0]) + '{:064X}'.format(Pka[1])
    Za = Hash(ma)
    idb = hex(int(binascii.b2a_hex(IDb.encode()).decode(), 16)).upper()[2:]
    ENTLb = '{:04X}'.format(len(idb) * 4)
    mb = ENTLb + idb + '{:064X}'.format(a) + '{:064X}'.format(b) + '{:064X}'.format(Gx) + '{:064X}'.format(
        Gy) + '{:064X}'.format(Pkb[0]) + '{:064X}'.format(Pkb[1])
    Zb = Hash(mb)
    x2=((1<<w)+(Rb[0]&((1<<w)-1)))%(1<<128)
    tb=(db+x2*rb)%n
    x1=((1<<w)+(Ra[0]&((1<<w)-1)))%(1<<128)
    x,y=mul_add(Ra[0],Ra[1],x1)
    x,y=add(Pka[0],Pka[1],x,y)
    V=mul_add(x,y,h*tb)
    t1, t2 = '{:064X}'.format(V[0]), '{:064X}'.format(V[1])
    m=t1+t2+Za+Zb
    #将m进行二进制转换，并进行128位的KDF计算，得到密钥Kb
    m='{:01024b}'.format(int(m,16))
    Kb=KDF(m,klen)
    return hex(int(Kb,2)).upper()[2:]
#A方进行密钥交换
def A_key_exchange(*Rb):
    #ra为A方私钥
    ra = 0x83A2C9C8B96E5AF70BD480B472409A9A327257F1EBB73F5B073354B248668563
    #Ra为A方公钥
    Ra = mul_add(Gx, Gy, ra)
    ida = hex(int(binascii.b2a_hex(IDa.encode()).decode(), 16)).upper()[2:]
    ENTLa = '{:04X}'.format(len(ida) * 4)
    ma = ENTLa + ida + '{:064X}'.format(a) + '{:064X}'.format(b) + '{:064X}'.format(Gx) + '{:064X}'.format(
        Gy) + '{:064X}'.format(Pka[0]) + '{:064X}'.format(Pka[1])
    Za = Hash(ma)
    idb = hex(int(binascii.b2a_hex(IDb.encode()).decode(), 16)).upper()[2:]
    ENTLb = '{:04X}'.format(len(idb) * 4)
    mb = ENTLb + idb + '{:064X}'.format(a) + '{:064X}'.format(b) + '{:064X}'.format(Gx) + '{:064X}'.format(
        Gy) + '{:064X}'.format(Pkb[0]) + '{:064X}'.format(Pkb[1])
    Zb = Hash(mb)
    x1=((1<<w)+(Ra[0]&((1<<w)-1)))%(1<<128)
    ta=(da+x1*ra)%n
    x2=((1<<w)+(Rb[0]&((1<<w)-1)))%(1<<128)
    x,y=mul_add(Rb[0],Rb[1],x2)
    x,y=add(Pkb[0],Pkb[1],x,y)
    U=mul_add(x,y,h*ta)
    t1, t2 = '{:064X}'.format(U[0]), '{:064X}'.format(U[1])
    m=t1+t2+Za+Zb
    m='{:01024b}'.format(int(m,16))
    Ka=KDF(m,klen)
    return hex(int(Ka, 2)).upper()[2:]


#ra=randint(1,n)
ra=0x83A2C9C8B96E5AF70BD480B472409A9A327257F1EBB73F5B073354B248668563
start_time1 = time.perf_counter()
Ra=mul_add(Gx,Gy,ra)#计算公钥Ra
end_time1 = time.perf_counter()
#rb=randint(1,n)
rb=0x33FE21940342161C55619C4A0C060293D543C80AF19748CE176D83477DE71C80
start_time2 = time.perf_counter()
Rb=mul_add(Gx,Gy,rb)#计算公钥Rb
end_time2 = time.perf_counter()
print(B_key_exchange(*Ra))
print('计算公钥Ra所需时间:', end_time1 - start_time1, '秒')
print(A_key_exchange(*Rb))
print('计算公钥Rb所需时间:', end_time2 - start_time2, '秒')
