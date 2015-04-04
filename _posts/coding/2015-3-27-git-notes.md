---
layout:     post
title:      Git入门
category: coding
description: Git shell的一点记录0.0
---


## 【基础篇】

出处：http://gitref.org/


###  初始化


使用git要做的第一件事就是初始化git代码库了。这里有两种可能：一是自己创建的工程，二是参与别人的工程。对于前者，要做的就是进入到代码的根目录下，执行

>    git init

对于后一种情况，则使用

>    git clone <code location>

 

###  git很干净


git不会像svn一样在每个目录下面都建立一个.svn目录，而只是在代码根目录下建立一个.git目录。所以相应的，当你执行git status的时候，显示出来的是整个工程的代码修改，而不是像svn一样显示当前目录下的修改。


git只建立一个.git目录的好处是，除了根目录下你需要注意这里比原先多了一个文件夹外，你可以很放心地认为“代码就像它看起来的那样”，你把它copy到任意一个地方都可以。而svn则不行，svn的代码目录是不能够拷贝到其他svn代码库中的，因为svn的索引会冲突。git可以让你保持“人生若只如初见”的感受。

 

###  git的思维


在git的世界里，代码有三种状态：unstaged, staged 和 committed。


unstaged表示该代码尚未开发完成，staged表示代码开发完成了，准备提交但是尚未提交，committed自然就是提交过的了。


让代码从unstaged变成staged，要通过命令      

>    git add <files>

     和

>    git rm <files>

让代码从staged变成committed，自然要使用命令

>    git commit

   
如上几乎就是单人开发的全部了，是不是很简单？不过故事还没讲完，因为世界不只有你自己。



## 【开发流程篇】

出处：http://nvie.com/posts/a-successful-git-branching-model/
 

git  真正令人为之欢呼的是它原生的分支概念。


创建一个分支这样操作

>    git checkout -b <new branch name>

合并某一个分支的修改使用这个命令

>    git merge <branch name>


此处应该有掌声！还记得svn中要执行这个操作你要干什么吗？你要先查log，记下要合并的分支中修改的开始版本号和结束版本号，然后在回到trunk目录下写一个我至今都无法记清楚的命令。。。。真是痛苦的回忆！还好现在有git了！

 

有了基本的分支技能，你需要给自己制定一个规划，如何使用这个强大的分支能力，本篇的《出处》给出了一个很好的模型，我的习惯就由此而来，在这里我就不加赘述了。

 

以上的所有的操作你都能够独自在自己的机器上完成，但是我们需要一些命令使我们能够和其他人交流代码。首先，你需要给远程的代码库起个别名

>    git remote add <alias> <remote address>

你需要拉取远程代码库的某个分支（默认是master）

>    git pull <alias> <branch name>

你需要提交代码给远程代码库

>    git push <alias> <branch name>

git的命令就是这么简单易懂，完全不需要我解释什么。


有了如上的基础，上手git应该就没有什么问题了，但是要很好的理解，最好还是要把我给出的网址上的内容好好地阅读一下。学好git绝对会让你的生活有序、轻松起来，不要吝惜时间，好好专研一下吧！

## 【ssh篇】

###  ssh原理

维基百科：[ssh][]

个人觉得最直接的好处就是Git每次提交时不用输密码

###  基本的ssh配置

GitCafe的帮助文档：如何安装和设置 Git

简要总结一下

  1.打开ssh目录，一般是隐藏的 cd ~/.ssh

  2.生成密钥文件,这样就会生成默认名字为id_rsa和id_rsa.pub

        ssh-keygen -t rsa -C "YOUR_EMAIL@YOUREMAIL.COM"

      (说明：YOUR_EMAIL@YOUREMAIL.COM换成你自己的邮箱)

  3.打开公钥文件（id_rsa.pub），并把内容复制至代码托管平台上

        vim ~/.ssh/id_rsa.pub

    进入 GitCafe -->账户设置-->SSH 公钥管理设置项，点击添加新公钥 按钮，在 Title 文本框中输入任意字符，在 Key 文本框粘贴刚才复制的公钥字符串，按保存按钮完成操作。

  4.测试

        ssh -T git@gitcafe.com

    成功应该提示

        Hi xxxxxx! You"ve successfully authenticated, but GitCafe does not provide shell access.

这样就可以只用ssh协议的URL了,一般默认是https协议的，如图点击SSH即可切换：

![ssh](/images/git-notes/1.jpg)

这样push代码时就不用再输密码了。

###  多账号ssh配置

当你在Github或Gitcafe或Coding都有账号时

假设已经有一个Gitcafe的密钥了，需要需要添加Github的

  1.生成指定名字的密钥

        ssh-keygen -t rsa -C "YOUR_EMAIL@YOUREMAIL.COM" -f ~/.ssh/github

    命名为github（这里叫什么随意，不要重名即可），然后会生成github和github.pub这两个文件

  2.打开公钥文件（id_rsa.pub），并把内容复制至代码托管平台上

  3.修改config文件

        vim ~/.ssh/config

  4.添加如下代码

        Host github.com www.github.com
        IdentityFile ~/.ssh/github

  5.测试

        ssh -T git@github.com

    如果是coding的

        Host coding.net www.coding.net
        IdentityFile ~/.ssh/coding

### 同一平台下的多账号配置

如果有两个Github账号：

  1.也是按照 多账号设置 的方法进行第一第二步
    这样你就已经正确的生成好了两个密钥，假设是：github_a和github_b分别对应的是你的账户aaaaaa和账户bbbbbb

  2.修改config文件

        vim ~/.ssh/config

    添加如下代码

        Host aaaaaa.github.com
        HostName github.com
        User git
        IdentityFile ~/.ssh/github_a
        Host bbbbbb.github.com
        HostName github.com
        User git
        IdentityFile ~/.ssh/github_b

  3.修改ssh URL
    例如原来的url是：git@github.com:aaaaaa/xxxxxx.git
    需要改成：git@aaaaaa.github.com:aaaaaa/xxxxxx.git
    bbbbbb账号的修改也是如此

最后补充一点（这部分Git熟悉的基本可以略过）：有些童鞋可能在设置这个多账号前已经配置了一个Github的ssh，然后把代码clone下来，配置多账号后，原来的代码就提交不上了。

此时你进入 原来clone的代码文件夹下，执行 git remote -v，即可看到远处资源库路径

如：git@github.com:aaaaaa/xxxxxx.git

执行git remote remove origin删除该远程路径

执行git remote add origin git@aaaaaa.github.com:aaaaaa/xxxxxx.git加上正确的远程仓库。