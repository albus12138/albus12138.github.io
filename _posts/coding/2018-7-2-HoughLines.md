---
layout: post
title: 霍夫线变换
category: coding
description: Hough线变换提取图像中直线
---

## 霍夫线变换

### 简介

霍夫线变换是一种在边缘二值图像中提取直线的方法

### 原理

一条直线，在图像二维空间可以用两个变量表示

- 笛卡尔坐标系: y=mx+b
- 极坐标系: r = xcosθ + ysinθ

![直线表示](../../images/HoughLines/1.jpg)

在霍夫变换中，采用极坐标系表示直线

对于平面中的一个任意点(x<sup>0</sup>, y<sup>0</sup>)，可以将通过这个点的一族直线定义为 r<sup>θ</sup> = x<sup>0</sup> cosθ + y<sup>0</sup> sinθ ，所以，每一对(r<sup>θ</sup>, θ)组合就代表一条通过(x<sup>0</sup>, y<sup>0</sup>)的直线

对于一个给定的(x<sup>0</sup>, y<sup>0</sup>)，我们可以画出 r<sup>θ</sup> 关于 θ 的图像，其中 r > 0 且 0 < θ < 2π

![直线族](../../images/HoughLines/2.jpg)

上图即为通过 x<sup>0</sup> = 8, y<sup>0</sup> = 6 的所有直线，再以同样的方法对其他两个点画出曲线，如下图

![多条直线族](../../images/HoughLines/3.jpg)

可以看出，三组直线族对应的曲线相交于点(0.925, 9.6)，也就是说，直线 9.6 = xcos(0.925)+ysin(0.925) 同时通过三个点

所以，在同一点相交的曲线条数，表示这个点代表的直线通过的像素点数，因此，当同一点处相交的曲线数量大于阈值后，我们可以认为这个点代表的直线在图像中是一条直线，霍夫线变换就是追踪二值边缘图像中的每个点对应的曲线交点

### 基于OpenCV的Python实现

- GaussianBlur & Canny 通过高斯滤波提取原图像的边缘二值图像
- HoughLines(边缘二值图像, 极坐标参数θ的分辨率，分辨率对弧度的参考值，检测一条直线需要的像素点数)

{% highlight python %}
import cv2
import numpy as np

img = cv2.imread("test.jpg", 0)
threshold = 50

img = cv2.GaussianBlur(img,(3,3),0)
edges = cv2.Canny(img, 50, 150, apertureSize = 3)
lines = cv2.HoughLines(edges, 1, np.pi/180, threshold)

result = img.copy()
for line in lines[0]:
    rho = line[0]
    theta= line[1]
    if  (theta < (np.pi/4. )) or (theta > (3.*np.pi/4.0)):
        pt1 = (int(rho/np.cos(theta)),0)
        pt2 = (int((rho-result.shape[0]*np.sin(theta))/np.cos(theta)),result.shape[0])
        cv2.line( result, pt1, pt2, (255))
    else:
        pt1 = (0,int(rho/np.sin(theta)))
        pt2 = (result.shape[1], int((rho-result.shape[1]*np.cos(theta))/np.sin(theta)))
        cv2.line(result, pt1, pt2, (255), 1)
cv2.imshow('Canny', edges )
cv2.imshow('Result', result)
cv2.waitKey(0)
{% endhighlight %}