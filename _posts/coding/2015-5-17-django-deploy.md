---
layout: post
title: Django部署
category: coding
description: CentOS6.5部署Django
---

这个Django项目前段时间用业余时间做了那么久...基本上完成了，现在终于到了部署到服务器上的时候啦~~~

部署环境：

* HTTP反向代理服务器---Nginx 1.015

* 数据库---Mysql 5.1.73

* Python WSGI UNIX的HTTP服务器---Gunicorn 19.3.0

* 守护进程---Supervisor 3.1.3

## 安装过程
### Nginx
1.通过yum安装
	yum install nginx
2.修改nginx配置文件
Django对于静态文件处理远不如Nginx，如果部署时还用Django处理静态文件就会影响的性能和安全性了。

	#/etc/nginx/conf.d/default.conf
	
	server {
        listen 80;
        server_name example.com;
		
		#将所有请求转发至Django监听的本地端口
        location / {
                proxy_pass http://127.0.0.1:8000;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

		#防盗链
		location ~* \.(gif|jpg|png|swf|flv)$ {
			valid_referers none blocked *.example.com;
			if ($invalid_referer) {
				rewrite ^/ http://www.example.com/403.html;
				#return 404;
			}
		}

		#处理静态文件(具体URL根据settings.py中的设置更改)
        location /static/ {
                alias /path/to/your/site/static/;
                expires 24h;
                access_log off;
        }
        location /media/ {
                alias /path/to/your/site/media/;
                expires 24h;
                access_log off;
        }
	}
3.测试配置文件是否存在错误
	nginx -t
4.重启nginx服务
	service nginx restart

### Mysql
1.通过yum安装
	yum install mysql-server
2.创建数据库
关于Mysql用户密码的配置在此就不再多说了。
	mysql

	#创建数据库时设置字符编码为utf8, 否则Django中会出现中文乱码
	mysql> create database db_name default charset=utf8;
3.修改Django数据库设置

	#settings.py
	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.mysql',
	        'NAME': 'db_name',
	        'USER': 'username',
	        'PASSWORD': 'password',
	        'HOST': '127.0.0.1',
	        'PORT': '3306'
	    }
	}

### Django、Gunicorn
1.安装Django和Gunicorn
	pip install django gunicorn gevent
2.通过Gunicorn启动Django
	#gevent异步处理
	gunicorn mysite.wsgi:application -w 4 -k gevent -b localhost:8000

### Supervisor
1.安装
	pip install supervisor
2.修改配置

	echo_supervisord_conf > /etc/supervisord.conf
	
	#设置独立配置文件
	#在supervisord.conf末尾添加
	[include]
	files = /etc/supervisord/conf.d/*.conf
	
	mkdir /etc/supervisord
	mkdir /etc/supervisord/conf.d
	cd /etc/supervisord/conf.d

	#进程配置文件
	vi example.conf
	#example.conf
	[program:mysite]
	command=gunicorn mysite.wsgi:application -w 4 -k gevent -b localhost:8000
	directory = /path/to/mysite
	user=root
	stdout_logfile=/var/log/mysite/gunicorn_supervisor.log
	redirect_stderr=true
3.启动Supervisor

	#读入配置文件
	supervisord -c /etc/supervisord.conf
	#启动服务
	service supervisord start
	#重新载入所有配置文件
	supervisorctl reread
	supervisorctl reload
	#启动
	supervisorctl start mysite