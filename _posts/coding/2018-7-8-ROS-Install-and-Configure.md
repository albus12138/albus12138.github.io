---
layout: post
title: ROS 安装及环境配置
category: coding
description: 在 Ubuntu 16.04 上安装 ROS Kinetic
---

## 安装

Kinetic 版仅支持 Ubuntu 15.10/16.04 和 Debian 8 通过 deb 包安装

- 配置 apt 源

{% highlight shell %}
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116

sudo apt-get update
sudo apt-get install ros-kinetic-desktop-full
{% endhighlight %}

上面 keyserver 的地址可以换成 `hkp://keyserver.ubuntu.com:80` 访问速度比较快

- 初始化 rosdep

在开始使用ROS之前,我们还需要对rosdep进行初始化

{% highlight shell %}
sudo rosdep init
rosdep update
{% endhighlight %}

一开始初始化时候一直无法解析 raw.githubusercontent.com , 最后发现是校园网dns的问题, 换了dns之后就可以访问了

安利一个DNS: 主DNS `1.1.1.1` 备用DNS `1.0.0.1`

- Shell 环境配置

在打开一个Shell会话时, 我们希望ROS的环境变量可以被自动的添加而不是手动添加

{% highlight shell %}
echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc
source ~/.bashrc
{% endhighlight %}

上面是针对bash环境的配置, 我平时用的是zsh, 所以用了下面这两条命令配置

{% highlight shell %}
echo "source /opt/ros/kinetic/setup.zsh" >> ~/.zshrc
source ~/.zshrc
{% endhighlight %}

- 安装一些便于创建和管理ROS工作区的工具

`sudo apt-get install python-rosinstall python-rosinstall-generator python-wstool build-essential`

到这为止, ROS的安装就基本结束了

## 环境管理

- 检查 ROS_ROOT 和 ROS_PACKAGE _PATH : `printenv | grep ROS`

## 建立工作空间

{% highlight shell %}
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws
catkin_make

source devel/setup.zsh
echo $ROS_PACKAGE_PATH
{% endhighlight %}

catkin_make 是一个非常方便的用来创建工作空间的工具, 第一次运行时会在你的工作空间内生成一个CMakeList.txt符号链接, 以及build和devel文件夹, 在建立完工作空间后, 我们需要让我们的工作空间位于ROS环境的最顶端, 通过执行该工作空间下devel里面的setup完成, 这里我使用的是zsh, 如果你的终端时bash, 请使用setup.bash :-)

如果工作空间配置正确, 你应该看到类似这样的输出: `/home/r4phael/catkin_ws/src:/opt/ros/kinetic/share`

另外, 在整个过程中, 请使用系统自带的python环境, 我之前用pyenv装了多版本的python, 在建立工作空间时, 我终端的python解释器是自己装的3.6.5, 导致找不到catkin_pkg