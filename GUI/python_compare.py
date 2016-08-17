#encoding: utf-8
import wx
from wx.py.shell import ShellFrame
from wx.py.filling import FillingFrame
import get
import encrypt
import packet
import sys
import socket
import struct
import urllib2
import time

class MyApp(wx.App):
    
    def OnInit(self):
       frame = MyFrame("Test", (500, 200), (450, 160))
       frame.Show()
       self.SetTopWindow(frame) #set top windows,a app only have one top windows
       return True
    
class MyFrame(wx.Frame):
    
    def __init__(self, title, pos, size):
        wx.Frame.__init__(self, None, -1, title, pos, size)
        menuFile = wx.Menu()
        menuFile.Append(1, "&使用说明...","程序使用说明以及注意事项")
        menuFile.Append(3,"&偏好设置","设置host")
        menuFile.AppendSeparator() #在about和exit之间创建一个分割线
        menuFile.Append(2,"&Bug Report","报告长官！发现Bug")
        
        menuFile2 = wx.Menu()
        menuFile2.Append(4,"&Python Shell","Open Python Shell frame")
        menuFile2.Append(5,"&Namespace Viewer","Open namespace viewer frame")
        menuBar = wx.MenuBar()
        menuBar.Append(menuFile, "&更多")
        menuBar.Append(menuFile2,"&Debug")
        self.SetMenuBar(menuBar) #设置MenueBar and about python
        
        self.Bind(wx.EVT_MENU, self.OnAbout,id=1)
        self.Bind(wx.EVT_MENU,self.OnBugReport,id=2)
        hosts = self.Bind(wx.EVT_MENU,self.OnInit,id=3)
        self.Bind(wx.EVT_MENU,self.OnShell,id=4)
        self.Bind(wx.EVT_MENU,self.OnFilling,id=5)
        self.CreateStatusBar() 
        
        self.SetStatusText("欢迎使用") #creat a StatusText and put text into 
        
        panel = wx.Panel(self) #redef panel
        self.connect = wx.Button(panel,label="登录",pos=(240, 60),size=(50, 50))#creat a button with position size
        self.disconnect = wx.Button(panel,label="下线",pos=(300,60),size=(50,50))#creat another button
        self.connect.Disable()
        
        self.Bind(wx.EVT_BUTTON, self.OnDisconnect,self.disconnect)   #button even close
        self.Bind(wx.EVT_BUTTON,self.OnConnect,self.connect)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)  #even close even
        
        wx.StaticText(panel, -1, "用户名:", pos=(20, 40))
        self.username = wx.TextCtrl(panel, -1 ,pos=(80, 40))
        self.username.SetInsertionPoint(0)
        self.Bind(wx.EVT_TEXT,self.Onuser,self.username)
        wx.StaticText(panel,-1,"密码:",pos=(210,40))
        self.pwd = wx.TextCtrl(panel, -1,pos=(250,40),style=wx.TE_PASSWORD)
        self.Bind(wx.EVT_TEXT,self.Onpwd,self.pwd)
        
        
        wx.CheckBox(panel, -1, "自动登录", (20, 80), (150, 20))
        wx.CheckBox(panel, -1, "保存密码", (100, 80), (150, 20))
    
    def OnInit(self,event):
        windows=wx.TextEntryDialog(None, "通常情况下不需要更改服务器host",'偏好设置', '210.45.194.10')
        windows.Show()
        if windows.ShowModal() == wx.ID_OK:
            response = windows.GetValue()
        else:
            response = windows.GetValue()
            print response
        windows.Destroy()
        
    
    def OnConnect(self,event):
            Username=self.username.GetValue()
            Password=self.pwd.GetValue()
            mac=get.get_mac_address()
            ip=get.Get_local_ip()
            upnet_net= packet.generate_upnet(mac, ip, Username, Password)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            hosts='210.45.194.18'
            sock.sendto(upnet_net, (hosts, 3848))
            upnet_ret = sock.recv(3848)
            upnet_ret = [i for i in struct.unpack('B' * len(upnet_ret), upnet_ret)]
            encrypt.decrypt(upnet_ret)
            status2 = upnet_ret[20]
            session_len = upnet_ret[22]
            session = upnet_ret[23:session_len + 23]
            message_len = upnet_ret[upnet_ret.index(11,35)+1]
            message = upnet_ret[upnet_ret.index(11,35)+2:message_len+upnet_ret.index(11,35)+2]
            message = ''.join([struct.pack('B', i) for i in message]).decode('gbk')
            if status2==0:
                wx.MessageBox(message,'认证不成功,请稍后再尝试')
                sock.close()
            else:
                wx.MessageBox(message)
                index = 0x01000000
                sock.settimeout(10) 
                while True:
                    breathe_packet = packet.generate_breathe(mac, ip, session, index)
                    sock.sendto(breathe_packet,(hosts,3848))
                    try:
                        breathe_ret = sock.recv(3848)
                    except socket.timeout:
                        wx.MessageBox('连接不顺畅')
                        sock.close()
                        continue
                    else:
                        status = struct.unpack('B' * len(breathe_ret), breathe_ret)
                        if status[20] == 0:
                            sock.close()
                            sys.exit()
                        time.sleep(30)
                        index += 3
                        print index
    
    def Onuser(self,event):  
        self._EnableOrDisableOkBtn()  
                  
    def Onpwd(self,event):  
        self._EnableOrDisableOkBtn()  
      
    def _EnableOrDisableOkBtn(self):  
        self.connect.Disable()  
        usrStr = self.username.GetValue()  
        pwdStr = self.pwd.GetValue()  
        if not usrStr=='' and not pwdStr=='':  
            self.connect.Enable()                    
    
    def OnDisconnect(self, event):
        msgbox = wx.MessageDialog(None, "",'你确定要下线吗？',wx.YES_NO | wx.ICON_QUESTION)
        ret = msgbox.ShowModal()
        if (ret == wx.ID_YES):
            self.Close()
         
    def OnAbout(self, event):
        wx.MessageBox("个人项目，仅用于学习与交流，严禁用于hack。\n作者不负任何责任", 
                "关于", wx.OK | wx.ICON_INFORMATION, self) 
    
    def OnBugReport(self,event):
        wx.MessageBox("Gmail:lyq19961011@gmail.com","欢迎提交Bug",wx.OK | wx.ICON_INFORMATION,self)
    
    def OnShell(self, event):
        frame = ShellFrame(parent=self)
        frame.Show()

    def OnFilling(self, event):
        frame = FillingFrame(parent=self)
        frame.Show()

    def OnCloseWindow(self, event):
        self.Destroy()
    
    
        
    
if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()
