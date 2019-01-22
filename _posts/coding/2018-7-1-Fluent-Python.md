---
layout: post
title: Fluent Python笔记
category: coding
description: Fluent Python 内容小结
---

## Part 1: 序言

### Chapter 1 | 数据模型

- `magic method` 是一种特殊的方法,形式如 `__getitem__`,可以让我们自定义的类具有一些原生类的效果,如 `len(obj)` 就是调用对象的 `__len__` 方法,如果我们自定义的类实现了这个方法,就可以通过 `len` 获得长度 [更多内容](https://docs.python.org/3/reference/datamodel.html#special-method-names)

## Part 2: 数据结构

### Chapter 2 | 序列

- 分类
	- Container(容器) sequences & Flat(平坦) sequences
		- list, tuple, collections.deque(Double-Ended Queue)
		- str, bytes, bytearray, memoryview, array.array

	- Mutable(可修改) sequences & Immutable(不可修改) sequences
		- list, bytearray, memoryview, array.array, collections.deque
		- tuple, str, bytes

- 递推式构造列表 (List Comprehensions and Generator Expressions)
	- `[ord(x) for x in "ABC" if ord(x) < ord('C')]` => `[65, 66]`
	- 通过这样的方式构建列表相比于循环或是map更具有可读性 [执行效率测试](https://github.com/fluentpython/example-code/blob/master/02-array-seq/listcomp_speed.py)
	- __注意__:在Python 3.x以前,这个表达式会导致内部循环变量泄露,如果在外部有同名符号会被覆盖

- 解包 (Unpacking)
	- 元组: `latitude, longitude = (33.9425, -118.408056)`
	- 处理多余元素: `a, *b, c = range(5)` => `a = 0, b = [1, 2, 3], c = 4`
	- 嵌套元组: `name, cc, pop, (latitude, longitude) = ('Tokyo', 'JP', 36.933, (35.689722, 139.691667))`
	- 命名元组:
	{% highlight python %}
	from collections import namedtuple
	City = namedtuple('City', 'name country population coordinates')
	tokyo = City('Tokyo', 'JP', 36.933, (35.689722, 139.691667))
	# >>> tokyo
	# City(name='Tokyo', country='JP', population=36.933, coordinates=(35.689722, 139.691667))
	# >>> tokyo.population
	# 36.933
	# >>> tokyo[1]
	# 'JP'
	{% endhighlight %}

- 切片对象 (Slice objects)
	- `s[a:b:c]` 从a到b步长为c
	- `slice(start, stop[, step])` 生成一个切片对象,使用方法 `s[sliceObj]`
	- 多维切片 `a[m:n, i:j]` `a[i, :, :,]` [更多内容](http://scipy.github.io/old-wiki/pages/Tentative_NumPy_Tutorial)
	- 使用切片对象修改可修改序列
	{% highlight python %}
	l = list(range(10))
	# l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
	l[2:5] = [20, 30]
	# l = [0, 1, 20, 30, 5, 6, 7, 8, 9] 不足的元素会被删除
	del l[5:7]
	# l = [0, 1, 20 ,30, 5, 8, 9]
	# l[2:5] = 100 错误!
	l[2:5] = [100]
	# l = [0, 1, 100, 8, 9]
	{% endhighlight %}

- 构建嵌套列表
	- `[['_'] * 3 for i in range(3)]` => `[['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]`

- +=问题
	- `t = (1, 2, [10, 20]); t[2] += [30, 40]` 会引发一个TypeError,但t的值仍会被修改
	- 所以,在不可变序列中放入一个可变类型是一个不明智的选择

- 排序
	- `obj.sort(key, reverse) or sorted(obj, key, reverse)` 其中 `sorted` 不改变原序列顺序
	- `reverse`为真时,将降序排列,key是一个单参数函数,通过该函数返回值排序
	- 二分查找 & 插入
		- 因为排序操作付出的代价是很高的,所以在排序后保持序列有序就十分重要
		- `bisect.bisect(haystack, needle)` 在 `haystack` 中查找探针应该插入的位置, 再通过 `haystack.insert(index, needle)` 将探针插入对应位置
		- `bisect.indort(haystack, needle)` 会直接将探针插入序列,并且比两步操作更加迅速

- 数组 (Array)
	- 如果一个列表只包含数字,那么数组是一个很好的选择,数组比列表效率更高,同样支持可变序列的所有方法
	- 快速存取: `frombytes` 和 `tofile`

- MemoryViews (内存查看对象?)
	- 受 NumPy 和 SciPy 启发产生,可以修改序列中部分内容而不影响其他部分,类似于C语音的指针
	- 大概在大量数据处理时使用可以降低计算复杂度? 个人感觉日常用途不明

- 双端队列 (Double-Ended Queue)
	- 队列的设计目的是为了快速从端点插入或移除数据
	- 双端队列在声明是需要显式声明最大长度,当队列中的元素达到最大长度后继续添加元素会从另一端移除元素
	- 除了双端队列,Python标准库还实现了一些其他队列
		- `queue` 线程安全的单端序列,在达到最大值后会等待移除而不是自动移除
		- `multiprocessing` 提供了支持多进程的队列(
		- `asynio` 异步队列

### Chapter 3 | 字典和集合

- 通用映射类型 (Generic Mapping Types)
	- `collections.abc` (Abstract Base Classes)模块提供了 `Mapping` 和 `MutableMapping` 两个类型,用于规定字典和相似类型的接口
	- 所有的映射类型都要求他们的关键字是可哈希的
		- 可哈希对象 (Hashable)
			- 所有原子级不可变的类型都可以计算哈希值,所以一个仅包含不可变类型的静态集总是可以哈希的,用户定义的类型默认时可哈希的,其哈希值是他们的 `id()`

- 字典 (Dicts)
	- 表达方式
		- 从2.7开始字典的声明可以使用递推式构造 `{country: code for code, country in DIAL_CODES}` 其中 `DIAL_CODES = [(86, 'China'), ...]`
	- 通过setdefault处理不存在的关键字
	- defaultdict: 在声明时提供一个可供调用的初始化函数(如list, 会返回一个空列表), 在索引到一个不存在的key时会调用这个函数
	- `__missing__`: 在通过get索引时会自动调用, 处理不存在索引引发的错误
	- 其他字典
		- OrderedDict: 内部元素的顺序会维持插入的顺序
		- ChainMap: 可以将多个映射合并为一个, 如对多个进行查询操作可以用到
		- Counter: 会对每一个出现的key进行计数, 可以用于统计字符串中字符数量
		- UserDict: 用纯Python实现的映射类型, 和普通字典相似
	- 扩展
		- 在对基础字典进行扩展以实现自定义映射类型时, 更推荐使用 UserDict, 因为它是以纯 python 实现的, 扩展起来更加方便, 比起使用dict代码可能更简单

- 不可变映射类型 (Immutable Mappings)
	- 在我们需要维持一些字典内容不被误操作所改变时, 我们可以通过 `MappingProxy` 实现, 向 `MappingProxyType(obj)` 传入一个映射对象, 会返回一个只读映射对象, 这个只读对象会随着被传入的对象变化而变化, 但直接对该只读对象的操作不会生效, 更不会影响到原对象

- 集合 (Sets)
	- 集合是一个在 Python 历史中相对较新的内容, `set` 和 `frozenset` 在 Python 2.6 时被纳入内建类型
	- 集合一个非常常见的功能就是去重, 集合内的所有元素是不重复的, 同时, 集合内的所有元素必须是可哈希的, `set` 本身是不可哈希的, 而 `frozenset` 是可哈希的, 所以可以在 `set` 中包含 `frozenset`
	- 集合支持一些集合论的操作, 集合在记录检索方面具有极大的优势(代码简单且执行速度快), 假设你有两份很长的通讯录, 然后要比较这两份通讯录中重叠的条目数量, 集合就是一个很好的选择: `len(mailing_list_1 & mailing_list_2)`
	- 表达方式
		- `s = {1, 2, ...}` 是一个最基础的声明方式, 注意, 你不能用这种方式生成一个空集合, `{}` 会返回一个字典而不是集合
		- 递推表达式: 和上文说明相似

- 哈希表 (Hash Table)
	- 哈希表是一个稀疏的数组, 在基础数据结构说明中, 哈希表的单元被称作 "buckets", Python 会试图保持至少 1/3 的单元是空的, 所以当这个哈希表变得拥挤时, Python会把他复制到一个新的更大的空间中
	- 要向哈希表中添加一个键值对时, 首先计算出这个键值对中关键字的哈希值, 对于用户自定义类的哈希值默认是它的id, 如果需要修改是否相等的判断依据, 要同时修改对应的hash计算方法, 因为当 `a == b` 时, `hash(a) == hash(b)` 必须成立
	- 前面提到的字典和集合就是基于哈希表建立的, 因此对于键的搜索是十分迅速的
	- 对字典进行空间优化(不推荐): 由于字典是基于哈希表的, 在高效的同时, 对于空间的有一定的浪费, 可以通过修改 `__slots__` 方法, 这个内容会在第九章进行详细讨论, 但如果不能证明对空间的优化是必要的, 请不要这样做, 因为优化总是在牺牲代码的可维护性
	- 哈希表中的元素(这里的元素指不基于哈希表的数据类型, 如元组)内部键值对顺序与插入顺序有关, 不影响哈希值计算, 向一个字典中添加内容可能会改变键值顺序(相当于向哈希表中插入内容)

### Chapter 4 | 文本和字节

- 从 Python 3 开始, 文本和字节有了明确的界线, 隐式地将字节转换为文本不再存在

- 字符 (Characters)
	- 从 2015 年开始, 我们将字符定义为了一个 Unicode 字符, 所以你从 Python 3 str 中获得的是 Unicode 字符, 而你从 Python 2 str 中获取的是字节

- 字节 (Bytes)
	- 字节在 Python 3 中有两个类型, 不可变类型 `bytes` 和可变类型 `bytearray`, bytearray 在 Python 2.6 中作为 str 的别名被加入
	- 表示方法: 尽管字节是一串数字, 但是一般还是会将其中 ASCII 字符和转义字符以字符形式显示, 其余用 \x00 这样的形式显示

- 结构体 (Struct)
	- 结构体可以按照规则将一串字节分解为一个元组, 如 `struct.unpack('<3s3sHH', packed_bytes)` 其中 < 代表小端序, 3s 代表长度为3的字节序列, H 代表 16-bits 数字

- 编码器/解码器 (Encoders/Decoders)
	- Python 发行版支持100余种编码, 每种编码有自己的名字和许多别名, 如 `utf_8` 有别名 `utf8 utf-8 U8` 等等
	- str.encode(codec): 字符 编码为 字节
	- str.decode(codec): 字节 解码为 字符 (这两个概念我混淆了很久Orz)

- UnicodeEncodeError/UnicodeDecodeError
	- 这两个错误可以说是 Python 2 里十分常见却难以排查的错误了, 引发这两个错误的原因就是在编码或解码的过程中, 某个字节在指定的编码中不存在对应的字符
	- 要在程序中处理这两个错误, 我们可以通过 encode/decode 函数的 errors 参数来控制, 可供选择的参数有:
		- strict: 默认参数, 会引发错误
		- replace: 用 U+FFFD 替换没有找到的字符
		- ignore: 忽略没有找到的字符

- SyntaxError
	- 由于 Python 3 的默认编码是 utf-8, Python 2 的默认编码是 ascii, 所以如果你的代码文件不是以对应编码保存, 并且没有声明编码的话, 在解释器读取代码时就会发生错误
	- `# coding: cp1252` 在代码开头加上这一条, 解释器就会按照cp1252进行读取

- 从 Python 3 开始, 可以使用非ASCII字符为变量命名了, 似乎并不利于与不同语言的人进行交流?

- 如何检测一串字节的编码
	- 没有办法准确得到结果, 你必须已知编码才能将字节转换为字符
	- chardet.detect(bytes) 可以帮助你猜测一串字节的编码类型, 并给出可信度

- 处理文本文件
	- 推荐流程: 在读入时将字节转换为字符串, 在程序中仅处理字符串, 在输出时再编码为字节序列
	- 注意: read 和 write 函数的默认编码均与系统编码一致, 如果在 windows 系统, 默认编码为 cp1252, 可以通过在打开文件时添加 encoding 参数控制输入输出编码

- 关于默认编码
	- GNU/Linux 和 OSX 中, 均为 utf-8
	- Windows 中, python默认文件编码为 cp1252, 终端输入输出编码为 cp850, 系统默认编码为 utf-8, 文件系统编码为 mbcs (好混乱......)

- 字符串比较
	- 标准化 Unicode
		- 由于 Unicode 同一个字符可能存在不同的字节表达形式, 所以在比较前应先进行标准化 `unicodedata.normalize`
		- NFC 将字节压缩, 产生最短的字符串
		- NFD 将字节扩展, 将压缩字符扩展为基础字符和组合字符
		- NFKC/NFKD 中的 K 代表 compatibility, 会更加严格进行转换, 如 ½ (U+00BD) 会被转换为 1/2, 4<sub>2</sub> 会被转换为 42, 所以在使用前应仔细考虑

	- 大小写转换
		- str.casefold() 是在 Python 3.3 中添加的新特性, 可以将字符转换为小写, 在纯 ASCII 字符串中与 str.lower() 效果相同
		- 存在两个特例
			- μ 转换后的字符与原字符看上去相同
			- ß 转换后为 ss8
		- 对于 Python 3.4 来说, 共计 116 个字符会与 lower 产生的结果不同, 仅占全部 110,122 个字符的 0.11%

	- 两个实用工具函数

	{% highlight python %}
	from unicodedata import normalize

	def nfc_equal(str1, str2):
		return normalize('NFC', str1) == normalize('NFC', str2)

	def fold_equal(str1, str2):
		return (normalize('NFC', str1).casefold() == normalize('NFC', str2).casefold())
	{% endhighlight %}

	- 极限标准化
		- 去除区分标志 (声调, 变音符号等等), 可以避免用户错误使用区分符号, 但也会大大降低搜索精度

	{% highlight python %}
	import unicodedata
	import string

	def shave_marks(txt):
		norm_txt = unicodedata.normalize('NFD', txt)
		shaved = ''.join(c for c in norm_txt if not unicodedata.combining(c))
		return unicodedata.normalize('NFC', shaved)

	def shave_marks_latin(txt):
		norm_txt = unicodedata.normalize('NFD', txt)
		latin_base = False
		keepers = []
		for c in norm_txt:
			if unicodedata.combining(c) and latin_base:
				continue  # ignore diacritic on Latin base char
			keepers.append(c)
			# if it isn't combining char, it's a new base char
			if not unicodedata.combining(c):
				latin_base = c in string.ascii_letters
		shaved = ''.join(keepers)
		return unicodedata.normalize('NFC', shaved)

	single_map = str.maketrans("""‚ƒ„†ˆ‹‘’“”•–—˜›""",
							   """'f"*^<''""---~>""")

	multi_map = str.maketrans({
		'€': '<euro>',
		'…': '...',
		'Œ': 'OE',
		'™': '(TM)',
		'œ': 'oe',
		'‰': '<per mille>',
		'‡': '**',
	})

	multi_map.update(single_map)


	def dewinize(txt):
		return txt.translate(multi_map)


	def asciize(txt):
		no_marks = shave_marks_latin(dewinize(txt))
		no_marks = no_marks.replace('ß', 'ss')
		return unicodedata.normalize('NFKC', no_marks)
	{% endhighlight %}

- Unicode 字符排序
	- 标准的对非 ASCII 排序的方法就是 `locale.strxfrm`, 在使用这个函数前, 要先设置语言和编码
		- `locale.setlocale(locale.LC_COLLATE, <your locale>.<encoding>)`
		- `sorted(data, key=locale.strxfrm)`
	- 还有另一种方法可以对 Unicode 字符进行排序, 这是 Django 的开发者开发的库 `PyUCA`, 这个库目前仅支持 Python 3
		- `coll = pyuca.Collator()`
		- `sorted(data, key=coll.sort_key)`

- Unicode 数据库
	- 关于 unicodedata 的内容太多了, 书中也仅仅简单介绍了一点, [更多内容](https://docs.python.org/3/library/unicodedata.html)

- 双模式 API
	- 对于标准库的许多函数都可以接受字符串和字节参数, 并根据参数类型调整处理方法, 如 os 模块在接受一个字节类型的路径输入时返回的内容均为字节类型

- 关于字符串和字节的内容大概就是这些, 关于最后这几部分看的确实比较懵, 平时也很少深入接触 Unicode 相关的内容, 跟着书上的例子看个大概吧 Orz

## Part 3: 函数

### Chapter 5 | 头等函数

- 函数式编程

	- 头等函数 (first-class functions) 也就是说函数能像参数一样被传入另一个函数, 也能作为返回值被返回出来, 可以被存入变量或数据结构
	- 接受以函数作为参数的函数称为高阶函数 (high-order functions)
		- 典型的高阶函数就是 map, filter, reduce 这些函数绝大部分语言都有类似的实现, 可能名字不同

- 匿名函数 lambda

- 7 种可以调用的对象
	- 用户定义函数
	- 内建函数
	- 内建方法
	- 方法
	- 类: 调用 `__new__` 和 `__init__`
	- 类实例: 调用 `__call__`
	- 生成器: 使用 yield 的函数或方法称为生成器, 生成器的调用过程和其他对象不一样, 在 14&16 章会有深入讨论

- 用户定义可调用类型
	- 通过定义 `__call__` 不仅是真正的函数对象, 任意的对象可以做出类似函数的行为

- 函数内省 (Function Introspection)
	- 除了 `__doc__` 方法, 函数对象还有许多其他属性, 可以通过 `dir(obj)` 来查看

- 参数传递
	- 仅关键词参数: 在 Python 3 中, 可以通过在一个可选的关键词前加入一个 `*arg` 参数, 使该参数后的关键词参数仅为能被关键词传递, 如: `func(a, *, b)`, 这个关键词参数并不需要指定一个默认值, 在这个例子中 `b` 仅能通过关键词传递, 因为 `*` 接收了所有除关键词参数以外的参数
	- 检查函数参数: 可以通过默认的 `__code__` 对象来检查参数信息，但不是很清晰，更推荐使用 `inspect.Signature` 对象来检查函数信息
	- 参数类型声明: `def clip(text:str, max_len:'int > 0'=80) -> str: ...` 这些对于参数数据类型的声明仅仅用于提示调用者, python不会对传入的参数进行类型检查, 可以通过 `__annotations__` 查看声明信息, 前面提到的 signature 函数同样可以查看这些信息

- 为函数式编程提供的模块
	- operator
		- 在函数式编程中, 用函数而不是运算符会更加方便, 在传统的函数式编程中, 你可以通过 `reduce, map, filter` 来将一个函数应用于一个序列
		- 通过 `itemgetter` 和 `attrgetter` 可以获取序列中的某个元素, 如用于排序等等
		- 此外, 可以使用 `methodcaller` 来调用一些除运算符以外的函数, 例如: `hiphenate = methodcaller('replace', ' ', '-')` 可以通过调用 hiphenate 将字符串中的空格替换为 '-'
	- functools.partial
		- partial 函数可以用于固定某些参数, 以便通过 reduce 调用该函数, 例如:`picture = partial(tag, 'img', cls='pic-frame')` 生成的 picture 函数固定了第一个参数为 img, 基于关键字的 cls 参数为 pic-frame

- 这一章讲解了一些 Python 函数式编程的基础, 函数可以被赋值给变量, 可以存入任何数据结构中, 可以被作为参数传入其他函数

### Chapter 6 | 设计模式

- 复用策略
	- 经典策略: 定义一系列算法, 分别封装, 并让他们可以交换, 通过策略让客户端独立使用他们
	- 面向函数的策略: 在经典策略中每个被构建的策略都是一个仅有一个方法的类, 同时, 没有状态. 因此, 我们可以使用一系列函数来替代这些类
	- 在模块中发现策略: 可以通过 inspect 和 globals 来获取该模块中的全部函数

- 指令
	- 指令是设计模式中另一个可以通过函数式编程简化的模式, 通过将函数作为参数进行传递, 可以有效简化指令设计模式的代码结构

- 这一章介绍了两种可以通过函数式编程简化的设计模式, 更多关于设计模式的内容可以阅读 《Design Pattern》

### Chapter 7 | 装饰器和闭包

- 装饰器是将被装饰函数作为参数的可执行函数, 可以对被装饰函数进行修改或替换, 严格来说装饰器是一种语法糖, 完全可以通过更易懂的方式实现, 但有时使用起来会更加方便, 关于装饰器最重要的两个特性是他们可以对被装饰函数进行修改, 以及在模块被加载时会被立刻执行

- 上面所说的在模块加载时会被立即执行严格来说是在被装饰函数被定义时执行, 通常是 import, 而被装饰函数并不会被执行, 通常装饰器与被装饰函数处于不同模块中, 在 web 框架中被广泛用于 URL 匹配

- 通过装饰器, 我们可以再一次优化上面提到的复用策略, 将各个策略作为被装饰函数, 在装饰器中构建一个列表, 我们可以很便捷的获取全部策略函数

- 闭包
	- 在了解闭包之前, 需要了解 Python 的变量空间规则, 由于 Python 不需要变量声明, 所以 Python 会假设所有在函数中被定义的变量为该函数的局部变量, 如果你在函数外面定义了一个变量 a, 然后在函数中先读取再修改, 那么会产生一个声明前引用错误, 如果你忘记对一个局部变量进行定义而直接读取的话你可能会在无意中使用了其外部命名空间中对应变量的值
	- 如果想使用外层空间中的变量，需要使用 `nonlocal` 关键字声明，如果想使用全局变量空间中的变量，需要使用 `global` 关键字声明

- 一个简单的装饰器：装饰器本质就是一个将被修饰函数作为参数的函数

```
@clock
def factorial(n):
    return 1 if n < 2 else n*factorial(n-1)

# 等价于直接作为参数传入
clock(factorial(n))
```

- 标准库中的一些装饰器
	- functools.lru_cache: 将函数之前的运行结果保存起来，供后续查询，传入参数是保存的最大长度，建议为2的乘方，默认128，在提升递归函数执行效率方面效果明显，如斐波那契数列，可以节省大量重复计算
	- singledispatch: Python 不支持函数的重载，但 Python 提供了一个装饰器，可以将普通函数变为泛函数，通过注册不同的传入参数类型，来使用不同的重载函数，对于这些重载函数来说，名字没有意义，所以一般使用匿名函数，当然也可以自己起一些名字

- 嵌套装饰器

```
@d1
@d2
def func():
    pass

d1(d2(func()))
```

- 含参数的装饰器:含参数的装饰器一般是通过装饰器工厂(Decorator Factory)实现，通过根据传入参数不同，返回不同的装饰器函数

```
@register(active=True)
def func():
    pass
```

- 这一章主要介绍了闭包的概念和装饰器，其中装饰器的基础原理与闭包相似

## Part 4: 面向对象

### 对象的引用，可变性和回收

<strong>To be Continued... Last updated: Jan 22, 2019</strong>