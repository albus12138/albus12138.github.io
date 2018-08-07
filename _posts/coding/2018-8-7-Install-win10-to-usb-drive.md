---
layout: post
title: 安装 Windows 10 到移动硬盘
category: coding
description: 安装 Windows 10 到移动硬盘
---

## 准备工作

- Windows 10 镜像
- 至少 32 GB 空间移动硬盘
- WinToUSB

## 安装过程

- 尝试 1:
	- 和正常安装 Windows 一样, 先烧录u盘启动盘, 然后从u盘启动, 选择驱动器时提示不支持 USB 和 IEEE 1394 端口

- 尝试 2:
	- Windows 10 安装失败后又尝试 Windows 7, 烧录u盘启动盘, 修复uefi引导(手动修复 和 rufus自动修复), 从u盘启动时显示 BCD 文件损坏, 镜像在 vmware 下可用, 错误原因不明

- 尝试 3:
	- 尝试 WTGA (Windows To Go 助手), 等待十几分钟没有进展, 强制终止

- 尝试 4:
	- WinToUSB 选择镜像和移动硬盘, 直接创建安装盘, 成功