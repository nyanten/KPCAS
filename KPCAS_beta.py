# -*- coding: utf-8 -*-
# build of python3.6 by OS X

# パッケージのインポート
# OpenCV使用
# 他のパッケージはpipコマンドでインストール
import sys, os
import cv2
import numpy
import tkinter as tk
import tkinter.filedialog as tkFD
from PIL import ImageTk, Image
from tkinter import PhotoImage


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack(expand=1, fill=tk.BOTH, anchor=tk.NW)
        # 基本ウィンドウ
        self.create_widgets()

    def create_widgets(self):
        self.title = tk.Label(self, text=u'KrProCessAS', font=("", 20))
        self.label = tk.Label(self, text=u'入力ファイル')
        self.var_entry = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.var_entry)
        self.button = tk.Button(self, text=u"開く", command=self.button_pushed)
        #self.var_check = tk.BooleanVar()
        #self.check = tk.Checkbutton(self, text=u'拡張子をjpgに限定')
        #self.text = tk.Text(self)
        self.canvas = tk.Canvas(self, width=300, height=300)
        self.button_qt = tk.Button(self, text=u"Quit", command=self.button_quit, width=5, height=2)

        # 各物体の位置(gridだとややこしいので、placeで直接指定する)
        # 文字など
        self.title.place(x=70, y=10) #title
        self.label.place(x=480, y=5) #text

        # エントリなど
        self.entry.place(x=480, y=25) #source
        self.entry.insert(tk.END, "開くを押して参照する")
        
        self.button.place(x=680, y=29) #open
        self.button_qt.place(x=10, y=10) #Quit
        #self.button.grid(column=2, row=0, sticky=tk.E)
        self.canvas.place(x=480, y=200)

        #self.columnconfigure(1, weight=1)
        #self.rowconfigure(2, weight=1)

        self.checkbox_make()

    # 参照ファイルコマンド
    def button_pushed(self):
        # http://spcx8.hatenablog.com/entry/2017/12/24/112528
        # ファイルの参照方法はWindowsとmacOSで異なる        
        # Windowsの場合は以下のようになる
        # fname = tkFD.askopenfilename(filetypes=[('data files','*.csv;*.txt')],initialdir=os.getcwd())
        # 参照ファイルの拡張子を絞る方法が異なるようで、Windowsの場合は'*.*'で全表示も可能
        
        fname = tkFD.askopenfilename(filetypes=[("jpg files","*.jpg")],initialdir=os.getcwd())
        print(fname)
        # picture_resize(self.fname)
        img_r = cv2.imread(fname)
        im_re = cv2.resize(img_r, (256, 256))
        cv2.imwrite("/Users/nyanten/Documents/Documents /killtime2/RealPython/OC/resize_picture/import_pic.jpg", im_re)
        # ソースコードの保存場所に気をつける

        # 以下、リサイズ後の絶対パス。なぜかはわからないが、絶対パスでないとエラーを吐く
        # ex) ~/Documents/... とするとエラー
        # 読み込み毎にリサイズされて上書きされる
        real_path = "/Users/nyanten/Documents/Documents /killtime2/RealPython/OC/resize_picture/import_pic.jpg"
        
        self.var_entry.set(fname)

        self.img = ImageTk.PhotoImage(file=real_path)
        self.canvas.create_image(100, 100, image=self.img)
            

    # Exitする
    def button_quit(self):
        print("Good Bye.")
        exit()


    # チェックボックス(命令セット) 仮で10とする
    def checkbox_make(self):
        check_val = []
        check_h = []

        for n in range(int(10)):
            #BooleanVarの作成
            bl = tk.BooleanVar()
            bl.set(False)
            
            b = tk.Checkbutton(text = "命令" + str(n+1), variable = bl)
            b.place(x=100, y=20*n + 50)

            #チェックの値を入れる
            check_val.append(bl)
            #チェックハンドルを入れる
            check_h.append(b)


# ひながた        
if __name__ == "__main__":
    root = tk.Tk()
    root.title("KPCAS_beta")
    root.geometry("720x480") # ウィンドウサイズ
    
    app = Application(master=root)
    app.mainloop()
