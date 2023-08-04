#project13

##Implement the above ECMH scheme

###实验概述
实现集合上的哈希，生成椭圆曲线的公私钥对，实验思路是先把集合里的元素映射成椭圆曲线上的点，利用椭圆曲线上的加法求解哈希值，具体实现过程见ECMH.py文件

####实验运行指导
用Win+R打开cmd然后输入pip install gmssl安装好该库后，用python运行ECMH.py文件即可