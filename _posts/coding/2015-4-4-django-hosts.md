---
layout:     post
title:      Django多域名
category: coding
description: 将不同域名解析到不同app
---

当你的project下面有多个app需要解析不同的域名，但你又想在同一个project内启动时，你需要[Django-Hosts][]

## Overview

Django-Hosts是Django的一个app，这个app可以将不同域名请求解析到不同的app

举个栗子，你有example.com，你希望a.example.com解析到a这个app，b.example.com解析到b这个app，那么就添加下面这段代码：

{% highlight python %}
# mysite/hosts.py
from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'a', 'a.urls', name='a'),
    host(r'b', 'b.urls', name='b'),
)
{% endhighlight %}

这段代码会将a.urls中的URL配置到a.example.com，b同理。

## 安装&配置

1.安装，推荐使用pip安装

>      pip install django-hosts

2.添加 'django_hosts' 到 INSTALLED_APPS

{% highlight python %}
# mysite/settings.py
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',

    ...

    'django_hosts',
)
{% endhighlight %}

3.添加 'django_hosts.middleware.HostsRequestMiddleware' 和 'django_hosts.middleware.HostsResponseMiddleware' 到 MIDDLEWARE_CLASSES 的开始和结尾

{% highlight python %}
MIDDLEWARE_CLASSES = (
    'django_hosts.middleware.HostsRequestMiddleware',

    ....

    'django_hosts.middleware.HostsResponseMiddleware',
)
{% endhighlight %}

4.在urls.py同目录下创建hosts.py

{% highlight python %}
from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'a', 'a.urls', name='a'),
    host(r'b', 'b.urls', name='b'),
)
{% endhighlight %}

5.设置 ROOT_HOSTCONF

{% highlight python %}
# mysite/settings.py
ROOT_HOSTCONF = 'mysite.hosts'
{% endhighlight %}

6.设置 DEFAULT_HOST

{% highlight python %}
# mysite/settings.py
DEFAULT_HOST = 'a'  #这里写默认host的name
{% endhighlight %}


[Django-Hosts]: https://pypi.python.org/pypi/django-hosts