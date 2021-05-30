# 体系结构

- 用户态与内核态

- `内核`->`系统调用`->`shell、公共库函数（系统调用的组合）`->`应用程序`

# Linux文件的概念

> Linux一切皆文件（磁盘、进程）

- Bin，二进制文件
- Dev，存放外接设备，Linux需要自己挂载外接设备
- Etc，存放配置文件
- Home，表示除了root以外其它用户的家目录。
- Proc，表示进程
- Root，root用户的家目录
- Sbin，super存放可以执行的二进制文件，但是需要root权限。
- Tmp，存放临时文件
- Usr，存放用户自己安装的软件（类似于windows下的program files）
- Var，存放的程序或者系统日志文件的目录
- Mnt，外接设备挂载的地方
# Linux基础指令
- Linux指令格式：`#（或者$）指令主体 [选项][操作对象]`
- command --help显示帮助
- -h human-readable

---

## 关机
- 正常关机（推荐）：shutdown -h now
- 关闭内存：halt
- init 0（快过时）
## reboot

重新启动计算机

- reboot 重启计算机
- reboot -w 模拟重启，只写开关机日志

## shutdown

> 关机（慎用）

- shutdown -h now 立即关机
- shutdown -h 15:25 "提示信息（可选择）"定时关机

## uptime

输出计算机的在线时间（开机时间）

- uptime

## ls

- ls 列出当前工作目录下的所有文件和文件夹的名称
- ls path 列出指定路径下的所有文件和文件夹
- ls -l path，以详细列表的形式进行展示
- ls -la path，显示所有的文件与文件夹（包括隐藏文件）【all】
- 文件第一列表示类型，其中-表示该行对应的文档类型为文件，d表示该行对应的文档类型为文件夹。【directory】隐藏文件以.开头
- ls -lh path 列出指定路径下的文件与文件夹，文件大小以可读性较高的形式显示（1024进制形式）
- ls指令颜色解析：蓝色表示文件夹，黑色表示文件，绿色表示拥有所有权限。
## pwd

> print working directory，打印当前工作路径

## cd
- cd path 切换目录
- cd ~ 快速切换到当前用户的家目录

## mkdir

>  make directory，创建文件夹

- mkdir path
- mkdir -p一次性创建多个不存在的目录
- mkdir path1 path2 path3一次性创建多个目录

## touch

> 创建文件

- touch path

- touch命令不可以在不存在的目录下创建文件
## cp

> copy

- `cp sourcePath targetPath`

- cp命令可以在在targetPath改变文件名
- 当使用cp命令复制文件夹时，需要添加命令选项-r（recursion，递归），否则文件夹会被忽略。
## mv

> move

- `mv sourcePath targetPath`

- 同样mv命令可以在在targetPath改变文件名（mv也是Linux的重命名指令）
- mv移动文件夹时不用加-r
## rm

> remove

- `rm [option] path`

- 可以通过option中 -f 取消删除前的询问（force）
- `rm -r 删除文件夹`
- `rm -rf 强制删除文件夹`
- 批量删除文件名具有相同特性的文件，fileName*（通配符）
## 输出重定向
- `>` 覆盖输出
- `>>`追加输出
- 正常的指令 > or >> path/log.txt
## cat
>  直接打开一个文件（不像vim那样进入文件，即无需手动退出）

- `cat path`

- `cat source1 source2 sourcen > 或者 >> target` 配合输出重定向使用对文件进行合并
## df

> disk free，查看磁盘空间

- 常用格式 #df -h
- FileSystem 表示磁盘分区
- Mounted on 表示挂载点
## free
查看空余资源
- 常用格式：free -m（m展示的单位格式）
## head
查看文件的前几行，默认10行
- 常用格式 #head -n path
## tail
- 查看后几行 #tail -n path
- 动态查看文件的动态变化（内容不能是自己手动添加的，可以查看输出重定向的内容，一般用来查看日志） #tail -f path
## less
以较少内容的形式展示文件内容，按辅助键滚屏（数字+回车 跳转到指定行、空格 翻页、方向键换行）
## wc
（word count）统计文件内容信息（行数、单词数、字节数）
- 常用格式 #wc -lwc path
## date
>  操作时间与日期（读取与设置）

