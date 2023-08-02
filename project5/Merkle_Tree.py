import hashlib
#import time
import timeit

def calculate_hash(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.digest()

def build_merkle_tree(leaves):
    leaves = [str(leaf).encode('utf-8') for leaf in leaves]

    if len(leaves) == 0:
        return None

    if len(leaves) == 1:
        return {
            'hash': calculate_hash(leaves[0]),
            'left': None,
            'right': None
        }

    nodes = []
    for i in range(0, len(leaves), 2):
        left_hash = calculate_hash(leaves[i])

        if i + 1 < len(leaves):
            right_hash = calculate_hash(leaves[i + 1])
        else:
            right_hash = left_hash

        nodes.append({
            'hash': calculate_hash(left_hash + right_hash),
            'left': {
                'hash': left_hash,
                'left': None,
                'right': None
            },
            'right': {
                'hash': right_hash,
                'left': None,
                'right': None
            }
        })

    return build_merkle_tree(nodes)

# 示例用法
leaves = [
    'leaf1',
    'leaf2',
    'leaf3',
    'leaf4'
]
#start_time = time.time()
merkle_tree = build_merkle_tree(leaves)
def test_code():
    merkle_tree = build_merkle_tree(leaves)

#end_time = time.time()
#run_time = end_time - start_time
print(merkle_tree)
# 测试代码执行时间，并重复执行多次取平均值
time_taken = timeit.timeit(test_code, number=1000)

print("平均执行时间：", time_taken, "秒")
#print("运行时间：", run_time, "秒")
