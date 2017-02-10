#关于supplicant.py  
安腾小蝴蝶的全平台认证脚本，以及图形用户界面版本  

##测试环境:
* OS X、windows、linux、android、Open-wrt(需要python运行环境，/overlay需要8m以上可用空间)
* Python 2.7.x   
* `图形用户界面版本`不需要Python运行环境

##AHNU用户：
Linux登录校园网方案：  
内网认证使用mentohust，外网用这个python脚本。  

##其他学校的用户：   
已知测试通过的院校:  
  
* 烟台大学赛尔网
* 广州商学院  

#图形用户界面版本:     
安装之后双击exe即可 :)  
Windows版安装包下载地址：[这里](https://github.com/lyq1996/supplicant/releases/download/GUI_test/Personal.exe) 
##特性：
* 无限制共享  
* 比官方蝴蝶快N倍  

##不完善的地方：  
* 需要手动输入服务器IP。     
* You tell me....  

#使用前的配置:  
请配置`Python2.7.x`。

##运行步骤:  
注意：  
在你运行之前，请确保`配置参数`都已填写正确。  
上线：  
```
$ python an_supplicant.py  
```   

下线： 
``` 
Ctrl＋C
```
##一些注意事项:   

如果终端显示permission deined：  
```
$ sudo chmod 755 .py
```  

##参考&鸣谢:  
> [benchmade](https://github.com/gnehsoah/benchmade)  
> [swiftz-protocal](https://github.com/xingrz/swiftz-protocal)  