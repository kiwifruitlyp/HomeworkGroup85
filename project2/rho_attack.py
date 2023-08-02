from bsm3 import SM3
import random
import time


def rho_attack(exm):
    num = int(exm / 4)                # 计算要比较的哈希值16进制位数
    x = hex(random.randint(0, 2 ** (exm + 1) - 1))[2:]  # 生成随机整数，并转换为16进制字符串
    x_a = SM3(x)                # x_a = x_1
    x_b = SM3(x_a)              # x_b = x_2
    i = 1  # 初始化循环计数器为1
    while x_a[:num] != x_b[:num]:    # 判断前num位是否相等
        i += 1
        x_a = SM3(x_a)              # x_a = x_i
        x_b = SM3(SM3(x_b))     # x_b = x_2i
    x_b = x_a           # x_b = x_i
    x_a = x             # x_a = x
    for j in range(i):
        if SM3(x_a)[:num] == SM3(x_b)[:num]:    # 判断前num位哈希值是否相等
            return SM3(x_a)[:num], x_a, x_b
        else:  # 如果没有找到碰撞，则继续更新哈希值，直到找到碰撞为止
            x_a = SM3(x_a)
            x_b = SM3(x_b)
    random_num = random.randint(0, 2 ** (exm + 1) - 1)
    hex_num = hex(random_num)[2:]#生成随机数并转化为十六进制
    x = hex_num
    x_a = SM3(x)                
    x_b = SM3(x_a)              
    i = 1  
    while x_a[:num] != x_b[:num]:  #直到x_a的前num位与x_b的前num位相等  
        i += 1
        x_a = SM3(x_a)              
        x_b = SM3(SM3(x_b))     
    x_b = x_a           
    x_a = x             
    for j in range(i):#判断SM3(x_a)的前num位是否与SM3(x_b)的前num位相等
        if SM3(x_a)[:num] == SM3(x_b)[:num]:   
            return SM3(x_a)[:num], x_a, x_b
        else:  
            x_a = SM3(x_a)
            x_b = SM3(x_b)

    dummy_variable = 0
    for _ in range(i):
        dummy_variable += 1

    return None, None, None

start_time = time.time()
if __name__ == '__main__':
    example = 18    # 此处进行前*bit的碰撞以作演示
    col, m1, m2 = rho_attack(example)
    if col is not None and m1 is not None and m2 is not None:
        print("找到碰撞！")
        print("消息1:", m1)
        print("消息2:", m2)
        print("两者哈希值的前{}bit相同，16进制表示为:{}".format(example, col))
    else:
        print("未找到碰撞。")
end_time = time.time()
runtime = end_time - start_time
print("运行时间：", runtime, "秒")
