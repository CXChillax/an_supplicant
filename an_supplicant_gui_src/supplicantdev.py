# Bugreport :lyq19961011@gmail.com
#-*-coding:utf-8-*-
'''
Main function
'''
import wx
import sys
import threading
import socket
import struct
import time
import struct
from func import config_r_w
from func import get_ip_mac
from func import creat_bytes
from func import en_de_crypt_func
from func import connect_func


class MainApp(wx.App):

    def OnInit(self):
        frame = SupplicantFrame("supplicant", (500, 200), (260, 350))
        frame.SetMaxSize((260, 350))
        frame.SetMinSize((260, 350))
        frame.Center()
        frame.Show()
        #self.icon = wx.Icon('swiftz.icon', wx.BITMAP_TYPE_ICO)
        # self.SetIcon(self.icon)
        self.SetTopWindow(frame)
        return True


class SupplicantFrame(wx.Frame):

    def __init__(self, title, pos, size):
        self.updateconf()
        self.threads = []
        self.getsession = []
        self.MAC = ''
        self.IP = ''
        wx.Frame.__init__(self, None, -1, title, pos, size)
        menuFile = wx.Menu()
        menuFile.Append(1, u"&关于...", u"关于本程序")
        menuFile.Append(3, u"&偏好设置", u"偏好设置")
        menuFile.AppendSeparator()
        menuFile.Append(2, u"&Bug Report", u"！！")
        menuBar = wx.MenuBar()
        menuBar.Append(menuFile, u"&更多")
        menuBar.Disable()
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=1)
        self.Bind(wx.EVT_MENU, self.OnBugReport, id=2)
        self.Bind(wx.EVT_MENU, self.OnSet, id=3)
        self.CreateStatusBar()
        self.SetStatusText(u"欢迎使用")
        panel = wx.Panel(self)
        self.connect = wx.Button(
            panel, label=u"登录", pos=(38, 196), size=(80, 25))
        self.disconnect = wx.Button(
            panel, label=u"下线", pos=(122, 196), size=(80, 25))
        self.connect.Disable()
        self.disconnect.Disable()
        self.Bind(wx.EVT_BUTTON, self.OnDisconnect, self.disconnect)
        self.Bind(wx.EVT_BUTTON, self.OnConnect, self.connect)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        wx.StaticText(panel, -1, u"用户名:", pos=(38, 51))
        self.username = wx.TextCtrl(panel, -1, self.u, pos=(90, 50))
        self.username.SetInsertionPoint(0)
        self.Bind(wx.EVT_TEXT, self.Onuser, self.username)
        wx.StaticText(panel, -1, u"密码:", pos=(38, 91))
        #self.setting = wx.Button(panel,label=u"设置",pos=(232, 106),size=(80, 25))
        #self.Bind(wx.EVT_BUTTON, self.OnSet,self.setting)
        #self.About = wx.Button(panel,label=u"关于",pos=(316, 106),size=(80, 25))
        #self.Bind(wx.EVT_BUTTON, self.OnAbout,self.About)
        #wx.CheckBox(panel, -1, u"自动登录", (58, 70), (150, 20))
        self.sp = wx.CheckBox(panel, -1, u"保存密码", (38, 120), (150, 20))
        if self.savepass == "1":
            self.sp.SetValue(1)
            self.pwd = wx.TextCtrl(
                panel, -1, self.p, pos=(90, 90), style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)
        else:
            self.sp.SetValue(0)
            self.p = ''
            self.pwd = wx.TextCtrl(
                panel, -1, self.p, pos=(90, 90), style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_TEXT, self.Onpwd, self.pwd)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, self.sp)
        self._EnableOrDisableOkBtn()

    def EvtCheckBox(self, event):
        if self.sp.IsChecked():
            config_r_w.confwritesp('1')
        else:
            config_r_w.confwritesp('0')

    def updateconf(self):
        self.a = config_r_w.confread()
        self.u = self.a[0]
        self.p = self.a[1]
        self.p = en_de_crypt_func.decoding_pass(self.p)
        self.host = self.a[2]
        self.ver = self.a[3]
        self.ser = self.a[4]
        self.savepass = self.a[5]

    def OnConnect(self, event):
        self.updateconf()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        Username = self.u
        Password = self.pwd.GetValue()
        mac = get_ip_mac.get_mac_address()
        self.MAC = mac
        ip = get_ip_mac.Get_local_ip()
        self.IP = ip
        service = self.ser
        version = self.ver
        upnet_net = creat_bytes.generate_upnet_packet(
            self.MAC, self.IP, Username, Password, service, version)
        hosts = self.host
        status, message = connect_func.upnet(
            sock, upnet_net, hosts, self.getsession)
        if status == 0:
            self.getsession = []
            sock.close
            msgbox = wx.MessageBox(message)
            # frame=ErrorFrame()
            # frame.Show()
        else:
            self.connect.Disable()
            # self.setting.Disable()
            self.disconnect.Enable()
            self.username.SetEditable(False)
            self.pwd.SetEditable(False)
            self.SetStatusText(u"认证成功")
            self.OnStartThread()
            wx.MessageBox(message)

    def Onuser(self, event):
        self._EnableOrDisableOkBtn()

    def Onpwd(self, event):
        self._EnableOrDisableOkBtn()

    def LogMessage(self, msg):
        wx.MessageBox(msg)
        self.SetStatusText(u'保持在线失败')

    def _EnableOrDisableOkBtn(self):
        self.Bind(wx.EVT_TEXT_ENTER, self.Onnone, self.pwd)
        self.connect.Disable()
        usrStr = self.username.GetValue()
        pwdStr = self.pwd.GetValue()
        pwdStr = en_de_crypt_func.encoding_pass(pwdStr)
        config_r_w.confwriteu(usrStr)
        config_r_w.confwritep(pwdStr)
        self.sp.Disable()
        self.updateconf()
        if not usrStr == '' and not pwdStr == '':
            self.connect.Enable()
            self.Bind(wx.EVT_TEXT_ENTER, self.OnConnect, self.pwd)
            self.sp.Enable()

    def Onnone(self, event):
        return True

    def OnDisconnect(self, event):
        msgbox = wx.MessageDialog(
            None, u'确定下线吗？', u"!", wx.YES_NO | wx.ICON_QUESTION)
        ret = msgbox.ShowModal()
        if (ret == wx.ID_YES):
            self.username.SetEditable(True)
            self.pwd.SetEditable(True)
            self.StopThreads()

            self.SetStatusText(u"已下线！")
            #wx.MessageBox( u"程序即将退出",u'下线了，呼吸线程关闭')
            # sys.exit()

    def OnAbout(self, event):
        wx.MessageBox(u"test~", u"关于", wx.OK | wx.ICON_INFORMATION, self)

    def OnBugReport(self, event):
        wx.MessageBox("Gmail:lyq19961011@gmail.com", u"欢迎提交bug",
                      wx.OK | wx.ICON_INFORMATION, self)

    def OnCloseWindow(self, event):
        msgbox = wx.MessageDialog(
            None, u"如果你当前在线的话，退出将会导致下线", u'确定关闭窗口吗？', wx.YES_NO | wx.ICON_QUESTION)
        ret = msgbox.ShowModal()
        if (ret == wx.ID_YES):
            while self.threads:
                self.StopThreads()
                if self.p == '':
                    config_r_w.confwritesp('0')
                time.sleep(0.5)
                sys.exit()
            if self.p == '':
                config_r_w.confwritesp('0')
            sys.exit()

    def OnSet(self, event):
        self.updateconf()
        windows = TextEntryDialog(
            None, u'偏好设置', u'服务器IP', u'客户端版本号', u'设置服务类型(int or internet)')
        windows.SetValue(self.host, self.ver, self.ser)
        windows.Show()
        windows.Center()
        if windows.ShowModal() == wx.ID_OK:
            response1 = windows.GetValue1()
            response2 = windows.GetValue2()
            response3 = windows.GetValue3()
            config_r_w.confwriteh(response1)
            config_r_w.confwritev(response2)
            config_r_w.confwrites(response3)
        else:
            windows.Destroy()
            self.updateconf()
        windows.Destroy()
        self.updateconf()

    def OnStartThread(self):
        thread = WorkerThread(
            self.MAC, self.IP, self.host, self.getsession, self)
        self.threads.append(thread)
        thread.start()

    def StopThreads(self):
        while self.threads:
            thread = self.threads[0]
            thread.stop()
            self.threads.remove(thread)
            self.connect.Enable()
            # self.setting.Enable()
            self.disconnect.Disable()
            self.getsession = []


