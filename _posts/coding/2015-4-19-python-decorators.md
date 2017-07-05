---
layout:     post
title:      Python装饰器
category: coding
description: Python的各式装饰器
---

##  函数式装饰器:装饰器本身是一个函数。

###  装饰函数:被装饰对象是一个函数

一、装饰器无参数：

1.被装饰对象无参数：

{% highlight python linenos %}
>>> def test(func):
    def _test():
        print 'Call the function %s().'%func.func_name
        return func()
    return _test

>>> @test
def say():return 'hello world'

>>> say()
Call the function say().
'hello world'
{% endhighlight %}
 

2.被装饰对象有参数：

{% highlight python linenos %}
>>> def test(func):
    def _test(*args,**kw):
        print 'Call the function %s().'%func.func_name
        return func(*args,**kw)
    return _test

>>> @test
def left(Str,Len):
    #The parameters of _test can be '(Str,Len)' in this case.
    return Str[:Len]

>>> left('hello world',5)
Call the function left().
'hello'
{% endhighlight %} 


二、装饰器有参数：

2.被装饰对象无参数：

{% highlight python linenos %}
>>> def test(printResult=False):
    def _test(func):
        def __test():
            print 'Call the function %s().'%func.func_name
            if printResult:
                print func()
            else:
                return func()
        return __test
    return _test

>>> @test(True)
def say():return 'hello world'

>>> say()
Call the function say().
hello world
>>> @test(False)
def say():return 'hello world'

>>> say()
Call the function say().
'hello world'
>>> @test()
def say():return 'hello world'

>>> say()
Call the function say().
'hello world'
>>> @test
def say():return 'hello world'

>>> say()

Traceback (most recent call last):
  File "<pyshell#224>", line, in <module>
    say()
TypeError: _test() takes exactly argument (0 given)
{% endhighlight %}

 

由上面这段代码中的最后两个例子可知：当装饰器有参数时，即使你启用装饰器的默认参数，不另外传递新值进去，也必须有一对括号，否则编译器会直接将func传递给test()，而不是传递给_test()

2.被装饰对象有参数：

{% highlight python linenos %}
>>> def test(printResult=False):
    def _test(func):
        def __test(*args,**kw):
            print 'Call the function %s().'%func.func_name
            if printResult:
                print func(*args,**kw)
            else:
                return func(*args,**kw)
        return __test
    return _test

>>> @test()
def left(Str,Len):
    #The parameters of __test can be '(Str,Len)' in this case.
    return Str[:Len]

>>> left('hello world',5)
Call the function left().
'hello'
>>> @test(True)
def left(Str,Len):
    #The parameters of __test can be '(Str,Len)' in this case.
    return Str[:Len]

>>> left('hello world',5)
Call the function left().
hello
{% endhighlight %} 
 

###  装饰类：被装饰的对象是一个类

一、装饰器无参数：

1.被装饰对象无参数：

{% highlight python linenos %}
>>> def test(cls):
    def _test():
        clsName=re.findall('(\w+)',repr(cls))[-1]
        print 'Call %s.__init().'%clsName
        return cls()
    return _test

>>> @test
class sy(object):
    value=32

    
>>> s=sy()
Call sy.__init().
>>> s
<__main__.sy object at 0x0000000002C3E390>
>>> s.value
32
{% endhighlight %} 
 

2.被装饰对象有参数：

{% highlight python linenos %}
>>> def test(cls):
    def _test(*args,**kw):
        clsName=re.findall('(\w+)',repr(cls))[-1]
        print 'Call %s.__init().'%clsName
        return cls(*args,**kw)
    return _test

>>> @test
class sy(object):
    def __init__(self,value):
                #The parameters of _test can be '(value)' in this case.
        self.value=value
     
>>> s=sy('hello world')
Call sy.__init().
>>> s
<__main__.sy object at 0x0000000003AF7748>
>>> s.value
'hello world'
{% endhighlight %}

 
二、装饰器有参数：

