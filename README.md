# 关于
安腾小蝴蝶的全平台认证脚本，以及图形用户界面版本  

## 测试环境:
* OS X、windows、linux、android、OpenWrt(需要python运行环境，最少路由器也要是8m的闪存)
* Python 2.7.x Python 3(没测试)   
* `图形用户界面版本`不需要Python运行环境，适用于Windows、OS X、Linux

## AHNU用户:
Linux登录校园网方案:  
内网认证使用mentohust，外网用这个python脚本。  

## 其他学校的用户:   
已知测试通过的院校:  
  
* 烟台大学赛尔网
* 广州商学院  

仅支持 `BAS认证`，PPPOE、Web认证并不支持。

# 图形用户界面版本:     
下载之后双击exe安装即可 :)  
Windows版安装包下载地址:[这里](https://github.com/lyq1996/supplicant/releases/download/GUI_test/Personal.exe) 

## 特性:
* 无限制共享  
* 比官方蝴蝶快N倍  
* 支持自定义服务类型

## 不完善的地方:  
* 需要手动输入服务器IP。     
* You tell me....  

# 命令行版本:  

## 配置说明(请勿改变缩进):

```
auth_host_ip = '210.45.194.10'  #这里是你的服务器ip地址
local_ip = '192.168.2.212'  #这里是你本地ip地址(用于绑定发送端口`3848`)
auth_ip = '172.17.142.14'  #这里是你需要认证的ip地址(如果不是NAT，那这两个就是一样的地址)
auth_mac_address = 'aa:bb:cc:dd:ee:ff'  #这里是网卡的MAC地址(貌似可有可无)
username = 'jack'  #用户名
password = '123456'  #密码
client_version = '3.6.4'  #自定义客户端版本
service_type = 'int'  #服务类型
dhcp_setting = '0'  #开启DHCP
message_display_enable = '1'  #显示认证之后的消息(Openwrt并不能显示，所以酌情请设置为不显示)
delay_enable = '0'  #上线之前延迟一点时间(等待服务器重新分配IP?)
reconnet_enable = '1'  #呼吸或上线失败自动重连
```

## 运行步骤:    

搜寻服务器IP和服务类型(如果你不知道的话):

```
$ python an_supplicant.py -search
```
![image](https://github.com/lyq1996/an_supplicant/master/image/usage.jepg)

上线:  
`注意`:在你运行之前，请确保`配置参数`都已填写正确。  

```
$ python an_supplicant.py  
```
![image](https://github.com/lyq1996/an_supplicant/master/image/login_success.jepg)

下线: 
``` 
Ctrl＋C
```

## 一些其它事项:   

如果终端显示permission deined:  
```
$ sudo chmod 755 an_supplicant.py
```  

## 参考&鸣谢:  
> [benchmade](https://github.com/gnehsoah/benchmade)  
> [swiftz-protocal](https://github.com/xingrz/swiftz-protocal)  