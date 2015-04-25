---
layout: post
title:  搭建邮件服务器
category: coding
description: Postfix+Dovecot+MySQL+Extmail虚拟用户邮件系统
---

搜索了网上很多教程，经过多次失败，终于整理出 CentOS 6.x 64 bit 系统的 postfix + extmail+mysql 邮件系统搭建文档。

安装环境：

*  操作系统---CentOS 6.5 64bit
*  邮件传输代理(MTA)---Postfix 2.6.2
*  WebMail 系统---Extmail 1.1.0
*  Web 账户管理后台---Extman 1.0.0
*  邮件投递代理(MDA)---maildrop 2.0.4
*  其它数据认证库---courier-authlib 0.62.2
*  SMTP 认证库---cyrus-sasl 2.1.22
*  POP3 认证库---courier-imap 4.5.0

##  安装准备

### DNS配置

虽然不加DNS解析也能把邮件发出去，但会被大多数邮件服务器当作垃圾邮件。根据我们的实际经验，需要添加三条DNS解析记录：A记录、MX记录、TXT记录。比如域名example.com，对应的DNS记录如下： 

<table border="1" align="center" cellpadding="10">
    <tr>
        <th>主机记录</th>
        <th>记录类型</th>
        <th>记录值</th>
        <th>MX优先级</th>
    </tr>
    <tr>
        <td>mail</td>
        <td>A</td>
        <td>xx.xx.xx.xx</td>
        <td>--</td>
    </tr>
    <tr>
        <td>@</td>
        <td>MX</td>
        <td>mail.example.com</td>
        <td>10</td>
    </tr>
    <tr>
        <td>@</td>
        <td>TXT</td>
        <td>v=spf1 mx -all</td>
        <td>--</td>
    </tr>
</table>

###  Mysql-Server安装

{% highlight Bash shell scripts %}
yum install mysql-server
{% endhighlight %}

###  关闭防火墙

{% highlight Bash shell scripts %}
service iptables stop #关闭防火墙

chkconfig iptable off #关闭开机自启动
{% endhighlight %}

###  关闭SELinux

修改/etc/selinux/config文件中设置SELINUX=disabled ，然后重启服务器。

###  删除系统自带的Sendmail

{% highlight Bash shell scripts %}
yum -y remove sendmail
{% endhighlight %}

###  添加EMOS1.6的YUM源

一开始是想使用EMOS1.5的，发现有一些版本上的问题竟然不兼容(╯‵□′)╯︵┻━┻，又因为EMOS1.6没有在线源，只好自己搭本地的了TAT

EMOS1.6源iso镜像[下载][] #MD5 988f899703a17487cba66bf3c35f194e

{% highlight Bash shell scripts %}
mkdir /var/EMOS-repo #为iso镜像建立挂载点

mount -o loop -t iso9660 ~/EMOS_1.6_x86_64.iso /var/EMOS-repo #挂载

vi /etc/yum.repos.d/EMOS.repo

    # EMOS.repo
    #
    # Created by ExtMail Dev Team: http://www.extmail.org/
    #
    # $Id$
    [EMOS]
    name=EMOS
    baseurl=file:///var/EMOS-repo/
    gpgcheck=0
    priority=0
    protect=0

yum clean all #清除yum记录
{% endhighlight %}

现在我们就建好本地的EMOS源了~准备工作到此结束~

## 安装邮件系统

###  安装MTA-Postfix

{% highlight Bash shell scripts %}
yum install postfix

postconf -n > /etc/postfix/main2.cf

mv /etc/postfix/main.cf /etc/postfix/main.cf.bak

mv /etc/postfix/main2.cf /etc/postfix/main.cf

vi /etc/postfix/main.cf
    
    # hostname
    mynetworks = 127.0.0.1
    myhostname = mail.example.com #这里替换为你的域名
    mydestination = $mynetworks $myhostname
    # banner
    mail_name = Postfix - by extmail.org
    smtpd_banner = $myhostname ESMTP $mail_name
    # response immediately
    smtpd_error_sleep_time = 0s
    # Message and return code control
    message_size_limit = 5242880
    mailbox_size_limit = 5242880
    show_user_unknown_table_name = no
    # Queue lifetime control
    bounce_queue_lifetime = 1d
    maximal_queue_lifetime = 1d
{% endhighlight %}

