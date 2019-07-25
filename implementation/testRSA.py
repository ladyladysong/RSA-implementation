# -*- coding: utf-8 -*- 
#!/usr/bin/env python


import sys
reload(sys)
sys.setdefaultencoding('utf8')


import wx
import wx.py.images
import os
import subprocess
import RSA

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,parent=None, title = 'Cryptology Experiment', 
            size=(500,450),style= wx.CAPTION |wx.MINIMIZE_BOX|wx.RESIZE_BORDER |wx.CLOSE_BOX | wx.CLIP_CHILDREN)

        #状态栏和工具栏
        self.panelNum = 1
        self.statusBar = self.CreateStatusBar()
        #将状态栏分割为3个区域,比例为1:2:3
        self.statusBar.SetFieldsCount(3)
        self.statusBar.SetStatusWidths([-6, -10, -2])

        self.toolbar = self.CreateToolBar()#增加一个工具
        home_image = wx.Image('Home.png')
        home_image = home_image.Scale(32,32).ConvertToBitmap() # 只有Image可以缩小，r缩小后再转回位图
        tool_home = self.toolbar.AddSimpleTool(wx.NewId(), home_image,'Home',"Return to the Home Page.",1)
        self.Bind(wx.EVT_TOOL, self.Home, tool_home)
        self.toolbar.Realize()
        
        self.ShowPanel1() 
        
        self.Show(True)
        self.Center()


    def ShowPanel1(self):
        # 面板一 

        self.panel1 = wx.Panel(self, pos=(0,0),size=(500,450))
        
        # rsa ds 选项
        button_rsa = wx.Button(self.panel1,-1,'RSA',pos=(25,50),size = (120,35)) # RSA 按钮
        L1 = wx.StaticText(self.panel1,-1,label = "The Rivest-Shamir-Adleman cryptosystem,\na cryptosystem for public-key encryption",pos=(180,50))
        button_ds = wx.Button(self.panel1,-1,'Digital Signature',pos=(25,170),size=(120,35)) # Digital Signature 按钮
        L2 = wx.StaticText(self.panel1,-1,label = "A digital signature is a mathematical scheme \nfor demonstrating the authenticity of a digital \nmessage or documents. A valid digital signat-\n-ure gives a recipient reason to believe that \nthe message was created by a known sender \n(authentication), that the sender cannot deny \nhaving sent the message (non-repudiation), \nand that the message was not altered in tran-\n-sit (integrity).",pos=(180,170))

        self.Bind(wx.EVT_BUTTON, self.click_RSA, button_rsa)
        self.Bind(wx.EVT_BUTTON, self.DigitalSignature, button_ds) 
        self.panel1.Bind(wx.EVT_MOTION,self.getPosition)




    def ShowPanel2(self):
        # 面板2
        #self.v_box2 = wx.wx.BoxSizer(wx.VERTICAL)
        self.statusBar.SetStatusText('', 1)#状态栏清空
        self.panel2 = wx.Panel(self,pos=(0,0),size=(500,450))
        # 文件输入
        #------------------
        self.filename_0 = ''
        L1 = wx.StaticText(self.panel2,-1,label = "Enter the file name:",pos=(25,5))
        self.filename_input = wx.TextCtrl(self.panel2,pos=(150,5),size=(230,-1),style=wx.TE_PROCESS_ENTER)
        button_browse = wx.Button(self.panel2,-1,'...',pos=(383,4),size = (37,27))
        L2 = wx.StaticText(self.panel2,-1,label = "Key:",pos=(113,45))
        self.key = wx.TextCtrl(self.panel2,pos=(150,45),size=(230,-1),style=wx.TE_PROCESS_ENTER)
        button_copyKey = wx.Button(self.panel2,-1,'Copy',pos=(383,44),size = (37,27))

        self.Bind(wx.EVT_BUTTON, self.OpenFile, button_browse) # '...'按钮
        self.Bind(wx.EVT_TEXT_ENTER, self.EnterFilename, self.filename_input)
        self.Bind(wx.EVT_BUTTON, self.copyKey, button_copyKey)
        file_select = wx.FileDialog(self.panel2,"browse","C:\Users\Dell\Desktop")
        # ------------------- 

        button_rsa_encrypt = wx.Button(self.panel2,-1,label='Encryption',pos=(80,90),size=(100,-1))
        button_rsa_decrypt = wx.Button(self.panel2,-1,label='Decryption',pos=(280,90),size=(100,-1))
        button_saveResult = wx.Button(self.panel2,-1,label='Save',pos=(415,310),size=(40,-1))
        text1 = wx.StaticText(self.panel2,-1,label='Result:',pos=(25,125))
        self.result = wx.TextCtrl(self.panel2,pos=(25,145),size = (430,160),style = wx.TE_MULTILINE)
        self.Bind(wx.EVT_BUTTON,self.rsa_encryption,button_rsa_encrypt)
        self.Bind(wx.EVT_BUTTON,self.rsa_decryption,button_rsa_decrypt)
        self.Bind(wx.EVT_BUTTON,self.saveResult,button_saveResult)

        self.panel2.Bind(wx.EVT_MOTION,self.getPosition)
        self.panel2.Show(True)


    def click_RSA(self,e):# 切换到RSA面板
        self.panel1.Destroy()
        self.panelNum = 2
        self.ShowPanel2()


    def rsa_encryption(self,e):
		if self.filename_0 != '':
			f = open(self.filename_0,'r')
			try:
				plain = f.read() # 读入明文
			finally:
				f.close()
			self.rsa = RSA.RSA()
			self.rsa.encrypt(plain)
			self.result.SetValue(self.rsa.cipher_string)
			self.key.SetValue(str(self.rsa.pri_key))
		else:
			self.statusBar.SetStatusText("No file.", 1)


    def rsa_decryption(self,e):
		if self.filename_0 != '':
			self.rsa.decrypt()
			self.result.SetValue(self.rsa.plain_string)
			self.key.SetValue(str(self.rsa.pri_key))
		else:
			self.statusBar.SetStatusText("No file.", 1)


    def DigitalSignature(self,e):
        print 'ds'

    def OpenFile(self,e):
        self.filename_input.Clear() # 假如打开"..."浏览，则清空前面键入的内容
        
        file_select = wx.FileDialog(self.panel2,"browse",defaultDir=os.getcwd(),
            defaultFile="",style=wx.OPEN|wx.CHANGE_DIR) # wx.MULTIPLE(reserve)  # 文件对话框
        if file_select.ShowModal()==wx.ID_OK:
            path = file_select.GetPath()
            self.filename_0 = path
            if self.filenameExamming(self.filename_0):
                self.filename_input.SetLabel(path)
        file_select.Destroy()

    def EnterFilename(self,e):
        self.filename_0 = e.GetString()
        self.filenameExamming(self.filename_0)


    def filenameExamming(self,string): # 检查文件是否txt文件 
        if not string.endswith('.txt') and not string.endswith('.TXT'):
            message1 = wx.MessageBox("This file is not a TXT file.",parent = self.panel2)
            self.statusBar.SetStatusText('Failed to load the file.', 1)
            return False
        else:
            self.statusBar.SetStatusText('Load the file correctly.', 1)
            return True

    def Home(self,e):
        if not self.panelNum == 1:
            self.panel2.Destroy()
            self.panelNum = 1
            self.ShowPanel1()
        
    def getPosition(self,e): 
        pos = e.GetPosition()
        self.statusBar.SetStatusText(str(pos[0])+','+str(pos[1]), 2)

        
    def saveResult(self,e):
        savefileDialog = wx.FileDialog(self,message='Save as',
            defaultFile='',style=wx.SAVE)
        if savefileDialog.ShowModal()==wx.ID_OK:
            path = savefileDialog.GetPath()
            file = open(path,'w+')
            file.write(self.result.GetValue())
            file.close()
        savefileDialog.Destroy()



    def copyKey(self,e): # 面板二的Copy键
		self.data = wx.TextDataObject()
		self.data.SetText(self.key.GetValue())
		print self.data
		if wx.TheClipboard.Open():
			wx.TheClipboard.SetData(self.data)
			wx.TheClipboard.Close()
		else:
			wx.MessageBox("Unable to open the clipboard", "Error")



if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()