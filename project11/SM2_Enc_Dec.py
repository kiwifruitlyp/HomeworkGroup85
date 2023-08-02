from random import randint
import math
from gmpy2 import invert
import random
import binascii
import time
iv = "7380166F4914B2B9172442D7DA8A0600A96F30BC163138AAE38DEE4DB0FB0E4E"
T = (0x79cc4519, 0x7a879d8a)
index = "0123456789ABCDEF"
W = []# W数组，用于存储消息扩展过程中的中间结果
W_ = []#W_数组，用于存储消息扩展过程中的中间结果

# 左移函数
def LeftShift(num, left):
    return (((num << left)&((1<<32)-1)) | (num >> (32 - left)))

#Ti函数
def Ti(x):
    return (T[1]) if x > 15 else (T[0])


def FFi(x, y, z, n):
    return ((x & y) | (y & z) | (x & z)) if n > 15 else (x ^ y ^ z)


def GGi(x, y, z, n):
    return ((x & y) | ((~x) & z)) if n > 15 else (x ^ y ^ z)


def P0(x):
    return (x ^ LeftShift(x, 9) ^ LeftShift(x, 17))


def P1(x):
    return (x ^ LeftShift(x, 15) ^ LeftShift(x, 23))

#填充函数
def padding(n, size,s):
    s=list(s)
    s.append('8')
    for i in range(0, n // 4):
        s.append("0")
    s=''.join(s)
    s+=hex(size)[2:].zfill(16).upper()
    return n,s




#消息扩展函数
def Extend(B):
    for i in range(0, 16):
        W.append(int(B[(8 * i):(8 * i) + 8],16)%((1<<32)))

    for i in range(16, 68):
        W.append(int(hex((P1(W[i - 16] ^ W[i - 9] ^ LeftShift(W[i - 3], 15))) ^ (LeftShift(W[i - 13], 7) ^ W[i - 6])),16)%((1<<32)))

    for i in range(0, 64):
        W_.append(int(hex(W[i] ^ W[i + 4]),16)%((1<<32)))

index=['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']

# 将数字转换为16进制字符串
def uint_to_str(num,k = 8) :
    s=""
    for i in range(0,k):
        s+=index[num % 16]
        num//=16
    return  s[::-1]
# 更新V寄存器的值
def update(V, Bi):
    temp = []
    temp1 = []
    for i in range(0, 8):
        t="0x"+V[8 * i: (8 * i) + 8]
        temp.append(int(t,16))
        temp1.append(temp[i])
    for i in range(0, 64):
        SS1 = LeftShift((LeftShift(temp[0], 12) + temp[4] + LeftShift(Ti(i), i % 32))%(1<<32), 7)
        SS2 = (SS1 ^ LeftShift(temp[0], 12))
        t=(FFi(temp[0], temp[1], temp[2], i)+temp[3])%((1<<32))
        TT1 = (FFi(temp[0], temp[1], temp[2], i) + temp[3] + SS2 + W_[i])%(1<<32)
        TT2 = (GGi(temp[4], temp[5], temp[6], i) + temp[7] + SS1 + W[i])%(1<<32)
        temp[3] = temp[2]
        temp[2] = (LeftShift(temp[1], 9))
        temp[1] = temp[0]
        temp[0] = TT1
        temp[7] = temp[6]
        temp[6] = LeftShift(temp[5], 19)
        temp[5] = temp[4]
        temp[4] = P0(TT2)
    result = ""
    for i in range(0, 8):
        result += uint_to_str(temp1[i] ^ temp[i])
    return result.upper()

# 定义Hash函数，用于进行杂凑运算
def Hash(m):
    size = len(m) * 4
    # 计算输入消息所占的位数    
    num = (size + 1) % 512
    # 根据位数计算填充位数t
    t = 448 - num if num < 448 else 960 - num
    # 根据位数计算填充位数
    k ,m= padding(t,size,m)
    t=len(m)
     # 计算消息分组个数
    group_number = (size + 65 + k) // 512
    B = []# 存储分组数据，每个分组为128个bit
    IV = []# 存储初始化向量，初始为iv
    IV.append(iv)# 初始IV为固定值iv
     # 对每个分组进行操作
    for i in range(0, group_number):
        B.append(m[128 * i:128 * i + 128])# 将消息分为128bit一组
        Extend(B[i])# 进行扩展操作
        IV.append(update(IV[i], B[i]))# 更新IV
        W.clear()
        W_.clear()
    temp = IV[group_number]# 取最后一个IV作为结果
    return temp


p=0xBDB6F4FE3E8B1D9E0DA8C0D46F4C318CEFE4AFE3B6B8551F        #192  或  256
a=0xBB8E5E8FBC115E139FE6A814FE48AAA6F0ADA1AA5DF91985
b=0x1854BEBDC31B21B7AEFC80AB0ECD10D5B1B3308E6DBF11C1
n=0xBDB6F4FE3E8B1D9E0DA8C0D40FC962195DFAE76F56564677
Gx=0x4AD5F7048DE709AD51236DE65E4D4B482C836DC6E4106640
Gy=0x02BB3A02D4AAADACAE24817A4CA3A1B014B5270432DB27D2

da=0x58892B807074F53FBF67288A1DFAA1AC313455FE60355AFD
# 定义加法运算，用于椭圆曲线上点的加法
def add(x1,y1,x2,y2):
    # 判断两个点是否相等
    if x1==x2 and y1==p-y2:
        return False
    # 计算斜率
    if x1!=x2:
        lamda=((y2-y1)*invert(x2-x1, p))%p
    else:
        lamda=(((3*x1*x1+a)%p)*invert(2*y1, p))%p
    # 计算新的点坐标
    x3=(lamda*lamda-x1-x2)%p
    y3=(lamda*(x1-x3)-y1)%p
    return x3,y3
# 多倍加法运算，用于进行点的倍乘和加法操作
def mul_add(x,y,k):
    k=bin(k)[2:]
    qx,qy=x,y
    # 逐位计算倍乘和加法
    for i in range(1,len(k)):
        qx,qy=add(qx, qy, qx, qy)
        if k[i]=='1':
            qx,qy=add(qx, qy, x, y)
    return (qx,qy)

# 密钥派生函数，用于从输入得到派生密钥
def KDF(z,klen):
    ct=1
    k=''
    # 进行密钥派生
    for i in range(math.ceil(klen/256)):
        t=hex(int(z+'{:032b}'.format(ct),2))[2:]
        k=k+hex(int(Hash(t),16))[2:]
        ct=ct+1
    # 对派生得到的密钥进行长度调整
    k='0'*((256-(len(bin(int(k,16))[2:])%256))%256)+bin(int(k,16))[2:]
    return k[:klen]

h=1
# 加密函数，实现基于椭圆曲线密码学的加密过程
def encrypt(m):
    plen=len(hex(p)[2:])
    m='0'*((4-(len(bin(int(m.encode().hex(),16))[2:])%4))%4)+bin(int(m.encode().hex(),16))[2:]
    klen=len(m)
    while True:
        #k=randint(1,n)
        k=0x384F30353073AEECE7A1654330A96204D37982A3E15B2CB5
        while k==da:
            k=randint(1, n)
        x2,y2=mul_add(Pa[0],Pa[1],k)
        if(len(hex(p)[2:])*4==192):
            x2,y2='{:0192b}'.format(x2),'{:0192b}'.format(y2)
        else:
            x2, y2 = '{:0256b}'.format(x2), '{:0256b}'.format(y2)
        t=KDF(x2+y2, klen)
        if int(t,2)!=0:
            break
    x1,y1=mul_add(Gx, Gy,k)
    x1,y1=(plen-len(hex(x1)[2:]))*'0'+hex(x1)[2:],(plen-len(hex(y1)[2:]))*'0'+hex(y1)[2:]
    c1=x1+y1
    c2=((klen//4)-len(hex(int(m,2)^int(t,2))[2:]))*'0'+hex(int(m,2)^int(t,2))[2:]
    c3=Hash(hex(int(x2+m+y2,2))[2:].upper())
    return c1,c2,c3

def decrypt(c1,c2,c3):
    # 将c1分为两部分，分别表示x1的前半部分和后半部分
    x1,y1=int(c1[:len(c1)//2],16),int(c1[len(c1)//2:],16)
    # 验证曲线上的点是否满足椭圆曲线方程
    if pow(y1,2,p)!=(pow(x1,3,p)+a*x1+b)%p:
        return False
    # 计算(x2, y2)，使用私钥da对(x1, y1)进行扩展倍乘运算
    x2,y2=mul_add(x1, y1, da)
    # 根据密钥长度不同，将点坐标转换为二进制字符串
    if (len(hex(p)[2:]) * 4 == 192):
        x2, y2 = '{:0192b}'.format(x2), '{:0192b}'.format(y2)
    else:
        x2, y2 = '{:0256b}'.format(x2), '{:0256b}'.format(y2)
    # 计算密钥长度
    klen=len(c2)*4
    # 生成密钥流
    t=KDF(x2+y2, klen)
    # 如果生成的密钥流为0，说明解密失败
    if int(t,2)==0:
        return False
    # 进行异或运算得到明文消息m
    m='0'*(klen-len(bin(int(c2,16)^int(t,2))[2:]))+bin(int(c2,16)^int(t,2))[2:]
    # 计算验证值u，使用哈希函数对(x2+m+y2)进行哈希运算
    u=Hash(hex(int(x2+m+y2,2))[2:])
    # 如果验证值不匹配，说明解密失败
    if u!=c3:
        return False
    # 返回解密得到的明文消息m
    return hex(int(m,2))[2:]

start_time = time.perf_counter()
Pa=mul_add(Gx,Gy,da)
m="Liyupei"#加密消息"Liyupei"，得到密文c1、c2、c3
c1,c2,c3=encrypt(m)#解密密文，得到明文m2
m2=decrypt(c1,c2,c3)#将明文m2转换为字节流
m2=binascii.a2b_hex(m2)
end_time = time.perf_counter()
print('程序运行时间:', end_time - start_time, '秒')
print(m2)#输出解密得到的明文消息m2

