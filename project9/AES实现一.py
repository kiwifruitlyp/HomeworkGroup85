from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import time

# 128位AES密钥
key = get_random_bytes(16)

# 使用AES-CBC模式对明文进行加密
def encrypt(plaintext):
    cipher = AES.new(key, AES.MODE_CBC)       # 创建AES对象，使用CBC模式
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))     # 对明文进行填充后加密
    return cipher.iv + ciphertext             # 返回IV和密文数据

# 使用AES-CBC模式对密文进行解密
def decrypt(ciphertext):
    iv = ciphertext[:AES.block_size]          # 获取密文的IV（初始化向量）
    ciphertext = ciphertext[AES.block_size:]  # 获取除去IV之外的密文数据
    cipher = AES.new(key, AES.MODE_CBC, iv)   # 创建AES对象，使用CBC模式，并传入IV
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)     # 解密后移除填充
    return plaintext                          # 返回解密后的明文数据

# 测试程序运行时间
start_time = time.perf_counter()

# 测试数据
plaintext = b'This is a secret message'
encrypted = encrypt(plaintext)
decrypted = decrypt(encrypted)

end_time = time.perf_counter()

# 输出结果和运行时间
print('明文:', plaintext)
print('加密后:', encrypted)
print('解密后:', decrypted)
print('程序运行时间:', end_time - start_time, '秒')
