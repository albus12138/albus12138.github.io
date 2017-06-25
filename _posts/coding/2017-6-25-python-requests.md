---
layout: post
title: Requests模块
category: coding
description: 超好用的python第三方模块requests使用方法介绍
---

## 0x00 环境安装

>	pip install requests

或源码安装

>	git clone git://github.com/kennethreitz/requests.git
>	cd requests
>	python setup.py install

## 0x01 发送请求

使用requests库发送HTTP请求非常简单，API写的恰当好处

{% highlight python %}
import requests
r = requests.get("http://albus12138.github.io")
# r = requests.get("http://albus12138.github.io", timeout=5) 设置5秒超时

r = requests.post("http://albus12138.github.io")
r = requests.head("http://albus12138.github.io")
r = requests.put("http://albus12138.github.io")
r = requests.delete("http://albus12138.github.io")
{% endhighlight %}

这里我们就得到了一个命名为`r`的response对象

* r.content -- 以字节方式获取相应内容

* r.cookies -- 以字典(CookieJar)的方式获取相应的Cookies

* r.encoding -- 相应内容编码格式

* r.headers -- 以字典的方式获取响应头

* r.is_permanent_redirect -- 响应状态是否为 301 永久重定向

* r.is_redirect -- 响应状态是否为 302 重定向

* r.json -- 调用requests内置的json解析器，将响应内容解析为json，失败时会抛出异常

* r.raw -- 获取原始响应内容，如果你想要这样做，请在get时添加stream=True参数

* r.request -- 获取对应的请求对象

* r.status_code -- 获取响应状态码

* r.text -- 以字符串方式获取响应内容

* r.url -- 获取请求地址

## 0x02 添加参数

添加URL参数，手动构造如`example.com/index?param=abc`的URL十分繁琐，在requests中可以使用params传入字典参数，自动生成带参数的URL

{% highlight python %}
params = {"key1": "value1", "key2": "value2"}
r = requests.get("http://albus12138.github.io", params=params)
# 这里可以通过 r.url 获取生成好的URL
{% endhighlight %}

注意：字典中值为`None`的参数不会被添加到URL中

添加POST参数：

{% highlight python %}
payload = {"key1": "value1", "key2": "value2"}
r = requests.post("http://albus12138.github.io", data=payload)
# r.text
{% endhighlight %}

## 0x03 使用会话

有时候我们想要请求的内容需要登陆后访问，如果手动添加cookie十分不便，这种情况下使用会话可以有效节省精力，专注于一些更重要的内容

{% highlight python %}
sess = requests.Session()
payload = {"usr": "albus", "pwd": "albus"}
r = sess.post("http://albus12138.github.io/login", data=payload)
r = sess.get("http://albus12138.github.io/admin")
{% endhighlight %}

## 0x04 使用代理访问

如果想要使用代理，可以为请求添加`proxies`参数

{% highlight python %}
proxies = {
	"http": "http://10.10.1.10:3128",
	"https": "https//10.10.1.10:3129",
	"http": "http://user:pass@10.10.1.10:3128/",
	'http': 'socks5://user:pass@host:port'
}
{% endhighlight %}