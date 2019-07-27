2018-4-30-live-in-ubuntu

---
layout: post
title: Ubuntu 配置小结
category: coding
description: 记录一下自己安装Ubuntu的过程吧
---

## 0x00 Installation

- Ubuntu 16.04 ISO

- 烧录U盘启动盘

- 4K对齐：先通过 `Try Ubuntu without Install` 进入系统，因为固态硬盘需要4k对齐，但是Ubuntu和Windows的硬盘对齐不一样，所以可以通过 `Gpart` 先分配一个1M的分区，然后再开始安装系统，因为我是在一块新的固态上面安装的，所以直接在Ubuntu下格式化

- UEFI+GPT：
    + EFI分区：512M，逻辑分区
    + swap分区：1-2倍内存空间，逻辑分区
    + 文件系统：大部分教程推荐分3个分区，分别挂载到 `/`，`/usr`，`/home`，个人感觉没有什么必要，我觉得我用不完512G，所以直接全挂载到根目录了

- 还有就是推荐断网安装，不更新软件包，不然安装过程中很可能出现卡死现象

## 0x01 Update && Cleanup
- 更新
    + 我们在安装系统的时候关闭了更新软件包，所以在装好系统之后还要更新一下
    + `sudo apt-get update && sudo apt-get upgrade`

- 卸载自带应用
    + `udo apt-get remove thunderbird totem rhythmbox empathy brasero simple-scan gnome-mahjongg aisleriot gnome-mines cheese transmission-common gnome-orca webbrowser-app gnome-sudoku  landscape-client-ui-install`
    + `sudo apt-get remove onboard deja-dup`

- 删除libreoffice
    + `sudo apt-get remove libreoffice-common`

- 删除Amazon
    + `sudo apt-get remove unity-webapps-common`
    + 在我卸载掉这个包之后确实删掉了Amazon，但是这个包在我后面装 `unity-tweak-tool` 时又带着Amazon回来了……

- 清理wine残留图标

    > rm ~/.local/share/applications/<Files>
    > rm ~/.local/share/applications/wine/Programs/<Files>
    > rm ~/.config/menu/applications-merged/<Files>

## 0x02 Beautify
- Unity 桌面美化
    + 安装 `Unity Tweak Tools`
        * `sudo apt-get install unity-tweak-tool`
    + 安装主题
        * 我选择的是一款扁平化主题 Flatbulons
        > sudo add-apt-repository ppa:noobslab/themes
        > sudo apt-get update
        > sudo apt-get install flatabulous-theme
        * 图标 ultra-flat-icons
        > sudo add-apt-repository ppa:noobslab/icons
        > sudo apt-get update
        > sudo apt-get install ultra-flat-icons
        * 安装完成后从 `unity tweak tool` 里面修改主题和图标

- Shell 美化
    + 安装zsh并切换
        * `sudo apt-get install zsh`
        * `sudo chsh -s $(which zsh)`
        * 注销，重新登录
    + 安装 `Oh my Zsh`
        * 推荐安装到zsh的插件目录下 `/home/<username>/.oh-my-zsh/plugins/`
        * `mkdir incr && cd incr`
        * 下载 [incr-2.0.zsh](http://mimosa-pudica.net/src/incr-0.2.zsh)
        * 配置zshrc文件 `echo "source ~/.oh-my-zsh/plugins/incr/incr*.zsh" >> ~/.zshrc && source ~/.zshrc`

## 0x03 Configure Environment
- 科学上网

    > sudo apt-get update
    > sudo apt-get install python-pip
    > sudo apt-get install python-setuptools m2crypto
    > sudo pip install shadowsocks
    > sudo apt-get install shadowsocks
    > sudo add-apt-repository ppa:hzwhuang/ss-qt5
    > sudo apt-get update
    > sudo apt-get install shadowsocks-qt5

    + 安装的是图形界面的ss，后面和win下的配置没什么区别
    + 配置浏览器
        * 直接开全局的话不仅会影响我们访问国内网站的速度，还会浪费代理流量
        * Chrome插件：SwitchyOmega
        * 设置自动切换，通过规则列表切换 [gfwlist.txt](https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt)

- Vim
    + `sudo apt-get install vim`

- Git
    + `sudo apt-get install git`
    + 推荐一个图形化界面Git客户端，支持绑定Github帐号 **GitKraken**

- Sublime Text 3

    > sudo add-apt-repository ppa:webupd8team/sublime-text-3    
    > sudo apt-get update    
    > sudo apt-get install sublime-text

    + 安装插件 MarkdownPreview & MarkdownEditing

- WPS Office
    + `sudo apt-get install wps-office`

- Chrome

    > sudo apt-get install libappindicator1 libindicator7
    > wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    > sudo dpkg -i google-chrome-stable_current_amd64.deb
    > sudo apt-get -f install

- uGet+aria2
    + 类似迅雷的会搜索资源加速下载的工具

    > sudo add-apt-repository ppa:plushuang-tw/uget-stable
    > sudo add-apt-repository ppa:t-tujikawa/ppa
    > sudo apt-get update
    > sudo apt-get install aria2 uget

    + 编辑->设置->插件  选择aria2

- TIM
    + 之前看到了基于AppImage打包的Tim和QQ，但还是想自己折腾一下，还是没有成功，最后用的还是基于AppImage的TIM，求知道怎么解决的大佬指导下菜鸡Orz
        * wine是3.0稳定版，TIM是2.1.8版
        * 库文件用原装的 `msvcp60` `riched20` `riched32` 替换了内建的库
        * 字体通过注册表改到了Ubuntu里安装的文泉驿微体黑
        * 启动后可以登录，但是进入消息列表界面后就会崩溃，显示引发崩溃的是dwrite.dll，用原装的库替换也还是会崩溃
    + 附上基于AppImage打包的[Wine-QQ-TIM](https://github.com/askme765cs/Wine-QQ-TIM)
    + **Update: 后来找到了更好用的工具集 [Deepin-Wine-Ubuntu](https://github.com/wszqkzqk/deepin-wine-ubuntu)**

## 0x04 其他工具
- htop: 更好用的系统资源监视器
- System Monitor: 通知栏显示系统资源情况
- Anbox: 安卓虚拟机
- Arronax: 创建start图标
- Kazam: 录屏
- unar: 压缩包解压, 解决unzip乱码问题
- Joplin: Markdown编辑器
- Nixnote: 印象笔记Linux版
- Kdenlive: 视频剪辑
- SMPlaye: 播放器
- GitKraken: git客户端
- Foxit Reader: PDF阅读器
- CuteCom: 串口助手
- Httrack: 静态站点克隆

到这里基本的应用和配置就完成了，剩下的就是安装自己习惯的开发环境了。这篇小结到这里就结束了，之前也尝试过几次Ubuntu，希望这次可以长期生活在Ubuntu下OwO。
