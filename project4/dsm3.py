# SM3算法实现
import time
#循环左移函数
def ROL(X, i):
    i = i % 32
    return ((X << i) & 0xFFFFFFFF) | ((X & 0xFFFFFFFF) >> (32 - i))

#杂凑函数FF
def FF(X, Y, Z, j):
    if j >= 0 and j <= 15:
        return X ^ Y ^ Z
    else:
        return ((X & Y) | (X & Z) | (Y & Z))

#杂凑函数GG
def GG(X, Y, Z, j):
    if j >= 0 and j <= 15:
        return X ^ Y ^ Z
    else:
        return ((X & Y) | (~X & Z))
#置换函数
#布尔函数P0
def P0(X):
    return X ^ ROL(X, 9) ^ ROL(X, 17)

#布尔函数P1
def P1(X):
    return X ^ ROL(X, 15) ^ ROL(X, 23)

T = [0x79cc4519, 0x7a879d8a]
#确定常量T_j
def T_(j):
    if j >= 0 and j <= 15:
        return T[0]
    else:
        return T[1]

#消息填充，使填充后的消息为512bit的整数倍
def Fill(message):
    m = bin(int(message, 16))[2:] # 将输入的十六进制字符串转换为二进制字符串
    if len(m) != len(message) * 4:
        m = '0' * (len(message) * 4 - len(m)) + m# 在字符串前面填充0
    l = len(m)
    l_bin = '0' * (64 - len(bin(l)[2:])) + bin(l)[2:] # 将消息的二进制表示的长度转换为64位二进制字符串
    m = m + '1'
    if len(m) % 512 > 448:
        m = m + '0' * (512 - len(m) % 512 + 448) + l_bin
    else:
        m = m + '0' * (448 - len(m) % 512) + l_bin
    m = hex(int(m, 2))[2:]# 将填充后的二进制字符串转换为十六进制字符串
    return m

#将消息分组
def Group(m):
    n = len(m) // 128
    M = []
    for i in range(n):
        M.append(m[0 + 128 * i:128 + 128 * i])
    return M

#将消息扩展
def Expand(M, n):
    W = []
    W_ = []
    for j in range(16):
        W.append(int(M[n][0 + 8 * j:8 + 8 * j], 16))# 将每个分组的子消息转换为32位整数
    for j in range(16, 68):
        W.append(P1(W[j - 16] ^ W[j - 9] ^ ROL(W[j - 3], 15)) ^ ROL(W[j - 13], 7) ^ W[j - 6])#高位运算和布尔混合运算
    for j in range(64):
        W_.append(W[j] ^ W[j + 4])#线性变换
    Wstr = ''
    W_str = ''
    for x in W:
        Wstr += (hex(x)[2:] + ' ')
    for x in W_:
        W_str += (hex(x)[2:] + ' ')
    return W, W_

#压缩函数
def CF(V, M, i):
    A, B, C, D, E, F, G, H = V[i] # 将迭代变量V[i]的值分解为8个32位变量
    W, W_ = Expand(M, i) # 扩展消息分组M[i]为W和W_
    for j in range(64):
        SS1 = ROL((ROL(A, 12) + E + ROL(T_(j), j % 32)) % (2 ** 32), 7)
        SS2 = SS1 ^ ROL(A, 12)
        TT1 = (FF(A, B, C, j) + D + SS2 + W_[j]) % (2 ** 32)
        TT2 = (GG(E, F, G, j) + H + SS1 + W[j]) % (2 ** 32)
        D = C
        C = ROL(B, 9)
        B = A
        A = TT1
        H = G
        G = ROL(F, 19)
        F = E
        E = P0(TT2)
    a, b, c, d, e, f, g, h = V[i]
    V_ = [a ^ A, b ^ B, c ^ C, d ^ D, e ^ E, f ^ F, g ^ G, h ^ H]#计算新的V[i]
    return V_
#定义初始化向量IV
IV = [0x7380166F, 0x4914B2B9, 0x172442D7, 0xDA8A0600, 0xA96F30BC, 0x163138AA, 0xE38DEE4D, 0xB0FB0E4E]

#迭代函数
def Iterate(M):
    n = len(M)#消息分组的数量
    V = []
    V.append(IV)#初始化迭代变量V
    for i in range(n):
        V.append(CF(V, M, i))#进行循环压缩迭代
    return V[n]


def SM3(message):
    m = Fill(message)  # 填充后消息
    M = Group(m)  # 消息分组
    Vn = Iterate(M)  # 迭代计算
    res = ''
    for x in Vn:
            res += hex(x)[2:].zfill(8)#将结果转化为十六进制字符串
    return res

start_time = time.perf_counter()
if __name__ == '__main__':
    end_time = time.perf_counter()
    SM3('123456')
    execution_time = end_time - start_time
    print("Execution Time:", execution_time)
    #print('对123456的哈希结果为',SM3('123456'))#对该消息进行哈希

    
