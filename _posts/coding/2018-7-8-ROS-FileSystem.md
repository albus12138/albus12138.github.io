---
layout: post
title: ROS 文件系统及包结构
category: coding
description: ROS Kinetic 文件系统, 包
---

## ROS 文件系统

文件系统概念

- 包(Packages): 包是ROS代码的基础单元, 其中包含库、可执行文件、脚本等等
- 配置文件(Manifests): package.xml是一个包的描述文件, 它被用于描述包与包之间的依赖关系, 以及版本、许可证等元信息

### 文件系统工具

- rospack = ros + pack(package)

	`rospack find [package_name]`

- roscd = ros + cd(change directory)

	`roscd [location_name[/subdir]]` roscd 是 rosbash 套件的一部分, 它可以用来在包之间切换路径, 和其他 ros 工具一样, roscd 仅会在 ROS_PACKAGE_PATH 中寻找内容
	
	`roscd log` 可以切换到存放 ROS 日志的文件夹, 注意, 如果你在之前没有运行过任何ROS程序, 这个命令会提示你不存在文件夹

- rosls = ros + ls(list)

	`rosls [location_name[/subdir]]` 用于通过包名列目录, 而不是绝对路径

- 和 Ubuntu 原生的 Shell 一样, rosbash 工具套件均支持Tab键自动补全

### 包

#### 创建包

- 组成
	- 一个独立的文件夹
	- package.xml
	- CMakeLists.txt

- 在工作空间中创建包
	- 这是一种推荐的开发方式, 每个包位于src目录下独立的文件夹中

{% highlight python %}
cd ~/catkin_ws/src

#catkin_create_pkg package_name depend1 depend2 depend3
catkin_create_pkg tutorials roscpp rospy std_msgs
{% endhighlight %}

通过上面这条指令可以自动创建一个包结构, 其中依赖不是必填内容

- 查看依赖
	- `rospack depends1 tutorials` 查看 tutorials 包的直接依赖
	- `rospack depends tutorials` 查看 tutorials 包的全部依赖

#### 创建自定义包

- Package.xml
	- Format 1 已经废弃, 故以下内容基于 Format 2 编写

	- 基础结构
		- package 根标签

	- 必要标签
		- name 包名
		- version 包版本
		- description 包描述
		- maintainer 负责包维护的人
		- license 遵守的协议

	- 依赖
		- depend 表示是构建, 导出和执行依赖, 最常用的标签
		- build_depend 构建依赖, 构建这个包时需要的依赖
		- build_export_depend 导出依赖, 将这个包构建为库时需要的依赖
		- buildtool_depend 构建工具依赖, 构建这个包时需要的工具, 默认为catkin
		- exec_depend 执行依赖, 在运行这个包时需要的依赖
		- test_depend 测试依赖, 针对单元测试的附加依赖, 不可与构建和执行依赖重复
		- doc_depend 这个包在生成文档时需要的依赖

	- MetaPackages 不太明白这东西0.0

	- 附加标签
		- url 一个指向更多信息的链接, 一般是wiki
		- author 包作者

{% highlight xml %}
<package format="2">
  <name>foo_core</name>
  <version>1.2.4</version>
  <description>
    This package provides foo capability.
  </description>
  <maintainer email="ivana@willowgarage.com">Ivana Bildbotz</maintainer>
  <license>BSD</license>

  <url>http://ros.org/wiki/foo_core</url>
  <author>Ivana Bildbotz</author>

  <buildtool_depend>catkin</buildtool_depend>

  <depend>roscpp</depend>
  <depend>std_msgs</depend>

  <build_depend>message_generation</build_depend>

  <exec_depend>message_runtime</exec_depend>
  <exec_depend>rospy</exec_depend>

  <test_depend>python-mock</test_depend>

  <doc_depend>doxygen</doc_depend>
</package>
{% endhighlight %}

- CMakeLists.txt

	- CMake 版本 `cmake_minimum_required(VERSION 2.8.3)`
	- 包名 `project(robot_brain)`
	- 寻找依赖包 `find_package(catkin REQUIRED)`, 注意, 这里只应包含构建依赖, 不应该包括执行依赖
	- catkin_package 是 catkin 提供的一个 CMake 宏, 这个函数必须在 `add_library` 和 `add_executable` 之前调用
		- INCLUDE_DIRS - 包含路径
		- LIBRARIES - 引用的库
		- CATKIN_DEPENDS - 其他依赖的 catkin 包
		- DEPENDS - 其他依赖的非 catkin 包
		- CFG_EXTRAS - 附加编译选项

	{% highlight CMake %}
	catkin_package(
		INCLUDE_DIRS include
		LIBRARIES ${PROJECT_NAME}
		CATKIN_DEPENDS roscpp nodelet
		DEPENDS eigen opencv)
	{% endhighlight %}

	- [更多内容](http://wiki.ros.org/catkin/CMakeLists.txt#Specifying_Build_Targets)

#### 构建包

- `catkin_make`
- 关于C++和Python构建需要修改的内容会在后面提到