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


  

  结果分析，从实验运行结果分析，可以发现循环展开优化后SM3的优化反而降低了，经过查找资料分析，可能是如下原因导致的：对于循环体较小的情况，循环展开可能导致代码变得更大，在缓存中放不下全部代码，从而影响了缓存的局部性和访问效率；循环展开可能导致分支预测的准确率下降。循环中的判断条件可能被展开后的代码分散到不同的地方，增加了分支的数量，使得分支预测的准确率下降，从而影响了代码的执行效率；循环展开可能导致指令缓存的限制。指令缓存通常有一个固定的大小限制，展开循环后的代码可能超过了指令缓存的容量，从而导致指令缓存的命中率下降，进而影响了代码的执行效率……
  
  实现效果以及运行结果截图：
 ![image](https://github.com/kiwifruitlyp/HomeworkGroup85/assets/139031774/d68daadf-89ef-49ce-afd2-bd8d229cc735)



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
