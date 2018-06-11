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

### oas归档存储 