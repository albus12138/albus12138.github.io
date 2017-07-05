---
layout:     post
title:      Django用户系统扩展
category: coding
description: 自己折腾Django用户系统的一点记录，也希望能帮助其他有同样问题的人~
---

## 为什么要扩展Django自带的用户系统

在网站的建设中发现自带的用户系统并不能满足使用需求，比如添加一些字段或者要求用户输入动态验证码，但又想使用默认的权限系统，所以才有了扩展的想法，在实践过程中也遇到了不少困难Orz

## 实现方法

### 继承AbstractUser

原有的User模型继承了AbstractUser，所以你的自定义用户表同样要继承AbstractUser，并在settings.py中添加

> AUTH_USER_MODEL = 'accounts.CustomUser'

accounts是我app的名称，你可以改为你的app名称。

{% highlight python linenos %}
# /mysite/accounts/models.py
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

### 加密password

做完这些，你会发现通过admin添加的用户无法登陆，这是因为Django在数据库中对密码进行了加密存储，不必担心，Django提供了make_password这个方法，你可以通过重写CustomUser.save_model来覆盖掉原有的行为

{% highlight python linenos %}
# /mysite/accounts/admin.py
class CustomUserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if 'pbkdf2_sha256$12000$' != request.POST["password"][:20]: #判断是否已经被加密，这里我只是检验了加密的标识，如果有更好的处理方法欢迎给我发送email:albus.zly@gmail.com
            obj.password = make_password(request.POST["password"])
        obj.save()
{% endhighlight %}

### 修改login页面显示

这时候，你已经可以使用你通过admin添加的用户登录到后台了~但是，我们还没有实现动态验证的功能，首先要修改登录页"admin/login.html"的模版来添加一个输入框，下面这段代码添加到login.html中password的后面。

{% highlight html %}
<!-- /django/contrib/admin/templates/admin/login.html -->
<div class="form-row">
    {{ form.token.errors }}
    <label for="id_token" class="required">{{ form.token.label }}:</label> {{ form.token }}
</div>
{% endhighlight %}

现在还不能看到添加的输入框，因为form中并没有定义token字段，你还要扩展一下登录表单，只需要继承AuthenticationForm就可以了。

{% highlight python linenos %}
# /mysite/accounts/forms.py
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth import authenticate

class CustomAuthenticationForm(AuthenticationForm, forms.Form):
    token = forms.CharField(label="验证码", max_length=50, widget=forms.TextInput)

    error_messages = {
        'invalid_login': "请输入正确的用户名或密码，并确认验证码正确",
        'inactive': "账户未激活",
    }

    def clean(self): # clean是AuthenticationForm原有的方法，在此我只是进行了修改覆盖
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        token = self.cleaned_data.get('token')

        if username and password and token:
            self.user_cache = authenticate(username=username,
                                           password=password, token=token)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
{% endhighlight %}

你现在应该修改urls来告诉Django你要使用自己的模版~在这里偷一下懒→_→需要了解关于修改模版的同学请移步[这里][]

{% highlight python linenos %}
# /mysite/urls.py
from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.contrib.auth import views
from accounts.forms import CustomAuthenticationForm

# 修改login页面url
adminurls = admin.site.urls
adminurls[0][1] = url(r'^login/$', views.login, {'authentication_form': CustomAuthenticationForm}, name='login')

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nktc.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(adminurls)),
)
{% endhighlight %}

### 实现动态验证

到此为止，你已经完成了对token字段的添加，接下来就是检验token是否有效，通过阅读Django官方文档对这里的说明，自定义的Backend应该包含至少Authenticate和get_user两个方法，然后在settings中添加

> AUTHENTICATION_BACKENDS = ('accounts.backends.CustomBackend',)

{% highlight python linenos %}
# /mysite/accounts/backends.py
from accounts.models import CustomUser
from django.utils import timezone

class CustomBackend(object):
    def authenticate(self, username, password, token):
        try:
            user = CustomUser.objects.get(username=username)
            if user.check_password(password):
                if user.use_token and user.vaild_token(token):
                    return user
                elif not user.use_token:
                    return user
            else:
                return None
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
{% endhighlight %}

## The End

嘛~终于做完了自己的用户系统~还有一点小激动呢

[这里]: http://www.ibm.com/developerworks/cn/opensource/os-django-admin/index.html