# 小蚁摄像机视频导出工具 v0.1 2014-12-27


## 先设置摄像机的 IP 地址
> cam-ip.txt 文件写上摄像机所在局域网的 IP 地址
> IP 地址，可以从路由器的 DHCP 客户列表中找到，客户端名称以 ANTSCAM 开头就是，后面一串字符是你摄像机的编号

运行 main.py 即可自动连接摄像机导出视频到 videos 文件夹下面

last-date.txt 保存最后导出的日期，下次导出将从最后记录的日期开始，格式为 YYYYMMDDHHII
