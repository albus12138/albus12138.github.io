---
layout:     post
title:      Django用户系统扩展笔记
category: coding
description: 和Django的用户系统奋斗的记录~~
---

## 为什么要扩展Django自带的用户系统

在网站的建设中发现自带的用户系统并不能满足使用需求，但又想使用默认的权限系统，所以才有了扩展的想法，在实践过程中也遇到了不少困难Orz

通过对原有User模型的查找，发现User直接继承AbstractUser，所以，我的自定义用户表同样继承了AbstractUser，代码如下：

{% highlight python %}
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser, models.Model):
   nickname = models.CharField(max_length=10)
   join_date = models.DateField(default=datetime.now()) # 账户注册时间
   last_login_date = models.DateField(default=datetime.now()) # 上次登录时间
   use_token = models.BooleanField(default=False) # 是否使用验证码
   token = models.CharField(max_length=50, blank=True) # 验证码生成token
   locked = models.BooleanField(default=False) # 账户锁定
   expire = models.DateField() # 账户有效期

   class Meta:
       permissions = (("can_view_customuser", "读取用户表"),)
{% endhighlight %}