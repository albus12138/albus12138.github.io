---
layout:     post
title:    Git入门
category: coding
description: Git shell的一点记录0.0
---


## 【基础篇】

出处：http://gitref.org/


###  初始化


使用git要做的第一件事就是初始化git代码库了。这里有两种可能：一是自己创建的工程，二是参与别人的工程。对于前者，要做的就是进入到代码的根目录下，执行

>    git init

对于后一种情况，则使用

>    git clone {code location}



###  git很干净


git不会像svn一样在每个目录下面都建立一个.svn目录，而只是在代码根目录下建立一个.git目录。所以相应的，当你执行git status的时候，显示出来的是整个工程的代码修改，而不是像svn一样显示当前目录下的修改。


git只建立一个.git目录的好处是，除了根目录下你需要注意这里比原先多了一个文件夹外，你可以很放心地认为“代码就像它看起来的那样”，你把它copy到任意一个地方都可以。而svn则不行，svn的代码目录是不能够拷贝到其他svn代码库中的，因为svn的索引会冲突。git可以让你保持“人生若只如初见”的感受。



###  git的思维


在git的世界里，代码有三种状态：unstaged, staged 和 committed。


unstaged表示该代码尚未开发完成，staged表示代码开发完成了，准备提交但是尚未提交，committed自然就是提交过的了。


让代码从unstaged变成staged，要通过命令    

>    git add {files}

和

>    git rm {files}

让代码从staged变成committed，自然要使用命令

>    git commit


如上几乎就是单人开发的全部了，是不是很简单？不过故事还没讲完，因为世界不只有你自己。



## 【开发流程篇】

出处：http://nvie.com/posts/a-successful-git-branching-model/


git  真正令人为之欢呼的是它原生的分支概念。


创建一个分支这样操作

>    git checkout -b {new branch name}

合并某一个分支的修改使用这个命令

>    git merge {branch name}


此处应该有掌声！还记得svn中要执行这个操作你要干什么吗？你要先查log，记下要合并的分支中修改的开始版本号和结束版本号，然后在回到trunk目录下写一个我至今都无法记清楚的命令。。。。真是痛苦的回忆！还好现在有git了！



有了基本的分支技能，你需要给自己制定一个规划，如何使用这个强大的分支能力，本篇的《出处》给出了一个很好的模型，我的习惯就由此而来，在这里我就不加赘述了。



以上的所有的操作你都能够独自在自己的机器上完成，但是我们需要一些命令使我们能够和其他人交流代码。首先，你需要给远程的代码库起个别名

>    git remote add {alias} {remote address}

你需要拉取远程代码库的某个分支（默认是master）

>    git pull {alias} {branch name}

你需要提交代码给远程代码库

>    git push {alias} {branch name}

git的命令就是这么简单易懂，完全不需要我解释什么。


有了如上的基础，上手git应该就没有什么问题了，但是要很好的理解，最好还是要把我给出的网址上的内容好好地阅读一下。学好git绝对会让你的生活有序、轻松起来，不要吝惜时间，好好专研一下吧！