class TextEntryDialog(wx.Dialog):

    def __init__(self, parent, title, caption, caption2, caption3):
        style = wx.DEFAULT_DIALOG_STYLE
        super(TextEntryDialog, self).__init__(
            parent, -1, title, style=style, pos=(620, 180))

        text = wx.StaticText(self, -1, caption)
        input = wx.TextCtrl(self, -1)
        input.SetInitialSize((100, 20))

        text2 = wx.StaticText(self, -1, caption2)
        input2 = wx.TextCtrl(self, -1)
        input2.SetInitialSize((70, 20))

        text3 = wx.StaticText(self, -1, caption3)
        input3 = wx.TextCtrl(self, -1)
        input3.SetInitialSize((70, 20))

        buttons = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text, 0, wx.ALL, 5)
        sizer.Add(input, 1, wx.ALL, 5)
        sizer.Add(text2, 0, wx.ALL, 5)
        sizer.Add(input2, 1, wx.ALL, 5)
        sizer.Add(text3, 0, wx.ALL, 5)
        sizer.Add(input3, 1, wx.ALL, 5)
        sizer.Add(buttons, 0, wx.ALL, 5)
        self.SetSizerAndFit(sizer)
        self.input = input
        self.input2 = input2
        self.input3 = input3

    def SetValue(self, value1, value2, value3):
        self.input.SetValue(value1)
        self.input2.SetValue(value2)
        self.input3.SetValue(value3)

    def GetValue1(self):
        return self.input.GetValue()

    def GetValue2(self):
        return self.input2.GetValue()

    def GetValue3(self):
        return self.input3.GetValue()


