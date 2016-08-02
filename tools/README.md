#从主code里分离出来的  
如果你用我的supplicant不能认证，那么先抓windows下的udp报文，通常是16进制data，比如分析upnet包就就把上线16进制data放在对应的程序的空list里，会相应的解密。  
downnet、breathe、message、等也是一样等道理。


解密算法用的是crpyt3848：  
将username、password、等转换为acsii对应数字，放在list里，在通过crpty3848加密。如果不能加密之后的报文和win下不一致，可能是加密算法不一样。  
通常用crpyt3848模拟与windows下报文是否一致，若一致，那必定是可以上线的。  