###  配置 courier-authlib

{% highlight Bash shell scripts %}
yum install courier-authlib courier-authlib-mysql

# 修改配置文件
rm -f /etc/authlib/authmysqlrc

vi /etc/authlib/authmysqlrc

    MYSQL_SERVER            localhost
    MYSQL_USERNAME          extmail
    MYSQL_PASSWORD          extmail
    MYSQL_SOCKET            /var/lib/mysql/mysql.sock
    MYSQL_PORT              3306
    MYSQL_OPT               0
    MYSQL_DATABASE          extmail
    MYSQL_USER_TABLE        mailbox
    MYSQL_CRYPT_PWFIELD     password
    MYSQL_UID_FIELD         uidnumber
    MYSQL_GID_FIELD         gidnumber
    MYSQL_LOGIN_FIELD       username
    MYSQL_HOME_FIELD        homedir
    MYSQL_NAME_FIELD        name
    MYSQL_MAILDIR_FIELD     maildir
    MYSQL_QUOTA_FIELD       quota
    MYSQL_SELECT_CLAUSE     SELECT * FROM mailbox WHERE username = '$(local_part)@$(domain)'

# 修改 authmysqlrc 的权限和拥有者
chown daemon.daemon /etc/authlib/authmysqlrc

chmod 660 /etc/authlib/authmysqlrc

# 修改 authdaemonrc 以下内容
vi /etc/authlib/authdaemonrc

    authmodulelist="authmysql"
    authmodulelistorig="authmysql"

# 启动
service courier-authlib start

# 修改authdaemon socket 目录权限
chmod 755 /var/spool/authdaemon/
{% endhighlight %}

###  配置 maildrop

{% highlight Bash shell scripts %}
yum install maildrop

# 配置 master.cf 注释掉原来的maildrop的配置内容，并改为下面内容
vi /etc/postfix/master.cf

    maildrop unix - n n - - pipe
    flags=DRhu user=vuser argv=maildrop -w 90 -d ${user}@${nexthop} ${recipient} ${user} ${extension} {nexthop}

# 配置 main.cf 由于maildrop不支持一次多个收件人，所以添加下面参数
vi /etc/postfix/main.cf

    maildrop_destination_recipient_limit = 1

# 测试maildrop对authlib的支持
maildrop -v
{% endhighlight %}

###  配置Nginx

暂无内容= =

###  配置Extmail&Extman

{% highlight Bash shell scripts %}
yum install extsuite-webmail extsuite-webman

cp /var/www/extsuite/extmail/webmail.cf.default /var/www/extsuite/extmail/webmail.cf

vi /var/www/extsuite/extmail/webmail.cf

    SYS_MYSQL_USER = extmail
    SYS_MYSQL_PASS = extmail

# 更新cgi目录权限 由于SuEXEC的需要，必须将cgi目录修改成vuser:vgroup权限
chown -R vuser:vgroup /var/www/extsuite/extmail/cgi/

chown -R vuser:vgroup /var/www/extsuite/extman/cgi/

# 链接基本库到Extmail
mkdir /tmp/extman

chown -R vuser:vgroup /tmp/extman/
{% endhighlight %}

###  初始化数据库

{% highlight Bash shell scripts %}
service mysqld start

chkconfig mysqld on

# 导入数据且初始化（默认的mysql都没有密码的，所以以下命令都不需要认证密码）
vi /var/www/extsuite/extman/docs/init.sql
# 把里面所有 extmail.org 的改为 你的域名

mysql < /var/www/extsuite/extman/docs/extmail.sql

mysql < /var/www/extsuite/extman/docs/init.sql

cp /var/www/extsuite/extman/docs/mysql_virtual_alias_maps.cf /etc/postfix/

cp /var/www/extsuite/extman/docs/mysql_virtual_domains_maps.cf /etc/postfix/

cp /var/www/extsuite/extman/docs/mysql_virtual_mailbox_maps.cf /etc/postfix/

cp /var/www/extsuite/extman/docs/mysql_virtual_sender_maps.cf /etc/postfix/

