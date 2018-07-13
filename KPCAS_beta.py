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
from tkinter import PhotoImage
from PIL import ImageTk


#RuntimeError: maximum recursion depth exceeded (再帰の数が深すぎるエラー)
#https://qiita.com/narupo/items/e25ac05a9065c0bd9c03
#http://sucrose.hatenablog.com/entry/2013/01/19/164008
#sys.setrecursionlimit(50000) #再帰の最大数を増やす
#LIMITER = sys.getrecursionlimit()
#print("maximum recursion depth set: " , LIMITER)

FILTER = ('２値化', 'グレイスケール', '赤成分抽出', '緑成分抽出', '青成分抽出',
          'フーリエ変換', '逆フーリエ変換', '平滑化', 'エッジ抽出', 'hoge',
          'ノイズのせ', 'メディアンフィルタ', 'ガウシアンフィルタ',
          '細線化', 'タイル化', '顔検出')

FILTER_SET = ('画像を読み込む', )


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
        self.button_qt = tk.Button(self, text=u"Quit", command=self.button_quit)
        self.button_act = tk.Button(self, text=u"命令を組み込む", command=self.action, width=20)
        self.button_man = tk.Button(self, text=u"マニュアル", command=self.manual_op, width=20)
        #self.var_check = tk.BooleanVar()
        #self.check = tk.Checkbutton(self, text=u'拡張子をjpgに限定')
        #self.text = tk.Text(self)

        # キャンバス定義
        self.canvas = tk.Canvas(self, width=200, height=200, relief=tk.RIDGE, bd=2)


        
        # 各物体の位置(gridだとややこしいので、placeで直接指定する)
        # 文字など
        self.title.place(x=100, y=5)
        self.label.place(x=500, y=3)

        # エントリなど
        self.entry.place(x=500, y=30) #source
        self.entry.insert(tk.END, "開くを押して参照する")

        # ボタンなど
        self.button.place(x=655, y=0)
        self.button_qt.place(x=10, y=5)
        self.button_act.place(x=500, y=300)
        self.button_man.place(x=500, y=270)
        #self.button.grid(column=2, row=0, sticky=tk.E)

        # キャンバスなど
        self.canvas.place(x=500, y=60)
        self.canvas.create_text(110, 110, text=u"Not Found Image...")

        # リストボックス・スクロールなど


        # その他
        #self.checkbox_make()

    # 参照ファイルコマンド
    def button_pushed(self):
        # http://spcx8.hatenablog.com/entry/2017/12/24/112528
        # ファイルの参照方法はWindowsとmacOSで異なる        
        # Windowsの場合は以下のようになる
        # fname = tkFD.askopenfilename(filetypes=[('data files','*.csv;*.txt')],initialdir=os.getcwd())
        # 参照ファイルの拡張子を絞る方法が異なるようで、Windowsの場合は'*.*'で全表示も可能
        
        fname = tkFD.askopenfilename(filetypes=[("jpg files","*.jpg")],initialdir=os.getcwd())
        print(fname)
        if not fname:
            print("ファイルが指定されていません")

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


    # 命令追加系統
    def action_add_bn(self):
        self.show_selection_a()
    
    def listbox_selected(self, event):
        self.show_selection_a()
    
    def show_selection_a(self):
        global slb
        global FILTER_SET
        for i in lb_default.curselection():
            slb = lb_default.get(i)
            print(slb + "を組み込みました")
            FILTER_SET += (slb, )
            self.action()

    # 命令削除系統
    def action_del_bn(self):
        self.show_selection_d()
    
    def listbox_selected(self, event):
        self.show_selection_d()
    
    def show_selection_d(self):
        global dlb
        global FILTER_SET
        for i in lb_new.curselection():
            dlb = lb_new.get(i)
            dlb_l = list(FILTER_SET) # タプルの要素削除はできないのでリストへ変更する
            del dlb_l[i] # リストで選択されている部分を削除する
            FILTER_SET = tuple(dlb_l) # タプルに戻す
            print(dlb + "を削除しました")
            self.action()
        

    # 命令セット
    def action(self):
        global lb_default
        global lb_new
        
        sub_win = tk.Toplevel(master=self.master)
        sub_win.title("命令セット")
        sub_win.geometry("480x240")

        print("Open Assembly Set")

        frame1 = tk.Frame(sub_win)
        frame1.place(x=10, y=50)
        frame2 = tk.Frame(sub_win)
        frame2.place(x=250, y=50)
        
        v1 = tk.StringVar(value=FILTER)
        v2 = tk.StringVar(value=FILTER_SET)
        lb_default = tk.Listbox(frame1, listvariable=v1, width=18, height=10)
        lb_new = tk.Listbox(frame2, listvariable=v2, width=18, height=10)
        
        lb_default.grid(row=0, column=0)
        lb_new.grid(row=0, column=0)

        scrollbar_1 = tk.Scrollbar(frame1, orient="v", command=lb_default.yview)
        scrollbar_2 = tk.Scrollbar(frame2, orient="v", command=lb_new.yview)
        lb_default['yscrollcommand'] = scrollbar_1.set
        lb_new['yscrollcommand'] = scrollbar_2.set
        
        scrollbar_1.grid(row=0, column=1, sticky=tk.NS)
        scrollbar_2.grid(row=0, column=1, sticky=tk.NS)
        
        lb_default.bind("<<Double-Button-1>>", self.listbox_selected)
        
        button = tk.Button(sub_win, text="Quit", command=sub_win.destroy)
        button.place(x=10, y=10)
        button = tk.Button(sub_win, text="命令を組む", command=self.action_add_bn)
        button.place(x=80, y=10)
        button = tk.Button(sub_win, text="命令を消す", command=self.action_del_bn)
        button.place(x=250, y=10)

        button = tk.Button(sub_win, text="実装")
        button.place(x=350, y=10)
        
        button.focus_set()
        sub_win.transient(self.master)
        sub_win.grab_set()


    def manual_op(self):
        man = open("./manual.txt","r")
        
        man_win = tk.Toplevel(master=self.master)
        man_win.title("マニュアル")
        man_win.geometry("680x420")

        text_in = man.read()
        text_in.ljust(100)

        button = tk.Button(man_win, text="Quit", command=kill)
        button.place(x=10, y=10)

        self.label = tk.Label(man_win, text=text_in, justify="left")
        self.label.place(x=10, y=50)

        #button.focus_set()
        man_win.transient(self.master)
        #man_win.grab_set()
        man.close()
            
    
    
    # チェックボックス(命令セット) 仮で10とする
    def checkbox_make(self):
        check_val = []
        check_h = []

        for n in range(int(10)):
            #BooleanVarの作成
            bl = tk.BooleanVar()
            bl.set(False)

            b = tk.Checkbutton(text=u"命令" + str(n+1), variable = bl)
            b.place(x=400, y=20*n + 100)
            
            #チェックの値を入れる
            check_val.append(bl)
            #チェックハンドルを入れる
            check_h.append(b)



# ひながた        
if __name__ == "__main__":
    root = tk.Tk()
    root.title("beta")
    root.geometry("720x480") # ウィンドウサイズ
    
    app = Application(master=root)
    app.mainloop()
