# #project1:implement the naïve birthday attack of reduced SM3
  实现方式：
    用python运行
  实验原理以及大致思路：
    首先实现SM3算法，定义并实现多个函数：
    循环左移函数ROL，杂凑函数FF,杂凑函数GG，置换函数P0以及P1，确定常量T_j,消息填充函数Fill(使填充后的消息为512bit的整数倍，消息分组函数Group（将消息分成128bit每组），消息扩展函数Expand,压缩函数CF，迭代函数Iterate,SM3函数，
    最后根据SM3算法把这些函数拼接起来实现SM3，并输出对字符串“123456”的哈希值
    再实现生日攻击：定义一个birthday_attack函数，利用对于一定长度和哈希值结果2^32长度，在2^16的密文空间中可以有50%以上的概率找到一个生日攻击的原理，使用类似查表的数据结构，以空间换时间，在本实验中，以前14bit和前18bit为例，可在较短时间内实现生日攻击
  实现效果以及运行结果截图：
    SM3实现的效果图：
    ![image](https://github.com/kiwifruitlyp/HomeworkGroup85/assets/139031774/91158b88-b3f0-4ed6-89f1-496c69935bfc)

    生日攻击实现效果截图：
    ![image](https://github.com/kiwifruitlyp/HomeworkGroup85/assets/139031774/4e0d68d8-a010-4782-9b9e-ef38f0e3b735)

                         

# #project2:implement the Rho method of reduced SM3
  实现方式：用python运行
  实验原理以及大致思路：
  实现效果以及运行结果截图：
# #project3:implement length extension attack for SM3
  实现方式：用python运行
  实验原理以及大致思路：
  实现效果以及运行结果截图：
  # #project4:do your best to optimize SM3 implementation (software)
  实现方式：用python运行
  实验原理以及大致思路：
  实现效果以及运行结果截图：
  # #project5:Impl Merkle Tree following RFC6962
  实现方式：用python运行
  实验原理以及大致思路：
  实现效果以及运行结果截图：
  # #project8:Impl Merkle Tree following RFC6962
  实现方式：用python运行
  实验原理以及大致思路：
  实现效果以及运行结果截图：
  # #project9: AES software implementation
  实现方式：用python运行
  实验原理以及大致思路：
  实现效果以及运行结果截图：
  # #project10:report on the application of this deduce technique in Ethereum with ECDSA
  实现方式：用python运行
  实验原理以及大致思路：
  实现效果以及运行结果截图：
  # #project11:impl sm2 with RFC6979
  实现方式：用python运行
  实验原理以及大致思路：
  实现效果以及运行结果截图：
  # #project13:Implement the above ECMH scheme
  实现方式：用python运行
  实验原理以及大致思路：
  实现效果以及运行结果截图：
  # #project14:Implement a PGP scheme with SM2
  实现方式：用python运行
  实验原理以及大致思路：
  实现效果以及运行结果截图：
  # #project15:implement sm2 2P sign with real network communication
  实现方式：用python运行
  实验原理以及大致思路：
  实现效果以及运行结果截图：
  # #project16:implement sm2 2P decrypt with real network communication
  实现方式：用python运行
  实验原理以及大致思路：
  实现效果以及运行结果截图：
