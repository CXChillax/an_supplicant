#Tools  
如果你用我的supplicant不能认证，那么先抓windows下的udp报文，比如分析upnet包就就把上线hex data放在对应的程序的空list里，会相应的解密。  
downnet、breathe、message、等也一样。


解密算法用的是crpyt3848：  
将username、password、等每一个字符转换为acsii对应的数字，放在list里，在通过crpty3848加密。如果加密之后的报文和win下不一致，那就是加密算法不一样。  
通常用crpyt3848模拟与windows下udp报文是否一致，若一致，那必定是可以上线的。  

