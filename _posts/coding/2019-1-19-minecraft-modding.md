---
layout: post
title: Minecraft Mod 开发
category: coding
description: Minecraft 1.7.10 Modding with Forge
---

## 开发环境搭建

1.7.10已经是一个很古老的版本了……很多文档都有或多或少的问题，记录下配置过程。一开始我是想用IDEA的，在多次尝试失败后还是用了eclipse。IDEA 失败的原因似乎是因为 1.7.10 forge 使用的 gradle 版本过低，无法识别出 openjdk_1.8 的版本号，因此导致 IDEA 的 gradle 面板无法使用，手动提升 gradle 版本是可行的，但 gradle 版本过高后会导致无法从 maven 仓库中找到 forge 插件，我也没有具体测试是否存在既兼容 openjdk_1.8 又能找到对应 forge 插件的版本。

还有就是由于某些原因，建议全程使用 SSR 全局模式或 proxychains 等工具加速，避免网络问题出现错误。

- 开发环境：
	- OS: Ubuntu 16.04 LTS
	- Java: OpenJDK 1.8
	- Gradle: 2.0
	- Eclipse

- 首先是从 Forge 官网下载源码，1.8以前下载SRC，之后下载MDK，解压到工作目录内，目录结构大致如下
```
Forge1.7.10-1614
└── forge-1.7.10-10.13.4.1614-src
     ├── build.gradle
     ├── CREDITS-fml.txt
     ├── eclipse
     ├── forge-1.7.10-10.13.4.1614-1.7.10-changelog.txt
     ├── gradle
     ├── gradlew
     ├── gradlew.bat
     ├── LICENSE-fml.txt
     ├── MinecraftForge-Credits.txt
     ├── MinecraftForge-License.txt
     ├── README.txt
     └── src
```

- 反编译 Minecraft `$ ./gradlew -i setupDecompWorkspace`

- 建立 Eclipse 项目 `$ ./gradlew -i eclipse`

- 将工作目录作为项目导入到 Eclipse 中

- 编译 `$ ./gradlew -i build`

- 运行客户端 `$ ./gradlew -i runClient`

- 运行服务端 `$ ./gradlew -i runServer`