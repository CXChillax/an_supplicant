#Bugreport :lyq19961011@gmail.com
#-*-coding:utf-8-*-
import wx
import threading
import get
import packet
import sys
import socket
import struct
import time
import connect


class MyApp(wx.App):
    
    def OnInit(self):
       frame = MyFrame("supplicant", (500, 200), (500, 160))
       frame.SetMaxSize((500,160))
       frame.SetMinSize((500,160))
       frame.Show()
       self.SetTopWindow(frame)
       return True
    
class MyFrame(wx.Frame):
    
    def __init__(self, title, pos, size):

        self.threads = []
        self.getsession = []
        self.MAC=''
        self.IP=''
        wx.Frame.__init__(self, None, -1, title, pos, size)
        menuFile = wx.Menu()
        menuFile.Append(1, u"&关于...",u"关于本程序")
        menuFile.Append(3,u"&偏好设置",u"设置服务器IP")
        menuFile.AppendSeparator() 
        menuFile.Append(2,u"&Bug Report",u"报告长官，发现bug！")
        menuBar = wx.MenuBar()
        menuBar.Append(menuFile, u"&更多")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnAbout,id=1)
        self.Bind(wx.EVT_MENU,self.OnBugReport,id=2)
        hosts = self.Bind(wx.EVT_MENU,self.OnSet,id=3)
        self.CreateStatusBar() 
        
        self.SetStatusText(u"欢迎使用")
        
        panel = wx.Panel(self) 
        self.connect = wx.Button(panel,label=u"登录",pos=(240, 60),size=(80, 50)) 
        self.disconnect = wx.Button(panel,label=u"下线",pos=(330,60),size=(80,50))
        self.connect.Disable()
        self.disconnect.Disable()
        self.Bind(wx.EVT_BUTTON, self.OnDisconnect,self.disconnect)
        self.Bind(wx.EVT_BUTTON,self.OnConnect,self.connect)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)         
        wx.StaticText(panel, -1, u"用户名:", pos=(28, 40))
        self.username = wx.TextCtrl(panel, -1 ,pos=(80, 40))
        self.username.SetInsertionPoint(0)
        self.Bind(wx.EVT_TEXT,self.Onuser,self.username)
        wx.StaticText(panel,-1,u"密码:",pos=(242,40))
        self.pwd = wx.TextCtrl(panel, -1,pos=(280,40),style=wx.TE_PASSWORD |wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_TEXT,self.Onpwd,self.pwd)
        wx.CheckBox(panel, -1, u"自动登录", (20, 80), (150, 20))
        wx.CheckBox(panel, -1, u"保存密码", (110, 80), (150, 20))
        

   
        
    
    def OnConnect(self,event):
        Username = self.username.GetValue()
        Password = self.pwd.GetValue()
        mac = get.get_mac_address()
        self.MAC=mac
        ip = get.Get_local_ip()
        self.IP=ip
        upnet_net = packet.generate_upnet(mac, ip, Username, Password)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        hosts = '210.45.194.10'
        status,message= connect.upnet(sock, upnet_net, hosts,self.getsession)
        if status == 0:
            msgbox = wx.MessageDialog(None, "",message,wx.OK)
            msgbox.ShowModal()
            frame=MainFrame()
            frame.Show()
        else:
            self.connect.Disable()
            self.disconnect.Enable()
            self.username.SetEditable(False)
            self.pwd.SetEditable(False)
            wx.MessageBox(u'呼吸线程开启',message)
            self.SetStatusText(u"认证成功")
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
        msgbox = wx.MessageDialog(None, "",u'确定要下线吗？',wx.YES_NO | wx.ICON_QUESTION)
        ret = msgbox.ShowModal()
        if (ret == wx.ID_YES):
            self.StopThreads()
            wx.MessageBox( u"程序即将退出",u'\n下线了，呼吸线程关闭')
            sys.exit()
            

     
    def OnAbout(self, event):
        wx.MessageBox(u"程序属于测试阶段\n仅用于学习，禁止用来hack，以及损害他人利益",u"关于", wx.OK | wx.ICON_INFORMATION, self) 

    def OnBugReport(self,event):
        wx.MessageBox("Gmail:lyq19961011@gmail.com",u"欢迎提交bug",wx.OK | wx.ICON_INFORMATION,self)



    def OnCloseWindow(self, event):
        msgbox = wx.MessageDialog(None, u"如果你当前在线的话，退出将会导致下线",u'确定关闭窗口吗？',wx.YES_NO | wx.ICON_QUESTION)
        ret = msgbox.ShowModal()
        if (ret == wx.ID_YES):
            self.StopThreads()
            time.sleep(0.5)
            sys.exit()
        

    def OnSet(self,event):
        windows=wx.TextEntryDialog(None, "host",u'偏好设置', '210.45.194.10')
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
        self.countdown = wx.StaticText(self, label=u"请在6s后重试",pos=(178,60))

class MainFrame(wx.Frame):


    def __init__(self):
        wx.Frame.__init__(self, None, title=u"上线失败",pos=(545,200),size=(420,150))
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
            msg = u"%ss后重试" % self.time2die
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
        self.hosts='210.45.194.10'
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.threadNum = 1
        self.timeToQuit = threading.Event()
        self.timeToQuit.clear()
        self.messageDelay = 30
        
    def stop(self):
        downnet = packet.generate_downnet(self.mac,self.ip,self.session,self.index)
        connect.downnet(self.sock, downnet,self.hosts)
        self.timeToQuit.set()
    
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
                    self.sock.close()
                    wx.MessageBox(u"保持在线失败！程序即将退出",u"错误!!",wx.OK | wx.ICON_INFORMATION,self)
                    sys.exit()
                    break
                else:
                    self.index += 3
                    self.timeToQuit.wait(self.messageDelay) 
            
        
def main():
    app = MyApp()
    app.MainLoop()
    
if __name__ == '__main__':
    main()
    
