from csm3 import SM3, Group, CF
import time

def len_ext_attack(message, extension, num_blocks):
    hash_orig = SM3(message)
    hash_msg = []
    for i in range(8):
        hash_msg.append(int(hash_orig[i * 8:i * 8 + 8], 16))
    
    total_length = hex((num_blocks + len(extension)) * 4)[2:]
    total_length = (16 - len(total_length)) * '0' + total_length
    
    extension = extension + '8'
    if len(extension) % 128 > 112:
        extension = extension + '0' * (128 - len(extension) % 128 + 112) + total_length
    else:
        extension = extension + '0' * (112 - len(extension) % 128) + total_length
    
    extension_group = Group(extension)
    num_groups = len(extension_group)
    
    V = [hash_msg]
    for i in range(num_groups):
        V.append(CF(V, extension_group, i))
    
    result = ''
    for x in V[num_groups]:
        result += hex(x)[2:]
    
    return result

start_time = time.time()
if __name__ == '__main__':
    orig_message = '123456'  # 原始消息
    extension = '123'  # 扩展部分
    
    if len(orig_message) % 128 < 112:
        num_blocks = (int(len(orig_message) / 128) + 1) * 128  # 16进制数个数
    else:
        num_blocks = (int(len(orig_message) / 128) + 2) * 128  # 16进制数个数
    
    len_message = hex(len(orig_message) * 4)[2:]
    len_message = (16 - len(len_message)) * '0' + len_message  # 消息长度
    
    padding = num_blocks - len(orig_message) - 16 - 1  # 补0个数=总长-消息-消息长度-1
    new_message = orig_message + '8' + padding * '0' + len_message + extension  # new_message = orig_message||1000...|| |orig_message| ||extension
    
    new_hash = SM3(new_message)
    attack_result = len_ext_attack(orig_message, extension, num_blocks)
    
    print("原始消息为：", orig_message)
    print("新消息的哈希值为:", new_hash)
    print("长度扩展攻击结果:", attack_result)
    
    if new_hash == attack_result:
        print("长度扩展攻击成功!")
    else:
        print("长度扩展攻击失败!")
end_time = time.time()
runtime = end_time - start_time
print("运行时间：", runtime, "秒")
