# #project1:implement the naïve birthday attack of reduced SM3
  #实现方式：
  
    用python运行
 
  #实验原理以及大致思路：
    
    首先实现SM3算法，定义并实现多个函数：
    
    循环左移函数ROL，杂凑函数FF,杂凑函数GG，置换函数P0以及P1，确定常量T_j,消息填充函数Fill(使填充后的消息为512bit的整数倍，消息分组函数Group（将消息分成128bit每组），消息扩展函数Expand,压缩函数CF，迭代函数Iterate,SM3函数，
    
    最后根据SM3算法把这些函数拼接起来实现SM3，并输出对字符串“123456”的哈希值
    
    再实现生日攻击：定义一个birthday_attack函数，利用对于一定长度和哈希值结果2^32长度，在2^16的密文空间中可以有50%以上的概率找到一个生日攻击的原理，使用类似查表的数据结构，以空间换时间，在本实验中，以前14bit和前18bit为例，可在较短时间内实现生日攻击
 
  #实现效果以及运行结果截图：
    
    SM3实现的效果图：
    ![image](https://github.com/kiwifruitlyp/HomeworkGroup85/assets/139031774/91158b88-b3f0-4ed6-89f1-496c69935bfc)
    生日攻击实现效果截图：
  ![image](https://github.com/kiwifruitlyp/HomeworkGroup85/assets/139031774/45ef0ced-0469-4a43-ae3a-6db5c5751325)


# #project2:implement the Rho method of reduced SM3
  实现方式：用python运行
  
  实验原理以及大致思路：
  
  SM3算法的实现与project1相同，定义一个rho_attack函数，参数exm表示要比较的哈希值的16位进制位数，函数内部调用SM3函数哈希算法计算哈希值，生成随机数，并进行比较，直到找到碰撞为止。在实现过程中要注意生成的随机整数要将其转换成16进制字符串，调用SM3计算其哈希值，再通过循环比较前num位的哈希值，在本实验中，要比较的哈希值位数为14和18，若找到碰撞，就打印出碰撞信息否则输出提示
  
  实现效果以及运行结果截图：
  ![image](https://github.com/kiwifruitlyp/HomeworkGroup85/assets/139031774/88eef8be-d0e8-40fb-a662-bbbe7592f921)

# #project3:implement length extension attack for SM3
  实现方式：用python运行
 
  实验原理以及大致思路：
  
  主要思路是利用SM3哈希算法的特性，通过构造恶意扩展部分，生成与原始消息具有相同哈希值的伪造消息。具体步骤首先使用SM3哈希算法计算原始消息的哈希值hash_orig，然后将其转换成整型分成8个32位整数存储在hash_msg列表中，计算扩展部分的总长度total_length，并转换成16进制字符串。长度计算公式为(num_blocks + len(extension)) * 4，其中num_blocks表示消息块数，每个块128位，len(extension)为扩展部分长度，添加'8'作为分割符，判断extension的长度是否满足128位对齐的要求，之后将将extension按每个128位为一组进行分组，初始化V列表，将hash_msg作为第一个元素加入V，循环计算num_groups次，每次调用CF函数生成下一个V值，并将其加入V，将V[num_groups]中的数值转换成16进制字符串，并拼接在一起得到result作为返回结果。最后主函数给定了原始消息orig_message和扩展部分extension的值，根据消息长度计算出num_blocks，然后构造新的消息new_message并计算其哈希值new_hash，调用len_ext_attack函数进行长度扩展攻击，将原始消息、扩展部分和num_blocks作为参数传入，得到的结果为attack_result。
  
  实现效果以及运行结果截图：
  ![image](https://github.com/kiwifruitlyp/HomeworkGroup85/assets/139031774/eb37748e-60d9-49b4-ae29-c2c6f2bcce4f)

  # #project4:do your best to optimize SM3 implementation (software)
  实现方式：用python运行
  
  实验原理以及大致思路：
 
  SM3算法的一般实现与project1和project2相同，SM3的优化可以从以下几个方面进行优化：利用多线程并行计算、利用更高效的数据结构或者算法来减少内存占用和数据传输量、利用优化循环结构减少循环次数或者合并循环、使用查表法位运算、或者使用循环展开指令集优化等等方法优化SM3，本实验从循环展开进行优化SM3算法，通过展开循环减少循环控制的开销，从而提高代码的运行效率。（之前尝试过用并行计算的方式进行优化，但是结果总是报错，总是出现多线程同时对一个资源进行访问产生死锁问题）

附上多线程报错截图：
![04CC5D655603443D57C752EC55F35F24](https://github.com/kiwifruitlyp/HomeworkGroup85/assets/139031774/9df03398-593e-4475-b4c4-982b7a5033e0)

![image](https://github.com/kiwifruitlyp/HomeworkGroup85/assets/139031774/c08a6ef9-aade-4cbc-812a-648e1b95a3c6)
![0C7792F63C01BF9368F1FA191E4B5C3F](https://github.com/kiwifruitlyp/HomeworkGroup85/assets/139031774/f3def92d-63bb-4ff0-bedb-e80506751694)



  

  结果分析，从实验运行结果分析，可以发现循环展开优化后SM3的优化反而降低了，经过查找资料分析，可能是如下原因导致的：对于循环体较小的情况，循环展开可能导致代码变得更大，在缓存中放不下全部代码，从而影响了缓存的局部性和访问效率；循环展开可能导致分支预测的准确率下降。循环中的判断条件可能被展开后的代码分散到不同的地方，增加了分支的数量，使得分支预测的准确率下降，从而影响了代码的执行效率；循环展开可能导致指令缓存的限制。指令缓存通常有一个固定的大小限制，展开循环后的代码可能超过了指令缓存的容量，从而导致指令缓存的命中率下降，进而影响了代码的执行效率……
  
  实现效果以及运行结果截图：
 ![image](https://github.com/kiwifruitlyp/HomeworkGroup85/assets/139031774/d68daadf-89ef-49ce-afd2-bd8d229cc735)



  # #project5:Impl Merkle Tree following RFC6962
  
  实现方式：用python运行
  
  实验原理以及大致思路：

   主要是实现Merkle树的构建和哈希计算功能，首先定义一个函数calculate_hash调用SHA-256算法计算数据的哈希值，build_merkle_tree函数接收一个叶子节点列表，对列表中的叶子节点进行哈希计算和构建Merkle树的操作；对于不同长度的叶子节点数量进行不同的返回处理，详情见代码；对于每一对叶子节点，将左节点计算哈希值，并判断是否存在右节点。如果存在右节点，则计算右节点的哈希值；否则，将右节点的哈希值设为与左节点相同。然后，将左节点和右节点的哈希值进行合并，计算它们的父节点的哈希值。最后，通过递归调用`build_merkle_tree`函数，传入新生成的节点列表来构建更高一层的Merkle树，直到最终生成根节点。
  
  实现效果以及运行结果截图：
  
![image](https://github.com/kiwifruitlyp/HomeworkGroup85/assets/139031774/6101c549-3ca6-4acc-b637-a1edf140402f)


  
  # #project8:AES impl with ARM instruction
  实现方式：用python运行
  
  实验原理以及大致思路：
  
  AES算法是基于矩阵运算的对称加密算法，包括字节替代、行移位、列混淆和轮密钥加四个阶段，其中字节替代可以使用查找表方式实现，行移位可以使用循环左移指令，大体思路就是分别实现AES算法中的每一个组成部分，可大致分为SubBytes()、ShiftRows()、MixColumns和AddRoundKey子函数再加上密钥扩展函数，最后进行拼接即可
 
  实现效果以及运行结果截图：
  
  由于代码还未完善，无法进行运行
  
# #project9: AES software implementation

  实现方式：用python运行

  实验原理以及大致思路：

  AES算法主要包括明文分组、密钥扩展、轮变换（包含四个操作SubBytes、ShiftRows、MixColumns 和 AddRoundKey），只需要分开实现这几部分的函数，进而完成这些功能，再根据算法流程进行拼接即可，这部分在密码学引论实验中已经做过，不再过多解释

  实现效果以及运行结果截图：
![image](https://github.com/kiwifruitlyp/HomeworkGroup85/assets/139031774/0b474fd2-5265-48c4-a882-9c23ddeb70d5)
![image](https://github.com/kiwifruitlyp/HomeworkGroup85/assets/139031774/f8b3d0be-64db-469a-9a3d-3089e3269983)



  # #project10:report on the application of this deduce technique in Ethereum with ECDSA

  实现方式：用python运行

  实验原理以及大致思路：

  利用相关数论知识主要是椭圆曲线相关知识实现ECDSA签名过程、公钥恢复，首先实现判断是否为二次剩余的函数boolQR（）；n在模p下的平方根函数solveQR（）； B 在模 N 下的乘法逆元函数mod_invese（）；求解 b 在模 n 下的乘法逆元，并计算最大公约数为 1 时的结果xgcd()实现这些基本函数再实现椭圆上的点加法add()，epoint_add1()；椭圆上的点乘multi()；密钥生成函数keygen()生成一对公私密钥，其中，私钥(sk)是一个随机生成的整数，公钥(pk)是将私钥乘以基点(G)得到的点；生成消息的签名函数signature()【先计算消息的哈希值(e)，生成一个随机数(k)作为签名中的一个参数，并计算(kG)得到签名中的一个点。接下来，计算签名中的两个值：r = (x坐标)%p，s = (k^(-1))(e + r*sk) % n。最终，返回签名值(r, s)】；最后定义一个密钥推导函数deduce（），【先从签名中获取签名点的x坐标(x)，并根据x坐标计算出两个可能的y坐标。然后，根据消息的哈希值(e)计算出临时点(tmp)。接下来，使用签名中的值(s)和推导出的临时点(tmp)计算得到两个可能的私钥(sk1, sk2)。最后，将每个私钥与推导出的临时点(tmp)相加，并使用签名中的值计算得到两个可能的公钥(pk1, pk2)】
  
实现效果以及运行结果截图：
![image](https://github.com/kiwifruitlyp/HomeworkGroup85/assets/139031774/9c0078ff-403c-49b7-aa9b-95f8a86ea98d)


  # #project11:impl sm2 with RFC6979
  
实现方式：用python运行
  
实验原理以及大致思路：
  
实现效果以及运行结果截图：
![image](https://github.com/kiwifruitlyp/HomeworkGroup85/assets/139031774/abb5d02f-38ee-49cb-a11b-2bbebf114990)
![image](https://github.com/kiwifruitlyp/HomeworkGroup85/assets/139031774/84fec7a2-9067-4cd6-8858-04de88f8d1f1)
![image](https://github.com/kiwifruitlyp/HomeworkGroup85/assets/139031774/a34d8411-fb39-4ee4-a6e6-541300d88b95)




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
