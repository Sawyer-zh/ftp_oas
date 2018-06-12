# ftp_oas
使用ubuntu作为服务器
<br>
### ftp客户端和服务端安装
#### ftp 客户端
 * 安装:apt-get install ftp
 * 连接:ftp 127.0.0.1 输入用户名密码 成功
 * 上传:put xxx [xxxname]
 * 下载:get xxx [xxxname]

#### ftp 服务端
 * 安装:apt-get install vsftpd
 * 新建用户: useradd -d /home/ftp_user -g ftp
 * 配置:
     * anonymous_enable=NO  不允许匿名登录,允许的话不会弹出登录框,访问的目录为/srv/ftp
     * #anon_upload_enable=YES 注释掉了
     * pam_service_name=ftp 最开始是vsftpd 然后一直登不上去.网上有人说ubuntu系统需要改成ftp,成功 
 * 其他:登录之后进入各自用户的家目录
<br>

#### 需求分析
各个部门只能访问修改各自的目录
管理员可以修改和访问所有的文件
<br>

#### 思路和一些linux 操作
 * 对各个部门新建用户和组,并设置家目录及访问权限,家目录为管理员目录的子目录 
 * 建立管理员账户和组,把他加到各个部门的分组里面
 * 涉及的一些命令
     * useradd / adduser
     * passwd
     * chown
     * chgrp
     * chmod
     * groupadd

<br>

### oas归档存储 