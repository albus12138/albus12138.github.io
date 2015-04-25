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



[下载]: http://mirror.extmail.org/iso/emos/EMOS_1.6_x86_64.iso