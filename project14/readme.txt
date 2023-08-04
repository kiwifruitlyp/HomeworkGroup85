#project14

##Implement a PGP scheme with SM2

###实验概述
PGP是个混合加密算法，它由一个对称加密算法、一个非对称加密算法、与单向散列算法以及一个随机数产生器（从用户击键频率产生伪随机数序列的种子）组成，实现一个简易PGP，调用GMSSL库中封装好的SM2/SM4加解密函数；加密时使用对称加密算法AES加密消息，非对称加密算法SM2加密会话密钥；解密时先使用SM2解密求得会话密钥，再通过AES和会话密钥求解原消息

####实验运行指导
用Win+R打开cmd然后输入pip install gmssl安装好该库后，用python分别运行PGP.py文件和PGP_RSA.py文件即可，其中要保证ECMH.py文件与他们在同一个目录中