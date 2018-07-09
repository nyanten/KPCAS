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
        # 各ウィジェット
        # 文字定義
        self.title = tk.Label(self, text=u"KrProCessAS", font=("", 20))
        self.label = tk.Label(self, text=u"入力ファイル")

        # エントリ定義
        self.var_entry = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.var_entry, width=22)

        # ボタン定義
        self.button = tk.Button(self, text=u"開く", command=self.button_pushed)
        self.button_qt = tk.Button(self, text=u"Quit", command=self.button_quit, width=5, height=2)
        self.button_act = tk.Button(self, text=u"命令セットを開く", command=self.button_action, width=15, height=2)
        
        #self.var_check = tk.BooleanVar()
        #self.check = tk.Checkbutton(self, text=u'拡張子をjpgに限定')
        #self.text = tk.Text(self)

        # キャンバス定義
        self.canvas = tk.Canvas(self, width=200, height=200, relief=tk.RIDGE, bd=2)

        # 命令ウィンドウ表示
        

        #
        # 各物体の位置(gridだとややこしいので、placeで直接指定する)
        # 文字など
        self.title.place(x=70, y=15)
        self.label.place(x=500, y=5)

        # エントリなど
        self.entry.place(x=500, y=30) #source
        self.entry.insert(tk.END, "開くを押して参照する")

        # ボタンなど
        self.button.place(x=650, y=5)
        self.button_qt.place(x=10, y=10)
        self.button_act.place(x=300, y=400)
        #self.button.grid(column=2, row=0, sticky=tk.E)

        # キャンバスなど
        self.canvas.place(x=500, y=60)
        self.canvas.create_text(110, 110, text=u"Not Found Image...")

        # リストボックス・スクロールなど

        

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
        self.canvas.create_image(110, 110, image=self.img)
            

    # Exitする
    def button_quit(self):
        print("Good Bye.")
        exit()


    def button_action(self):
        sub_win = tk.Toplevel(master=self.master)

        frame1 = tk.Frame(sub_win)
        frame1.grid()
        
        currencies = ('JPY', 'USD', 'EUR', 'CNY', 'MXN', 'CAD')
        v1 = tk.StringVar(value=currencies)
        lb = tk.Listbox(frame1, listvariable=v1, height=3)
        lb.grid(row=0, column=0)

        scrollbar = tk.Scrollbar(frame1, orient="v", command=lb.yview)
        lb['yscrollcommand'] = scrollbar.set
        scrollbar.grid(row=0, column=1, sticky=tk.NS)
        
        button = tk.Button(frame1, text="thank you", command=sub_win.destroy)
        button.grid(row=1, column=0, columnspan=2)
        button.focus_set()
        sub_win.transient(self.master)
        sub_win.grab_set()
        
        

    # チェックボックス(命令セット) 仮で10とする
    def checkbox_make(self):
        check_val = []
        check_h = []

        for n in range(int(10)):
            #BooleanVarの作成
            bl = tk.BooleanVar()
            bl.set(False)

            self.listbox.insert(x, "Meirei" + str(n+1))
            #b = tk.Checkbutton(text=u"命令" + str(n+1), variable = bl)
            #b.self.place(x=400, y=20*n + 100)
            
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
