#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import cv2

class TkRoot(tk.Tk):
    '''
    Tkinterウィンドウ画面クラス (画面設定/メニューバー設定)
    '''
    def __init__(self):
        '''
        Tkinterウィンドウ画面コンストラクタ
        '''
        super().__init__()
        self.title("GUI_title")     #Windowタイトルの描画
        self.geometry("400x300")    #画面サイズ
        self.config(bg="black")     #背景色
        self.create_menu()

    def callback_GUI_file_select(self):
        '''
        GUIを用いたファイル指定
        '''
        # ファイル選択ダイアログの表示
        fTyp = [("","*")]   #fTypeで拡張子を限定可能
        iDir = os.path.abspath(os.path.dirname(__file__))   #GUI表示でのデフォルトパスを指定
        file = filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)   #指定したファイル名を取得する (キャンセル時は空文字)
        if file != "":
            messagebox.showinfo('folder',file)

    def callback_GUI_folder_select(self):
        '''
        GUIを用いたフォルダ指定
        '''
        # ファイル選択ダイアログの表示
        iDir = os.path.abspath(os.path.dirname(__file__))     #GUI表示でのデフォルトパスを指定
        folder = filedialog.askdirectory(initialdir = iDir)   #指定したファイル名を取得する (キャンセル時は空文字)
        if folder != "":
            messagebox.showinfo('folder',folder)

    def create_menu(self):
        '''
        メニューバーの描画
        '''
        self.menu_bar = Menu(self)
        self.config(menu = self.menu_bar)
        self.file_menu = Menu(self.menu_bar,tearoff=0)
        self.file_menu.add_command(label='Open Existing File',command=self.callback_GUI_file_select)    #ファイル指定GUIメニュー
        self.file_menu.add_separator()  #セパレータの表示
        self.file_menu.add_command(label='Open Existing Directry',command=self.callback_GUI_folder_select)   #フォルダ指定GUIメニュー
        self.menu_bar.add_cascade(label='Files', menu=self.file_menu)

class TkFrame(tk.Frame):
    def __init__(self, master=None):
        '''
        Tkinterウィンドウ画面コンストラクタ
        '''
        super().__init__(master)
        self.root = master
        self.config(width=200)  #フレームサイズの設定(幅)
        self.config(height=200) #フレームサイズの設定(高さ)
        self.config(bg="gray")  #フレームの設定(色)
        self.propagate(False)   #フレームのpropagate設定 (この設定がTrueだと内側のwidgetに合わせたフレームサイズになる)
        self.create_widgets()   #widgetsの追加
        self.pack()             #フレーム描画

        #http://cylomw.hatenablog.com/entry/2016/11/08/183644

    def create_widgets(self):
        '''
        Widget描画用処理
        '''
        #ラベルの描画
        #ラベル表示するテキストを設定　font(フォント名/サイズ/太文字),fg:文字色,bg:背景色
        self.label1 = tk.Label(self,text='label_test',font=("Helvetica", 20, "bold"),fg = "red",bg = "blue") 
        self.label1.grid(row=0,column =0,sticky=tk.W)

        #キャンバスの描画 (Opencvで読み込んだ画像の表示)
        image_bgr = cv2.imread("lena.jpg")
        image_bgr = cv2.resize(image_bgr,(100,100))            # opencv画像をresize
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB) # imreadはBGRなのでRGBに変換
        image_pil = Image.fromarray(image_rgb)                 # RGBをPILフォーマットに変換
        self.image_tk  = ImageTk.PhotoImage(image_pil)         # ImageTkフォーマットへ変換
        self.canvas = tk.Canvas(self, bg="blue", width=image_bgr.shape[0], height=image_bgr.shape[1])
        self.canvas.create_image(0, 0, image=self.image_tk, anchor='nw') # ImageTk 画像配置
        self.canvas.grid(row=1,column =0,columnspan=2,sticky=tk.W)

        #ボタンの描画
        self.button1 = tk.Button(self,text="Hello World",command=self.func_callback_button) #ボタン文字列・コールバック関数の設定
        self.button1.grid(row=2,column =0,sticky=tk.W)
        ##http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/anchors.html

        #テキストボックスの描画
        self.textbox1 = tk.Entry(self,width=20)
        self.textbox1.insert(tk.END,"default") #テキストボックス初期文字列の設定
        self.textbox1.grid(row=3,column =0,sticky=tk.W)

        #チェックボタンの描画
        self.chval = tk.BooleanVar(False) #チェックボタン初期値設定
        self.chbox1 = tk.Checkbutton(self, text = 'check1', variable = self.chval) #チェックボタンテキスト/変数紐づけ設定
        self.chbox1.grid(row=4,column =0,sticky=tk.W)

        #ラジオボタンの描画 (択一式)
        self.radval = tk.IntVar(0)  #ラジオボタンテキスト/変数紐づけ設定
        self.radbut1 = tk.Radiobutton(self, text = 'radio0', variable = self.radval, value = 0) #ラジオボタンテキスト/変数紐づけ設定
        self.radbut1.grid(row=5,column =0,sticky=tk.W)
        self.radbut2 = tk.Radiobutton(self, text = 'radio1', variable = self.radval, value = 1) #ラジオボタンテキスト/変数紐づけ設定
        self.radbut2.grid(row=5,column =1,sticky=tk.W)

        #シークバーの表示
        self.seekbarval = tk.DoubleVar() #シークバー変数設定
        self.seekbarval.trace("w", self.func_callback_seekbar) #シークバー変数変動時コールバック関数設定
        self.sc = ttk.Scale(self,variable=self.seekbarval,orient=tk.HORIZONTAL,from_=0,to=255)  #シークバー描画
        self.sc.grid(row=6, column=0,columnspan=2, sticky=(tk.N,tk.E,tk.S,tk.W))

    def func_callback_seekbar(self,*args):
        '''
        バーを動かして値が変化したときのコールバック
        '''
        print('value = %d' % self.seekbarval.get())

    def func_callback_button(self):
        '''
        ボタンを押したときのコールバック関数
        '''
        print("テキストボックス:",self.textbox1.get())
        print("チェックボックス:",self.chval.get())

if __name__ == '__main__':
    app = TkFrame(master=TkRoot())
    app.mainloop()