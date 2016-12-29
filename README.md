#关于supplicant.py
项目主页：https://github.com/lyq1996/supplicant  
基于Python的安腾小蝴蝶的全平台认证脚本，以及用户界面版本  

##测试环境
* OS X、windows、linux、android、(Open-wrt以测试，需要python运行环境，/overlay需要8m以上可用空间)
* Python 2.7.x

# AHNU用户：
Linux登录校园网方案：内网认证使用mentohust，外网用本python脚本。已在linux，windows，os x下测试通过。


# 其他学校的用户：
如果你们学校校园网是蝴蝶，那么你完全可以用这个脚本去登录校园网，多试试参数。

##GUI version:  
需要安装wxpython模块，GUI界面测试版。  


mac在打包前需要安装好py2app。  
打包命令：  
cd /GUI  
py2applet --make-setup supplicant.py
python setup.py py2app  


特性：
*无限制共享  
*比官方蝴蝶快N倍  

不完善的地方：  
1、需要手动输入服务器IP。     
2、You tell me....

Windows版安装包下载地址：https://github.com/lyq1996/supplicant/releases/download/GUI_test/Personal.exe  
  

##使用前的配置  
使用前请配置Python2.7.x，对于一些自带Python3.5的linux发行版本用户请自行配置2.7。  
在程序打开前必须先打开.py文件进行用户名，密码等参数的填写。（具体看注释）  

安卓在使用前下载Qpython。


##运行步骤:  
注意：在你运行之前，请确保上一步的配置参数都已填写正确  
上线：  
Mac用户：打开终端，把py文件拖到终端里运行。

Linux用户：下载python运行环境，随后步骤同Mac。

windows用户：下载python运行环境并配置正确，拖入cmd中。  

下线：  
Ctrl＋C

##一些注意事项  
使用时请看好你的物理网卡mac地址，以及ip是否是当前网卡上的。  

如果终端显示permission deined：请chmod 755 .py文件拖进去，回车即可。  

##吐槽：  
一个学硬件的大学狗，  
从没接触过用户界面开发..  
写这些东西好苦啊..   
以后还是滚回去搞搞电源搞搞单片机吧。  