- date 显示当前时间（CST 当地时间）
- date +%F (等价于 #date "+%Y-%m-%d") 格式化年月日（yyyy-MM-dd） 
- date +%F%T(或者#date "+%F %T")等价于#date "+%Y-%m-%d %H:%M :%S" 输出年月日时分秒

- 获取过去的时间（备份时常用）# date -d "-1 day" 获取一天前的时间
- 获取未来的时间 #date -d "+1 day" 获取一天后的时间
- 单位可选值 day、month、year
## cal
> 输出当前月的日历

- cal -1（默认，输出当前月的日历）
- cal -3 输出当前月与前后月的日历
- cal -y year 输出指定年份的全部月份

## clear
- 清除终端中已经存在的指令（假的清屏，下拉屏幕，快捷键Ctrl+L）
## 管道

> 可将指令连接起来，前一个指令的输出作为后一个指令的输入。管道连接符一般不单独使用，必须配合其他指令搭配使用，主要起辅助作用

- 管道符连接符：`|`
- 管道只处理前一个命令的正确输出，链上任何一个命令发生异常都会导致整体异常，指令终止
- 右侧的命令需要能够接收标准输入流，否则传递过程中数据会被抛弃。常用的命令：`sed`、`awk`、`grep`、`cut`、`head`、`top`、`less`、`more`、`wc`、`join`、`sort`、`split`
- 过滤
- `指令 输入目录 | 操作 操作内容 `

- 如 #ls / | grep y
只显示含y的文件或目录
- 通过管道达成其它指令的效果

- 如 less指令，用管道实现：#cat path | less
- 拓展处理，如 统计文件数 #ls / | wc -l

## hostname
> 获取服务器的主机名（获取、临时设置（一般不在这里设置））

- hostname 输出完整的主机名
- hostname -f 输出当前主机名中的FQDN（全限定域名）
## id
查看一个用户的基本信息（用户id，用户组id，附加组id），如果不指定用户，则默认当前用户。
## whoami
显示当前登录的用户名，一般用于shell脚本
## ps 
> 查看服务器的进程信息

- e 相当于“A”，表示列出全部进程
- f 显示全部的列（全字段）
UID（用户ID）、PID（进程ID）、PPID（父进程ID，如果一个进程没有PPID，则这个进程是僵尸进程）、C（CPU占用率）、STIME（进程的启动时间）、TTY（终端发起，如果是问号则表示进程由系统发起）、CMD（进程对应的名称或者路径）
- 在ps结果中过滤出想要查看的进程信息ps -ef | grep name（查找过滤时会产生一个进程，故过滤结果至少有一个）
## grep

> global regular expression print，查找文件里面符合条件的行

- `grep [options] pattern file`
- options
  - `-o --only-matching : 只显示匹配PATTERN 部分`
  - `-v 或 --revert-match : 显示不包含匹配文本的所有行`

## top

> 查看服务器的进程占用资源（zombies僵尸）
> q退出
> M 将进程按内存使用降序排列
> P 将进程按照CPU使用降序排列
> 1 查看cpu每个核的使用情况，展开显示各个cpu的详细信息

- PID 进程id
- PR 优先级
- VIRT 虚拟内存
- SHR 共享内存
- RES 常驻内存
- 进程实际使用内存 = RES - SHR
## du 
查看目录的真实大小
- 语法 du -sh path
- -s 只显示汇总的大小（summary）
- -h 以较高可读性的形式进行显示
## find

> 在指定目录下查找指定文件

- `find path [options] params`
- path 默认在为当前目录，`/`全局搜索
- name 按照文件名，支持模糊查询 `file_name*`
- `iname` 忽略大小写 
- type 按照文件类型（f文件，d目录）
## service
用于控制软件的启动、停止、重启
- service 服务名 start/stop/restart
## kill
- $ kill PID
## killall
- $ killall 进程名称
## ifconfig
> 获取网卡地址（eth0 网络，lo 本地），已废弃

## ip addr

## uname
获取计算机操作系统相关信息
- $uname
- $uname -a 操作系统完整信息
## netstat
>  查看网络连接状态

- t 只列出tcp协议的连接
- n 将字母组合转化为ip地址，将协议转化为端口号
- l 表示过滤出 .state列中值为LISTEN的连接
- p 显示发起连接的进程PID和进程名称
## man
> manual 手册

## awk

> 无缩写，awk为三个创始人的名字。适合处理规格化数据

- `awk [options] 'bool pattern{cmd}' file`
- 一次读取一行文本，按输入分隔符进行切片，切成多个组成部分
- 切片直接保存在内建的变量之中，`$0`表示行的全部，`$1`表示第一个
- 支持对单个切片的判断，支持循环判断，默认分隔符为空格
- `NR`表示`awk`命令执行之后按照分隔符读取的数据次数，默认分隔符为换行符，所以`NR`默认等于数据行数
- `awk -F "," 'cmd' file`设置列分隔符

## sed

> stream editor，流编辑器，适合对文本内容行进行处理

- `sed [option] 'sed command' file`

- example

  ```
  sed command 's/修改前的内容reg/修改后的内容reg/'
  
  sed 's/^Str/String/' xxx.java # 将指定文件中Str替换为String
  
  # sed默认将结果显示在终端而不是修改文件，如果需要在源文件替换，需要加-i参数
  # 默认为替换第一个，///g全局替换
  # ///d 删除行
  ```

  

# 快捷键
- ctrl + u 清除光标前的内容
- ctrl + k 清除光标后的内容
# vim
## vim的三种模式（常用）
### vim打开方式
1. $ vim 文件路径
2. $ vim +数字 文件路径（打开文件并将光标移动到指定行）
3. $ vim +/ 关键字 文件路径（打开指定文件，并且高亮显示关键字）
### 命令模式
- 不能对文件进行操作，可以输入快捷键（删除行、复制行、移动光标、粘贴）
- 打开文件自动进入的模式

光标移动到行首

shift + 6 (^)

光标移动到行末

shift + 4 ($)

光标移动到首行 gg

光标移动到末行 G

翻屏

- 上 pg up 或者 ctrl + b （back）
- 下 pg dn 或者 ctrl + f （forward）

复制、粘贴

- 复制 yy（光标所在行）
- 张贴 p
- 向下复制多行（包括光标所在行） 行数 yy
- 可视化复制 ctrl + v 通过方向键控制选中区域，yy确定复制

剪切/删除

- dd 剪切或者删除光标所在行（严格意义上是剪切命令）
- 行数 dd 剪切、删除多行（空白自动补全）
- D 剪切、删除光标所在行，空白不补全

撤销 u 或者 :u (undo)

恢复 ctrl + r redo

光标快速移动 行数 G （移动到指定行）

行数 + 上下方向键 向上向下快速移动

行数 + 左右方向键

向左向右快速移动n字符
### 编辑模式
- 对文件文本进行编辑
### 末行模式
- 在末行输入命令。对文件进行操作（搜索、替换、保存、退出、撤销、高亮）
- :w 保存文件
- :w 路径 另存为
- :q 退出文件 
- :wq 保存并退出
- :q! 强制退出（不保存刚才的修改）
- :!命令 调用编辑器外部命令(当外部命令结束后按任意键回到vim编辑器打开的内容)
- / 查找（可以直接进入末行模式）查找并高亮显示
- 在搜索结果中切换上一个结果与下一个结果 N/n 
- :nohl no highlight 取消高亮
- :s/搜索关键词/新的内容 string replace 替换光标所在行的第一个匹配内容
- :s/搜索关键词/新的内容/g 替换光标所在行的全部匹配内容
- :%s/搜索关键词/新的内容 替换全文的每行首个匹配内容
- :%s/搜索关键词/新的内容/g 替换全文的全部匹配内容
- :set nu (number)显示行号
- :set no nu 取消显示行号
- :files 使用vim打开多个文件时，在末行模式下进行切换文件，查看当前已经打开的文件 %a当前打开的文件 #上一次打开的文件 
- : open fileName 打指定文件
- :bn 切换到下一个文件（back next）
- :bp 切换到上一个文件（back previous ）
### 常用功能
#### 代码着色
- 开启 :syntax on
- 关闭显示 :syntax off
#### 计算器的使用
当编辑文件时，使用计算器简单计算
- 编辑模式下 ctrl + R 输入=号，此时光标移动到最后一行，在此进行计算，输入回车键即可
### 模式间的切换
#### 命令模式到末行模式
- 输入 英文:
#### 末行模式回退到命令模式
- 按一下 esc 等待5秒后退出
- 按两下 esc 快速退出
- 删除命令直到删除:
#### 命令模式切换到编辑模式
- i 在光标所在的字符前面开始插入insert
- a 在光标所在的字符后面开始插入append
- o 在光标所在行的下面另起一行
- I 在光标所在行的行首开始插入
- A 在光标所在行的行尾开始插入
- O 在光标所在行的上面另起一行开始插入
- S 删除光标所在行并插入
#### 编辑模式回退到命令模式
- esc
### vim 配置
#### vim配置文件
- 文件打开时在末行模式下输入配置（临时）
- 个人配置文件 （~/.vimrc，如果没有则可以自行新建）
- 全局配置文件 vim自带，/etc/vimrc/
#### 配置项
个人配置文件优先级高于全局配置
### 异常退出
在编辑文件之后没有wq便退出
- 在交换文件删除即可
### 别名机制
alias cls 'clear' 一般在配置文件中配置
### 退出方式
- :x 在文件没有修改时，表示直接退出，但不会像:wq那样修改文件修改时间（:q）；在文件被修改的情况下表示保存并退出（:wq）。
# Linux自有服务
## 运行模式（级别）
### 7个运行级别
- 0 关机级别（不要这样设置）
- 1 单用户模式
- 2 多用户模式，不带NFS（默认）
- 3 多用户模式（完整的）
- 4 保留模式（未使用）
- 5 X11模式（完整的图形化界面）
- 6 reboot重启级别
#### 命令
- 切换到纯代码窗口 init 3
## 用户管理
/etc/passwd 用户的关键信息
用户名:密码（占位）:用户ID:注释:家目录:解析器 shell
/etc/group 用户组的关键信息
/etc/shadow 用户的密码信息
#### 用户管理
1. 添加用户 $useradd 选项 用户名
- g 表示指定用户的用户组（用户组的ID或者组名）
- G 表示指定用户的附加组
- u uid，用户的ID（系统默认从500之后按顺序分配uid）
- c 添加注释
- useradd 会自动创建同名的家目录和用户组
2. 修改用户 $usermod 选项 用户名
- g、G、u 同上
- I 修改用户名
3. 修改密码
passwd 用户名
su 用户名 切换用户
4. 删除用户
userdel
#### 用户组管理
实际上是对group的修改
1. 用户组添加 groupadd 选项
用户组名

2. 用户组编辑 groupmod 选项 用户组名
- g 表示选择自己设置一个自定义的用户组ID（默认由500后递增）
- n 类似于用户修改-I，表示设置新的用户组的名称
3. 用户组删除 groupdel 用户组名
当这个组是某个用户的主组时，需要把所有用户从组内移除
## 网络设置
1. 网卡配置文件位置
/etc/sysconfig/network-script
ifcfg-网卡名字
2. 配置项
- ONBOOT 是否开机启动
- BOOTPROTO ip地址分配，HDCP表示动态主机分配协议
- HWADDR MAC地址
3. 重启网卡
$ service network restart
4. 创建快捷方式
$ In -s 原文件路径 快捷方式路径
5. 停止指定网卡 ifdown 网卡名
6. 启动指定网卡 ifup 网卡名
## ssh服务
## 文件传输
- filezilla 可视化
- pscp 命令行
## 修改主机名
- hostname
- hostname -f FQDN 查看
1. hostname 要设置的主机名 （设置临时的主机名，不需要重启，但是需要切换主机名）
2. 修改 /etc/sysconfig/network 配置文件 永久修改主机名
3. 修改hosts文件，将新主机名指向Hosts文件的位置:/etc/hosts（本地DNS，设置FQDN）
## chkconfig服务
开机启动服务
- chkconfig --list 开机启动服务查询
- chkconfig --del serviceName 删除服务
- chkconfig --add serviceName 添加服务
- chkconfig --level level serviceName on/off 如 chkconfig --level 35 on
## ntp服务
ntp服务用于对时间的同步管理操作
- 时间上游服务器 `http://www.ntp.org.cn/pool.php`
- `ntpdate 时间服务器的域名或者IP地址`
- 启动时间同步服务
1. `service ntpd start` 或者 `/etc/init.d/ntpd/start`
2. `chkconfig --level 35 ntpd on`
## 防火墙设置
> centos 6.5 iptables，centos 7.x firewall

- iptables 启动 service iptables start/reset/stop/或者/etc/init.d/iptables start/stop/restart
- 查看状态 service iptables status
- iptables -L -n 查看规则
- 简单设置防火墙 iptables -A INPUT -p tcp --dport 80 -j ACCEPT
## rpm软件管理
- rpm -qa|grep key 查询某个软件的安装情况
- rpm -e 软件名 卸载软件
- rpm -e 软件名 --nodeps 强制卸载
- 软件安装
1. lsblk （list block devices 查看块状设备）
2. 挂载光盘 mount 设备原始地址（/dev/sr0，统一在/dev下） 挂载点（一般在/mnt下） 
3. 解挂 umount path（挂载点）
4. rpm -ivh 软件完整名称 安装软件
- i install
- v 进度条
- h 以#形式显示进度条
## cron（crontab）计划任务
1. crontab 选项 列出计划任务
- l list
- e edit
- u user
- r remove
2. 编辑任务
分 时 日 月 周 需要执行的命令（不需要的由*占位）
- \*表示取值范围内的任意数字，-做连续区间表达式，/表示每多少个（每十分钟一次，在分得位置表示*/10），,表示多个取值(1,2,6)

## 权限

  - 权限：读、写、执行

  - 身份：owner、group、others、root

  - ls -l path (等价于 ll path)查看文件即相关属性

  - drwxr-x
    - 第1位，表示文档类型：d，文件夹；-，文件；I，软连接、s，套接字
    - 第2位，读权限：r可读，-不可读
    - 第3位，写权限：w可写，-不可写
    - 第4位，执行权限：x可执行，-不可执行
    - 第5~7位，表示与所有者同在一个组的用户权限
    - 第8~10，除上面以外的其它用户的权限

  - 权限设置

      - 语法：chmod 选项 权限模式 文档（需要为root或者文件所有者）
      - 常用选项

          - -R 递归设置权限（当文档类型为文件夹时）
      - 字母形式
         - 给谁设置？
            - u owner
            - g group
            - o others 
            - a all 所有人，包含ugo（默认）
         - 作用？
            - +新增权限
            - -删除用户权限
            - =将权限设置成具体权限
         - 权限？
            - r
            - w
            - x
         - 例子 #chmod u+x，g+rx，o+r test.cfg
      - 数字形式
      - r 4，w 2，x 1
         - 0 --- 没有任何权限
         - 1 --x 可执行
         - 2 -w- 可写
         - 3 -wx 可写，可执行
         - 4 r-- 可读
         - 5 r-x 可读，可执行
         - 6 可读，可写
         - 7 拥有全部权限
      - 不要设置可写，可执行，不能读的权限（由于无法打开而不能进行修改，但是可以通过重定向追加）
      - 在Linux中，如果要删除文件，要看该文件所在的目录是否有写权限，如果有才可以删除。

      ### 属主与属组的设置

  - 属主，指的是所属的用户（文件的主人）

  - 属组，指的是所属的用户组

  - 这两个信息在文档创建时使用创建者的信息

  - chown 更改文档的所属用户

        - \#chown -R username path
        - \#chgrp -R groupname path
        - \#chown -R username:groupname path
## sudo

让管理员事先定义某些特殊命令可以由谁执行，配置文件：/etc/sudores

- 配置sudo文件需要使用 #visudo打开
- 语法 ： 用户名 运行的主机=（以谁的身份执行，ALL表示root） 当前用户可以执行的命令 
- 使用sudo命令时，需要书写命令的完整路径，完整路径可以使用 switch 命令 来查看
- test ALL=(ALL) /usr/sbin/useradd,/usr/bin/passwd/ ,!/usr/bin/passwd/root 加!表示不允许执行该命令
- \#sudo -l 普通用户查看自己拥有的权限
- 

## SHELL

- `cat /etc/shells` 查看shell种类
- `chsh - s xxx` 切换shell种类

### 规范

- 代码规范：\#!/bin/bash 指定当前系统当前这个脚本要使用的shell解析器

  shell 相关命令

- 命名规范：文件名.sh

- 流程：1.创建.sh文件；2.编写shell代码；3.执行shell脚本（必须有执行权限）
## 软件安装
> yum [-y] 表示默许任何询问，删除操作时不要使用该选项

```
1. yum list
2. yum search
3. yum [-y] install packName
4. yum [-y] update [packName] 不使用包名则更新全部软件
5. yum [-y] remove packName
```