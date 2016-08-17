# 关于supplicant.py
基于Python的安腾小蝴蝶的全平台认证脚本，理论上可在windows、linux、osx、android、ios等可以安装python运行环境的系统下跑起。但目前属于测试阶段，可能会出现意想不到的错误，如果出错了，请告诉我：lyq19961011@gmail.com。  

# AHNU用户：
方案：内网认证使用mentohust，外网用本python脚本。已在linux，windows下测试通过。
目前可视化界面还没有做完，只有osx有可视化的内网认证界面。它不利于全平台的移植。

此项目可能下步会推出osx下的可视化界面，方便用户使用。但是linux，和安卓，脚本交互就已经很友好了，可能永远都不会有可视化界面。

# 其他学校的用户：
如果你们学校校园网是蝴蝶，那么你完全可以用这个脚本去登录校园网,某些情况可能需要修改code，如果登录过程中出现错误，请你告诉我，我会去解决。

# 已知bug：
 1、you tell me

## release 0.1.x在osx、windows、linux下测试通过。  
release 0.2.x是每次手动输入用户名和密码的，安全性较高...防止有人打开.py文件偷看你密码，是吧。。已在windows、osx、linux测试通过。
  
  关于我为什么要搞这两个版本：是为了脚本能方便的在Openwrt等等的第三方路由器系统跑起来。

##测试环境
* OS X、windows、linux、(android、Openwrt暂未测试)
* Python 2.7.x


##0.1版 使用前的配置  
使用前请配置Python2.7.x，对于一些自带Python3.5的linux发行版本用户请自行配置2.7，否则会报错。  
在程序打开前必须先打开.py文件进行用户名，密码的填写。  

Mac用户推荐使用coderunner打开下载的py文件  

windows用户推荐使用Notepad＋＋打开下载的py文件  

安卓在使用前请下载运行python2.7.x的软件，安卓目前正在测试中，服务器返回的packet解包报错。gbk编码问题，正在完善。


username = '' #在这里填上你的用户名

password = '' #在这里填上你的密码


##0.1版 运行步骤:  
注意：在你运行之前，请确保上一步的配置参数都已填写正确  
上线：  
Mac用户：打开终端，把py文件拖到终端里，回车。

Linux用户：下载python运行环境，随后步骤同Mac。

windows用户：下载python运行环境并配置正确。windows＋r，输入cmd，回车，把脚本拖入cmd，回车。或者双击.py文件。    

下线：  
输入ctrl＋C

##一些注意事项  
使用时请看好你的网卡mac地址和程序显示的是否一致，以及ip是否是当前网卡上的。  

如果终端显示permission deined：输入 chmod 755 .py文件拖进去，回车即可

##0.2版 运行步骤:  
和0.1一样，拖进去就行了...但使用前什么都不用改

##future release demo:  
安装wx框架，GUI测试版，跑起来了。  

