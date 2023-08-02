import random
import time
from asm3 import SM3


def birthday_attack(exm):
    collision_dict = [-1] * 2 ** exm
    max_value = int(2 ** (exm / 2))#搜寻原像空间的大小
    
    for i in range(max_value):
        hash_value = int(SM3(str(i))[0:int(exm / 4)], 16)# 计算哈希值
        # 检查是否有碰撞
        if hash_value in collision_dict:
            return hash_value, i, collision_dict[hash_value]
        collision_dict[hash_value] = i# 将哈希值添加到字典中
    
    return None


start_time = time.time()
if __name__ == '__main__':
    bit_length = 18#将前*bit进行碰撞，实际可以找到更多碰撞
    collision = birthday_attack(bit_length)
    
    if collision:
        col, m1, m2 = collision
        print("找到碰撞，消息{}与{}哈希值的前{}bit相同，16进制表示为:{}。".format(m1, m2, bit_length, col))
    else:
        print("未找到碰撞。")
        
end_time = time.time()
runtime = end_time - start_time
print("运行时间：", runtime, "秒")
