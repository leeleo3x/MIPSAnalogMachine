#汇编器反汇编器模拟机的设计

[English Version](README.md)

####李奥 3130001009 hi@leeleo.me

##汇编器

###使用方法

    python3 encoder.py input [output]

###算法简介

- 将汇编文件分行读入
- 替换每行的非必要字符
- 将每条指令分词存储
- 使用正则表达式提取必要信息
- 与存储的关键字进行匹配并转换为汇编码
- 将汇编码转换为二进制输出到文件中

##反汇编器

###使用方法

    python3 decoder.py input [output]

###算法简介

- 将二进制文件读入
- 将每32bit转换为一个Int类型
- 将32bit进行处理并转换为汇编指令
- format汇编指令
- 将汇编指令输出到文件中

##模拟机

- 模拟机仿照debug的工作模式
- 读入二进制文件到内存中
- 模拟执行汇编代码

- 基本命令

    - file file_name - 读入二进制文件的指令
    - n - 执行一条指令
    - p [pos] - 输出pos寄存器的内容，如果没有提供pos则输出所有寄存器的内容
    - m pos - 输出pos内存的内容
    - s - 输出当前pc指针的地址

- 本模拟机考虑了delay slot 所以建议在有delay slot的命令后插入noop指令
