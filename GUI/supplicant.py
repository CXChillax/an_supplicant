#encoding: utf-8
import wx
import threading
from wx.py.shell import ShellFrame
from wx.py.filling import FillingFrame
import get
import packet
import sys
import socket
import struct
import time
import connect

class MyApp(wx.App):
    
    def OnInit(self):
       frame = MyFrame("Test", (500, 200), (500, 160))
       frame.Show()
       self.SetTopWindow(frame) #set top windows,a app only have one top windows
       return True
    
class MyFrame(wx.Frame):
    
    def __init__(self, title, pos, size):

        self.threads = []
        self.getsession = []
        self.MAC=''
        self.IP=''
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
        hosts = self.Bind(wx.EVT_MENU,self.OnSet,id=3)
        self.Bind(wx.EVT_MENU,self.OnShell,id=4)
        self.Bind(wx.EVT_MENU,self.OnFilling,id=5)
        self.CreateStatusBar() 
        
        self.SetStatusText("欢迎使用") #creat a StatusText and put text into 
        
        panel = wx.Panel(self) #redef panel
        self.connect = wx.Button(panel,label="登录",pos=(240, 60),size=(50, 50))#creat a button with position size
        self.disconnect = wx.Button(panel,label="下线",pos=(300,60),size=(50,50))#creat another button
        self.connect.Disable()
        self.disconnect.Disable()
        self.Bind(wx.EVT_BUTTON, self.OnDisconnect,self.disconnect)   #bind button to even close
        self.Bind(wx.EVT_BUTTON,self.OnConnect,self.connect)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)  #bind even close even
        
        wx.StaticText(panel, -1, "用户名:", pos=(20, 40))
        self.username = wx.TextCtrl(panel, -1 ,pos=(80, 40))
        self.username.SetInsertionPoint(0)
        self.Bind(wx.EVT_TEXT,self.Onuser,self.username)
        wx.StaticText(panel,-1,"密码:",pos=(210,40))
        self.pwd = wx.TextCtrl(panel, -1,pos=(250,40),style=wx.TE_PASSWORD |wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_TEXT,self.Onpwd,self.pwd)
 
        
        
        wx.CheckBox(panel, -1, "自动登录", (20, 80), (150, 20))
        wx.CheckBox(panel, -1, "保存密码", (100, 80), (150, 20))
        

   
        
    
    def OnConnect(self,event):
        Username = self.username.GetValue()
        Password = self.pwd.GetValue()
        mac = get.get_mac_address()
        self.MAC=mac
        ip = get.Get_local_ip()
        self.IP=ip
        upnet_net = packet.generate_upnet(mac, ip, Username, Password)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        hosts = '210.45.194.18'
        status,message= connect.upnet(sock, upnet_net, hosts,self.getsession)
        if status == 0:
            msgbox = wx.MessageDialog(None, "",message,wx.OK)
            msgbox.ShowModal()
            frame=MainFrame()
            frame.Show()
        else:
            self.connect.Disable()
            self.disconnect.Enable()
            wx.MessageBox('呼吸线程开启',message)
            self.SetStatusText("认证成功")
            self.OnStartThread()
            

    
    def Onuser(self,event):
        self._EnableOrDisableOkBtn()  
              
    def Onpwd(self,event):
        self._EnableOrDisableOkBtn()  
  
    def _EnableOrDisableOkBtn(self):
        self.Bind(wx.EVT_TEXT_ENTER,self.Onnone,self.pwd)
        self.connect.Disable()
        usrStr = self.username.GetValue()
        pwdStr = self.pwd.GetValue()
        if not usrStr=='' and not pwdStr=='':
            self.connect.Enable()
            self.Bind(wx.EVT_TEXT_ENTER,self.OnConnect,self.pwd)                    
    
    def Onnone(self,event):
        return True
    
    def OnDisconnect(self, event):
        msgbox = wx.MessageDialog(None, "",'你确定要下线吗？',wx.YES_NO | wx.ICON_QUESTION)
        ret = msgbox.ShowModal()
        if (ret == wx.ID_YES):
            self.StopThreads()
            wx.MessageBox( "程序即将退出",'\n下线了，呼吸线程关闭')
            sys.exit()
            

     
    def OnAbout(self, event):
        wx.MessageBox("个人项目，仅用于学习与交流，严禁用于hack。\n作者不负任何责任","关于", wx.OK | wx.ICON_INFORMATION, self) 

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

    def OnSet(self,event):
        windows=wx.TextEntryDialog(None, "通常情况下不需要更改认证host",'偏好设置', '210.45.194.10')
        windows.Show()
        if windows.ShowModal() == wx.ID_OK:
            response = windows.GetValue()
        else:
            response = windows.GetValue()
        windows.Destroy()
    
    def OnStartThread(self):
        thread = WorkerThread(self.MAC, self.IP, self.getsession, self)
        self.threads.append(thread)
        thread.start()

    
    def StopThreads(self):
        while self.threads:
            thread = self.threads[0]
            thread.stop()
            self.threads.remove(thread)
    


class PanelOne(wx.Panel):


    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.countdown = wx.StaticText(self, label="请在6秒后重试",pos=(160,60))

class MainFrame(wx.Frame):


    def __init__(self):
        wx.Frame.__init__(self, None, title="连接不成功",pos=(545,200),size=(420,150))
        self.panelOne = PanelOne(self)
        self.time2die = 5
  
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(1000)
  
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panelOne, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
  
    def update(self, event):
        
        if self.time2die > 0:
            msg = "请在%s秒后重试" % self.time2die
            self.panelOne.countdown.SetLabel(msg)
        else:
            self.Close()
            self.Layout()
            self.timer.Stop()
        self.time2die -= 1


class WorkerThread(threading.Thread):
    
    def __init__(self, mac, ip, session, window):
        threading.Thread.__init__(self)
        self.session=session
        self.index=0x01000000
        self.mac=mac
        self.ip=ip
        self.window=window
        self.hosts='210.45.194.18'
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.threadNum = 1
        self.timeToQuit = threading.Event()
        self.timeToQuit.clear()
        self.messageDelay = 30
        
    def stop(self):
        downnet = packet.generate_downnet(self.mac,self.ip,self.session,self.index)
        connect.downnet(self.sock, downnet,self.hosts)
        self.timeToQuit.set()
        self.sock.close()
    
    def run(self):
         self.timeToQuit.wait(10)
         while True:
            if self.timeToQuit.isSet():
                self.sock.close()
                break
            else:
                breathe = packet.generate_breathe(self.mac, self.ip, self.session, self.index)
                status = connect.breathe(self.sock, breathe, self.hosts)
                if status == 0:
                    break
                else:
                    self.index += 3
                    self.timeToQuit.wait(self.messageDelay) 
            
        

if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()