class PanelOne(wx.Panel):

    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)

        self.countdown = wx.StaticText(self, label=u"请在6s后重试", pos=(178, 60))


class ErrorFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, title=u"上线失败",
                          pos=(520, 200), size=(420, 150))
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
            msg = u"请在%ss后重试" % self.time2die
            self.panelOne.countdown.SetLabel(msg)
        else:
            self.Close()
            self.Layout()
            self.timer.Stop()
        self.time2die -= 1


class WorkerThread(threading.Thread):

    def __init__(self, mac, ip, host, session, window):
        threading.Thread.__init__(self)
        self.session = session
        self.index = 0x01000000
        self.mac = mac
        self.ip = ip
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.window = window
        self.hosts = host
        self.threadNum = 1
        self.timeToQuit = threading.Event()
        self.timeToQuit.clear()
        self.messageDelay = 30

    def stop(self):
        downnet = packet.generate_downnet(
            self.mac, self.ip, self.session, self.index)
        connect_func.downnet(self.sock, downnet, self.hosts)
        self.timeToQuit.set()
        self.index = 0x01000000

    def run(self):
        self.timeToQuit.wait(0)
        # print self.session
        while True:
            # print self.index
            if self.timeToQuit.isSet():
                self.sock.close()
                break
            else:
                breathe = creat_bytes.generate_breathe(
                    self.mac, self.ip, self.session, self.index)
                status = creat_bytes.breathe(self.sock, breathe, self.hosts)
                # print status
                if status == 0:
                    stat = u'保持在线状态失败'
                    wx.CallAfter(self.window.LogMessage, stat)
                    wx.CallAfter(self.window.StopThreads)
                    self.timeToQuit.wait(3)
                    # self.sock.close()
                    #wx.MessageBox(u"保持在线失败！程序即将退出",u"错误!!",wx.OK | wx.ICON_INFORMATION,self)
                    # self.stop()
                else:
                    #stat = u'成功'
                    # print self.index
                    self.index += 3
                    # wx.CallAfter(self.window.LogMessage,stat)
                    #wx.MessageBox(u"OK",u"OK!!",wx.OK | wx.ICON_INFORMATION,self)
                    self.timeToQuit.wait(self.messageDelay)


def main():
    app = MainApp()
    app.MainLoop()


if __name__ == '__main__':
    main()
