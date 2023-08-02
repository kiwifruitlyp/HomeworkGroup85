from random import randint
import math
from gmpy2 import invert
import random
import binascii
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

da=0x128B2FA8BD433C6C068C8D803DFF79792A519A55171B1B650C23661D15897263
#签名
def signature(m,Za):
    m1=Za+m
    e=Hash(m1)#计算拼接后的Za和m的哈希值
    #k=randint(1,n)#生成随机数k
    k=0x6CB28D99385C175C94F94E934817663FC176D925DD72B727260DBAAE1FB2F96F
    x1,y1=mul_add(Gx,Gy,k)
    r=(int(e,16)+x1)%n
    s=(invert(1+da,n)*(k-r*da))%n
    return (hex(r)[2:].upper(),hex(s)[2:].upper())
#验证
def Verify(r,s,Za,m,Pa):
    if int(r,16) not in range(1,n-1):
        return False
    if int(s,16) not in range(1,n-1):
        return False
    m1=Za+m
    e=Hash(m1)
    t=(int(r,16)+int(s,16))%n
    if t==0:
        return False
    x1,y1=mul_add(Pa[0],Pa[1],t)
    x2,y2=mul_add(Gx,Gy,int(s,16))
    x1,y1=add(x2,y2,x1,y1)
    R=(int(e,16)+x1)%n
    if(hex(R)[2:].upper()==r):
        return True
    return False


Pax,Pay=mul_add(Gx,Gy,da)# 计算公钥 Pa 的横纵坐标
Pa=(Pax,Pay)
m="Liyupei"
m=hex(int(binascii.b2a_hex(m.encode()).decode(),16)).upper()[2:]
IDa="ALICE123@YAHOO.COM" 
ida=hex(int(binascii.b2a_hex(IDa.encode()).decode(),16)).upper()[2:]
ENTLa='{:04X}'.format(len(ida)*4)
m1=ENTLa+ida+'{:064X}'.format(a)+'{:064X}'.format(b)+'{:064X}'.format(Gx)+'{:064X}'.format(Gy)+'{:064X}'.format(Pa[0])+'{:064X}'.format(Pa[1])
Za=hex(int(Hash(m1),16))[2:].upper()
start_time1 = time.perf_counter()
sign=signature(m,Za)# 生成数字签名
end_time1 = time.perf_counter()
print('生成数字签名所需时间:', end_time1 - start_time1, '秒')
start_time2 = time.perf_counter()
print(Verify(*sign,Za,m,Pa)) # 验证数字签名
end_time2 = time.perf_counter()
print('验证数字签名所需时间:', end_time2 - start_time2, '秒')