vi /etc/postfix/main.cf

    # extmail config here
    virtual_alias_maps = mysql:/etc/postfix/mysql_virtual_alias_maps.cf
    virtual_mailbox_domains = mysql:/etc/postfix/mysql_virtual_domains_maps.cf
    virtual_mailbox_maps = mysql:/etc/postfix/mysql_virtual_mailbox_maps.cf
    virtual_transport = maildrop:

service postfix restart

# 测试authlib登录，example.com改为你的域名
/usr/sbin/authtest -s login postmaster@example.com extmail

# 配置图形化日志
/usr/local/mailgraph_ext/mailgraph-init start

# 启动cmdserver
/var/www/extsuite/extman/daemon/cmdserver --daemon

# 加入开机自启动
echo "/usr/local/mailgraph_ext/mailgraph-init start" >> /etc/rc.d/rc.local
echo "/var/www/extsuite/extman/daemon/cmdserver -v -d" >> /etc/rc.d/rc.local
{% endhighlight %}

注:

* Extmail url: http://mail.example.com/extmail
* Extman url: http://mail.example.com/extman
* Extman 管理员用户名：root@mail.example.com
* 管理员默认密码： extmail*123*
* Extmail 登录时，域名项应改为 mail.example.com

###  配置cyrus-sasl

{% highlight Bash shell scripts %}
# 删除系统自带的cyrus-sasl
rpm -e --nodeps cyrus-sasl

# 如果以上卸载有问题，请用以下卸载方式：
rpm -qa | grep cyrus-sasl | xargs rpm -e --allmatches --nodeps

yum install cyrus-sasl*

vi /etc/postfix/main.cf

    # smtpd related config
    smtpd_recipient_restrictions = permit_mynetworks, permit_sasl_authenticated, reject_non_fqdn_hostname, reject_non_fqdn_sender, reject_non_fqdn_recipient, reject_unauth_destination, reject_unauth_pipelining, reject_invalid_hostname,
    # SMTP sender login matching config
    smtpd_sender_restrictions = permit_mynetworks, reject_sender_login_mismatch, reject_authenticated_sender_login_mismatch, reject_unauthenticated_sender_login_mismatch
    smtpd_sender_login_maps = mysql:/etc/postfix/mysql_virtual_sender_maps.cf, mysql:/etc/postfix/mysql_virtual_alias_maps.cf
    # SMTP AUTH config here
    broken_sasl_auth_clients = yes
    smtpd_sasl_auth_enable = yes
    smtpd_sasl_local_domain = $myhostname
    smtpd_sasl_security_options = noanonymous

cp /usr/lib64/sasl2/smtpd.conf /usr/lib64/sasl2/smtpd.conf.bak

vi /usr/lib64/sasl2/smtpd.conf

    pwcheck_method: authdaemond
    log_level: 3
    mech_list: PLAIN LOGIN
    authdaemond_path:/var/spool/authdaemon/socket

service postfix restart
# 通过以下命令获得postmaster@extmail.org的用户名及密码的BASE64编码：
perl -e 'use MIME::Base64; print encode_base64("postmaster\@mail.example.com")'

perl -e 'use MIME::Base64; print encode_base64("extmail")'

# 开始测试
telnet localhost 25
    Trying 127.0.0.1...
    Connected to localhost.localdomain (127.0.0.1).
    Escape character is '^]'.
    220 mail.example.com ESMTP Postfix - by extmail.org
    ehlo mail.example.com <<输入内容(域名)
    250-mail.example.com
    250-PIPELINING
    250-SIZE 5242880
    250-VRFY
    250-ETRN
    250-AUTH LOGIN PLAIN
    250-AUTH=LOGIN PLAIN
    250-ENHANCEDSTATUSCODES
    250-8BITMIME
    250 DSN
    auth login <<输入内容
    334 VXNlcm5hbWU6
    cG9zdG1hc3RlckByb29raWUuY29t <<输入内容(用户名)
    334 UGFzc3dvcmQ6
    ZXh0bWFpbA== <<输入内容(密码)
    235 2.7.0 Authentication successful ##显示这个说明认证成功
    Quit <<输入内容
    221 2.0.0 Bye
    Connection closed by foreign host.
{% endhighlight %}

TO BE CONTINUE...

[下载]: http://mirror.extmail.org/iso/emos/EMOS_1.6_x86_64.iso