1.被装饰对象无参数：

{% highlight python linenos %}
>>> def test(printValue=True):
    def _test(cls):
        def __test():
            clsName=re.findall('(\w+)',repr(cls))[-1]
            print 'Call %s.__init().'%clsName
            obj=cls()
            if printValue:
                print 'value = %r'%obj.value
            return obj
        return __test
    return _test

>>> @test()
class sy(object):
    def __init__(self):
        self.value=32

        
>>> s=sy()
Call sy.__init().
value = 32
>>> @test(False)
class sy(object):
    def __init__(self):
        self.value=32

        
>>> s=sy()
Call sy.__init().
{% endhighlight %} 
 

2.被装饰对象有参数：

{% highlight python linenos %}
>>> def test(printValue=True):
    def _test(cls):
        def __test(*args,**kw):
            clsName=re.findall('(\w+)',repr(cls))[-1]
            print 'Call %s.__init().'%clsName
            obj=cls(*args,**kw)
            if printValue:
                print 'value = %r'%obj.value
            return obj
        return __test
    return _test

>>> @test()
class sy(object):
    def __init__(self,value):
        self.value=value

        
>>> s=sy('hello world')
Call sy.__init().
value = 'hello world'
>>> @test(False)
class sy(object):
    def __init__(self,value):
        self.value=value
       
>>> s=sy('hello world')
Call sy.__init().
{% endhighlight %}

 
##  类式装饰器：装饰器本身是一个类，借用__init__()和__call__()来实现职能

###  装饰函数：被装饰对象是一个函数

一、装饰器无参数：

1.被装饰对象无参数：

{% highlight python linenos %}
>>> class test(object):
    def __init__(self,func):
        self._func=func
    def __call__(self):
        return self._func()

    
>>> @test
def say():
    return 'hello world'

>>> say()
'hello world'
{% endhighlight %}

 

2.被装饰对象有参数：

{% highlight python linenos %}
>>> class test(object):
    def __init__(self,func):
        self._func=func
    def __call__(self,*args,**kw):
        return self._func(*args,**kw)

    
>>> @test
def left(Str,Len):
    #The parameters of __call__ can be '(self,Str,Len)' in this case.
    return Str[:Len]

>>> left('hello world',5)
'hello'
{% endhighlight %}

 
二、装饰器有参数

1.被装饰对象无参数：

{% highlight python linenos %}
>>> class test(object):
    def __init__(self,beforeinfo='Call function'):
        self.beforeInfo=beforeinfo
    def __call__(self,func):
        def _call():
            print self.beforeInfo
            return func()
        return _call

    
>>> @test()
def say():
    return 'hello world'

>>> say()
Call function
'hello world'
{% endhighlight %}

 或者：

{% highlight python linenos %}
>>> class test(object):
    def __init__(self,beforeinfo='Call function'):
        self.beforeInfo=beforeinfo
    def __call__(self,func):
        self._func=func
        return self._call
    def _call(self):
        print self.beforeInfo
        return self._func()

    
>>> @test()
def say():
    return 'hello world'

>>> say()
Call function
'hello world'
{% endhighlight %}

 
2.被装饰对象有参数：

{% highlight python linenos %}
>>> class test(object):
    def __init__(self,beforeinfo='Call function'):
        self.beforeInfo=beforeinfo
    def __call__(self,func):
        def _call(*args,**kw):
            print self.beforeInfo
            return func(*args,**kw)
        return _call

    
>>> @test()
def left(Str,Len):
    #The parameters of _call can be '(Str,Len)' in this case.
    return Str[:Len]

>>> left('hello world',5)
Call function
'hello'
{% endhighlight %}

 或者：

{% highlight python linenos %}
>>> class test(object):
    def __init__(self,beforeinfo='Call function'):
        self.beforeInfo=beforeinfo
    def __call__(self,func):
        self._func=func
        return self._call
    def _call(self,*args,**kw):
        print self.beforeInfo
        return self._func(*args,**kw)

    
>>> @test()
def left(Str,Len):
    #The parameters of _call can be '(self,Str,Len)' in this case.
    return Str[:Len]

>>> left('hello world',5)
Call function
'hello'
{% endhighlight %}

 

###  装饰类：被装饰对象是一个类

一、装饰器无参数：

1.被装饰对象无参数：

{% highlight python linenos %}
>>> class test(object):
    def __init__(self,cls):
        self._cls=cls
    def __call__(self):
        return self._cls()

    
>>> @test
class sy(object):
    def __init__(self):
        self.value=32

    
>>> s=sy()
>>> s
<__main__.sy object at 0x0000000003AAFA20>
>>> s.value
32
{% endhighlight %}
 

2.被装饰对象有参数：

{% highlight python linenos %}
>>> class test(object):
    def __init__(self,cls):
        self._cls=cls
    def __call__(self,*args,**kw):
        return self._cls(*args,**kw)

    
>>> @test
class sy(object):
    def __init__(self,value):
        #The parameters of __call__ can be '(self,value)' in this case.
        self.value=value

        
>>> s=sy('hello world')
>>> s
<__main__.sy object at 0x0000000003AAFA20>
>>> s.value
'hello world'
{% endhighlight %}

 
二、装饰器有参数：

1.被装饰对象无参数：

{% highlight python linenos %}
>>> class test(object):
    def __init__(self,printValue=False):
        self._printValue=printValue
    def __call__(self,cls):
        def _call():
            obj=cls()
            if self._printValue:
                print 'value = %r'%obj.value
            return obj
        return _call

    
>>> @test(True)
class sy(object):
    def __init__(self):
        self.value=32

        
>>> s=sy()
value = 32
>>> s
<__main__.sy object at 0x0000000003AB50B8>
>>> s.value
32
{% endhighlight %}
 

2.被装饰对象有参数：

{% highlight python linenos %}
>>> class test(object):
    def __init__(self,printValue=False):
        self._printValue=printValue
    def __call__(self,cls):
        def _call(*args,**kw):
            obj=cls(*args,**kw)
            if self._printValue:
                print 'value = %r'%obj.value
            return obj
        return _call

    
>>> @test(True)
class sy(object):
    def __init__(self,value):
        #The parameters of _call can be '(value)' in this case.
        self.value=value

        
>>> s=sy('hello world')
value = 'hello world'
>>> s
<__main__.sy object at 0x0000000003AB5588>
>>> s.value
'hello world'
{% endhighlight %} 


## 总结：
* @decorator后面不带括号时（也即装饰器无参数时），效果就相当于先定义func或cls，而后执行赋值操作func=decorator(func)或cls=decorator(cls)；

* @decorator后面带括号时（也即装饰器有参数时），效果就相当于先定义func或cls，而后执行赋值操作 func=decorator(decoratorArgs)(func)或cls=decorator(decoratorArgs)(cls)；

* 如上将func或cls重新赋值后，此时的func或cls也不再是原来定义时的func或cls，而是一个可执行体，你只需要传入参数就可调用，func(args)=>返回值或者输出，cls(args)=>object of cls；

* 最后通过赋值返回的执行体是多样的，可以是闭包，也可以是外部函数；当被装饰的是一个类时，还可以是类内部方法，函数；

* 另外要想真正了解装饰器，一定要了解func.func_code.co_varnames,func.func_defaults,func.func_argcount，通过它们你可以以func的定义之外，还原func的参数列表，详见Python多重装饰器中的最后一个例子中的ArgsType；另外关键字参数是因为调用而出现的，而不是因为func的定义，func的定义中的用等号连接的只是有默认值的参数，它们并不一定会成为关键字参数，因为你仍然可以按照位置来传递它们。