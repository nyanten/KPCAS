# -*- coding: utf-8 -*-
# build of python3.6 by OS X

# パッケージのインポート
# OpenCV使用
# 他のパッケージはpipコマンドでインストール
import sys, os, shutil
import datetime
import cv2
import numpy
import tkinter as tk
import tkinter.filedialog as tkFD
from tkinter import PhotoImage
from PIL import ImageTk

#print(sys.path)

# 外部ファイル
import func_collection as fc


#RuntimeError: maximum recursion depth exceeded (再帰の数が深すぎるエラー)
#https://qiita.com/narupo/items/e25ac05a9065c0bd9c03
#http://sucrose.hatenablog.com/entry/2013/01/19/164008
#sys.setrecursionlimit(50000) #再帰の最大数を増やす
#LIMITER = sys.getrecursionlimit()
#print("maximum recursion depth set: " , LIMITER)


FILTER = ('２値化', 'グレイスケール', '赤単色', '緑単色', '青単色',
          '色交換(赤青)', '色交換(赤緑)', '色交換(緑青)', 
          'HSV色空間(色相シフト)', 'HSV色空間(彩度シフト)', 'HSV色空間(明度シフト)',
          '明るく', '暗く', 'ガンマ補正', 'セピア', 'モザイク', 'ネガポジ反転', 'ミラー', 
          'フーリエ変換', '逆フーリエ変換', 'エッジ抽出', 'ノイズのせ', '平均化', 
          'メディアンフィルタ', 'ガウシアンフィルタ', 'アフィン変換(90度)', 
          '顔検出')

FILTER_SET = ()

# カレントディレクトリ取得
CD = os.getcwd()
print(CD)

# 画像リサイズ後の保存先。読み込むたびに上書きされる。
# このパスを自分の環境に合わせて設定。
# 絶対パス
REAL_PATH = os.path.join(CD, "resize_picture", "import_pic.jpg")
print(REAL_PATH)

# 出力絶対パス
O_REAL_PATH = os.path.join(CD, "output_img", "output_img.jpg")
print(O_REAL_PATH)

# 保存先パス
S_REAL_PATH = os.path.join(CD, "save_image", "Final_img_")

# フラグ
FO = 0

# 現時刻
NOW = datetime.datetime.now()


# 命令セット追加削除時のリスト用グローバル変数
# 本来、グローバル変数は大文字表記が暗黙の了解だが、これら以下のものは例外とする。理由は以下の通り。
# 1. このグローバル変数は一部の関数内でのみ扱う。
# 2. 中身の変化状態を別関数では用いていない。
# 3. 結局のところ、組み込んだ命令はグローバル変数 FILTER_SET を読み出すため。
global lb_default
global lb_new


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
        self.button_man = tk.Button(self, text=u"マニュアル", command=self.manual_op, width=20)
        self.button_act = tk.Button(self, text=u"命令を組み込む", command=self.action, width=20)
        self.button_exe = tk.Button(self, text=u"命令を実行", command=self.exe_action, width=20)
        self.button_save = tk.Button(self, text=u"出力結果を保存", command=self.save, width=20)
        self.button_clear = tk.Button(self, text=u"すべてクリア", command=self.all_clear, width=20)
        #self.var_check = tk.BooleanVar()
        #self.check = tk.Checkbutton(self, text=u'拡張子をjpgに限定')
        #self.text = tk.Text(self)

        # キャンバス定義
        self.canvas = tk.Canvas(self, width=200, height=200, relief=tk.RIDGE, bd=2)
        self.o_canvas = tk.Canvas(self, width=250, height=250, relief=tk.RIDGE, bd=2)

        
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
        self.button_man.place(x=500, y=270)
        self.button_act.place(x=500, y=300)
        self.button_exe.place(x=500, y=330)
        self.button_save.place(x=500, y=360)
        self.button_clear.place(x=500, y=390)
        #self.button.grid(column=2, row=0, sticky=tk.E)

        # キャンバスなど
        self.canvas.place(x=500, y=60)
        self.canvas.create_text(110, 110, text=u"Not Found Image...")
        self.o_canvas.place(x=10, y=40)
        self.o_canvas.create_text(127, 127, text=u"Not Output Image...")

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
        global REAL_PATH
        
        fname = tkFD.askopenfilename(filetypes=[("jpg files","*.jpg")],initialdir=os.getcwd())
        print(fname)
        if not fname:
            print("ファイルが指定されていません")

        # picture_resize(self.fname)
        img_r = cv2.imread(fname)
        im_re = cv2.resize(img_r, (256, 256))
        cv2.imwrite(REAL_PATH, im_re)
        # ソースコードの保存場所に気をつける

        # 以下、リサイズ後の絶対パス。なぜかはわからないが、絶対パスでないとエラーを吐く
        # ex) ~/Documents/... とするとエラー
        # 読み込み毎にリサイズされて上書きされる
        
        self.var_entry.set(fname)

        self.img = ImageTk.PhotoImage(file=REAL_PATH)
        self.canvas.create_image(110, 110, image=self.img)


    # マニュアルを開く
    def manual_op(self):
        man = open("./manual.txt","r")
        
        man_win = tk.Toplevel(master=self.master)
        man_win.title("マニュアル")
        man_win.geometry("680x420")

        text_in = man.read()
        text_in.ljust(100)

        button = tk.Button(man_win, text="Quit", command=man_win.destroy)
        button.place(x=10, y=10)

        self.label = tk.Label(man_win, text=text_in, justify="left")
        self.label.place(x=10, y=50)

        #button.focus_set()
        man_win.transient(self.master)
        #man_win.grab_set()
        man.close()


    # 保存
    def save(self):
        global FO
        shutil.copy(O_REAL_PATH, S_REAL_PATH + str(NOW) + "_" + str(FO) + ".jpg")
        FO += 1
        print("save")
            

    # すべてクリア
    def all_clear(self):
        global FILTER_SET
        print("All Set clear")
        FILTER_SET = ()
        flag1 = os.path.exists(REAL_PATH)
        flag2 = os.path.exists(O_REAL_PATH)
        if flag1 == True:
            os.remove(REAL_PATH)
        elif flag2 == True:
            os.remove(O_REAL_PATH)
        elif flag1 == True and flag2 == True:
            os.remove(REAL_PATH)
            os.remove(O_REAL_PATH)

        self.canvas.delete("all")
        self.canvas.create_text(110, 110, text=u"Not Found Image...")
        self.o_canvas.delete("all")
        self.o_canvas.create_text(127, 127, text=u"Not Output Image...")
        print("FILTER SET EMPTY")


    # Exitする 全リセットして終了
    def button_quit(self):
        global FILTER_SET
        print("Good Bye.")
        FILTER_SET = ()
        flag1 = os.path.exists(REAL_PATH)
        flag2 = os.path.exists(O_REAL_PATH)
        if flag1 == True:
            os.remove(REAL_PATH)
        if flag2 == True:
            os.remove(O_REAL_PATH)

        print("FILTER SET EMPTY")
        exit()

        
    #
    # beta作成時に発生していた、命令セットサブウィンドウが無限に増えるVer
    # 組み込んだ命令を動的にリストボックス表示したいがためにaction関数を繰り返し呼び出していた
    #
    # 命令追加系統
    #def action_add_bn(self):
    #    self.show_selection_a()
    
    #def listbox_selected(self, event):
    #    self.show_selection_a()
    
    # def show_selection_a(self):
    #     global slb
    #     global FILTER_SET
    #     for i in lb_default.curselection():
    #         slb = lb_default.get(i)
    #         print(slb + "を組み込みました")
    #         FILTER_SET += (slb, )
    #         self.action()
    #
    # 命令削除系統
    # def action_del_bn(self):
    #     self.show_selection_d()
    
    # def listbox_selected(self, event):
    #     self.show_selection_d()
    
    # def show_selection_d(self):
    #     global dlb
    #     global FILTER_SET
    #     for i in lb_new.curselection():
    #         dlb = lb_new.get(i)
    #         dlb_l = list(FILTER_SET) # タプルの要素削除はできないのでリストへ変更する
    #         del dlb_l[i] # リストで選択されている部分を削除する
    #         FILTER_SET = tuple(dlb_l) # タプルに戻す
    #         print(dlb + "を削除しました")
    #         self.action()
    #
    # action関数を繰り返し呼び出さず、組み込んだリストボックス(lb_new)を再表示させるために、以下のようにコード改変。
    # action関数に内部関数として呼び出すことで解決。
    #
    
    
    # 命令セット
    def action(self):
        global lb_default
        global lb_new
        
        sub_win = tk.Toplevel(master=self.master)
        sub_win.title("命令セット")
        sub_win.geometry("480x240+100+50")

        print("Open Assembly Set")
        
        # 命令追加系統
        def action_add_bn():
            show_selection_a()
    
        def listbox_selected():
            show_selection_a()
    
        def show_selection_a():
            global lb_default
            global lb_new
            global FILTER_SET
            for i in lb_default.curselection():
                slb = lb_default.get(i)
                print(slb + "を組み込みました")
                FILTER_SET += (slb, )

                # リストボックスの更新
                frame2 = tk.Frame(sub_win)
                frame2.place(x=250, y=50)
                v2 = tk.StringVar(value=FILTER_SET)
                lb_new = tk.Listbox(frame2, listvariable=v2, width=18, height=10)
                lb_new.grid(row=0, column=0)
                scrollbar_2 = tk.Scrollbar(frame2, orient="v", command=lb_new.yview)
                lb_new['yscrollcommand'] = scrollbar_2.set
                scrollbar_2.grid(row=0, column=1, sticky=tk.NS)
                

        # 命令削除系統
        def action_del_bn():
            show_selection_d()
    
        def listbox_selected_d():
            show_selection_d()
    
        def show_selection_d():
            global lb_new
            global FILTER_SET
            for i in lb_new.curselection():
                dlb = lb_new.get(i)
                dlb_l = list(FILTER_SET) # タプルの要素削除はできないのでリストへ変更する
                del dlb_l[i] # リストで選択されている部分を削除する
                FILTER_SET = tuple(dlb_l) # タプルに戻す
                print(dlb + "を削除しました")

                # リストボックス更新
                frame2 = tk.Frame(sub_win)
                frame2.place(x=250, y=50)
                v2 = tk.StringVar(value=FILTER_SET)
                lb_new = tk.Listbox(frame2, listvariable=v2, width=18, height=10)
                lb_new.grid(row=0, column=0)
                scrollbar_2 = tk.Scrollbar(frame2, orient="v", command=lb_new.yview)
                lb_new['yscrollcommand'] = scrollbar_2.set
                scrollbar_2.grid(row=0, column=1, sticky=tk.NS)


        # 命令全クリア
        def action_all_clear():
            global FILTER_SET
            FILTER_SET = ()
            
            frame2 = tk.Frame(sub_win)
            frame2.place(x=250, y=50)
            v2 = tk.StringVar(value=FILTER_SET)
            lb_new = tk.Listbox(frame2, listvariable=v2, width=18, height=10)
            lb_new.grid(row=0, column=0)
            scrollbar_2 = tk.Scrollbar(frame2, orient="v", command=lb_new.yview)
            lb_new['yscrollcommand'] = scrollbar_2.set
            scrollbar_2.grid(row=0, column=1, sticky=tk.NS)
            

        # リストボックス用フレーム
        frame1 = tk.Frame(sub_win)
        frame1.place(x=10, y=50)
        frame2 = tk.Frame(sub_win)
        frame2.place(x=250, y=50)

        # 内部関数(ネストした関数)は関数オブジェクトとして扱う
        f1 = action_add_bn
        f2 = listbox_selected
        f3 = action_del_bn
        f4 = listbox_selected_d
        f5 = action_all_clear

        # デフォルトでのリストボックスとスクロールバー生成
        v1 = tk.StringVar(value=FILTER)
        v2 = tk.StringVar(value=FILTER_SET)
        lb_default = tk.Listbox(frame1, listvariable=v1, width=18, height=10)
        lb_new = tk.Listbox(frame2, listvariable=v2, width=18, height=10)

        # リストボックスの配置
        lb_default.grid(row=0, column=0)
        lb_new.grid(row=0, column=0)

        # スクロールバーの詳細設定
        scrollbar_1 = tk.Scrollbar(frame1, orient="v", command=lb_default.yview)
        scrollbar_2 = tk.Scrollbar(frame2, orient="v", command=lb_new.yview)
        lb_default['yscrollcommand'] = scrollbar_1.set
        lb_new['yscrollcommand'] = scrollbar_2.set

        # スクロールバーの配置
        scrollbar_1.grid(row=0, column=1, sticky=tk.NS)
        scrollbar_2.grid(row=0, column=1, sticky=tk.NS)

        # 選択されている部分をバインドするためのもの
        lb_default.bind("<<Double-Button-1>>", f2)
        lb_new.bind("<<Double-Button-1>>", f4)

        # 各ボタンの役割と配置
        button = tk.Button(sub_win, text="Quit", command=sub_win.destroy)
        button.place(x=10, y=10)
        button = tk.Button(sub_win, text="命令を組む", command=f1)
        button.place(x=80, y=10)
        button = tk.Button(sub_win, text="命令を消す", command=f3)
        button.place(x=250, y=10)

        button = tk.Button(sub_win, text="命令をクリア", command=f5)
        button.place(x=350, y=10)

        # 命令組み込み時にサブウィンドウへとフォーカスする
        button.focus_set()
        sub_win.transient(self.master)
        sub_win.grab_set()


    # 命令セット逐次実行
    def exe_action(self):
        print(len(FILTER_SET))
        # 作成した命令セットの長さ
        j = range(len(FILTER_SET))

        if FILTER_SET != ():
        # 命令セット分だけ順に実行する
            for i in j:
                # 初回はリサイズしたものを読み込み、以降は処理後を繰り返し読む
                if i == 0:
                    if FILTER_SET[i] in {"２値化"}:
                        print("２値化")
                        fc.Binary(REAL_PATH)
                    elif FILTER_SET[i] in {"グレイスケール"}:
                        print("グレイスケール")
                        fc.Gray(REAL_PATH)
                    elif FILTER_SET[i] in {"赤単色"}:
                        print("赤単色")
                        fc.Red(REAL_PATH)
                    elif FILTER_SET[i] in {"緑単色"}:
                        print("緑単色")
                        fc.Green(REAL_PATH)
                    elif FILTER_SET[i] in {"青単色"}:
                        print("青単色")
                        fc.Blue(REAL_PATH)
                    elif FILTER_SET[i] in {"色交換(赤青)"}:
                        print("色交換(赤青)")
                        fc.RtoB(REAL_PATH)
                    elif FILTER_SET[i] in {"色交換(赤緑)"}:
                        print("色交換(赤緑)")
                        fc.RtoG(REAL_PATH)
                    elif FILTER_SET[i] in {"色交換(緑青)"}:
                        print("色交換(緑青)")
                        fc.GtoB(REAL_PATH)
                    elif FILTER_SET[i] in {"HSV色空間(色相シフト)"}:
                        print("HSV色空間(色相シフト)")
                        fc.HSV_h(REAL_PATH)
                    elif FILTER_SET[i] in {"HSV色空間(彩度シフト)"}:
                        print("HSV色空間(彩度シフト)")
                        fc.HSV_s(REAL_PATH)
                    elif FILTER_SET[i] in {"HSV色空間(明度シフト)"}:
                        print("HSV色空間(明度シフト)")
                        fc.HSV_v(REAL_PATH)
                    elif FILTER_SET[i] in {"明るく"}:
                        print("明るく")
                        fc.Bright(REAL_PATH)
                    elif FILTER_SET[i] in {"暗く"}:
                        print("暗く")
                        fc.Dark(REAL_PATH)
                    elif FILTER_SET[i] in {"ガンマ補正"}:
                        print("ガンマ補正")
                        fc.Gamma(REAL_PATH)
                    elif FILTER_SET[i] in {"セピア"}:
                        print("セピア")
                        fc.Sepia(REAL_PATH)
                    elif FILTER_SET[i] in {"モザイク"}:
                        print("モザイク")
                        fc.Moza(REAL_PATH)
                    elif FILTER_SET[i] in {"ネガポジ反転"}:
                        print("ネガポジ反転")
                        fc.NegaPosi(REAL_PATH)
                    elif FILTER_SET[i] in {"ミラー"}:
                        print("ミラー")
                        fc.Mirror(REAL_PATH)
                    elif FILTER_SET[i] in {"アフィン変換(90度)"}:
                        print("アフィン変換")
                        fc.Rotate(REAL_PATH)
                    else:
                        print("ぶっこわれ")
                        
                # 初回以降
                else:
                    if FILTER_SET[i] in {"２値化"}:
                        print("２値化")
                        fc.Binary(O_REAL_PATH)
                    elif FILTER_SET[i] in {"グレイスケール"}:
                        print("グレイスケール")
                        fc.Gray(O_REAL_PATH)
                    elif FILTER_SET[i] in {"赤単色"}:
                        print("赤単色")
                        fc.Red(O_REAL_PATH)
                    elif FILTER_SET[i] in {"緑単色"}:
                        print("緑単色")
                        fc.Green(O_REAL_PATH)
                    elif FILTER_SET[i] in {"青単色"}:
                        print("青単色")
                        fc.Blue(O_REAL_PATH)
                    elif FILTER_SET[i] in {"色交換(赤青)"}:
                        print("色交換(赤青)")
                        fc.RtoB(O_REAL_PATH)
                    elif FILTER_SET[i] in {"色交換(赤緑)"}:
                        print("色交換(赤緑)")
                        fc.RtoG(O_REAL_PATH)
                    elif FILTER_SET[i] in {"色交換(緑青)"}:
                        print("色交換(緑青)")
                        fc.GtoB(O_REAL_PATH)
                    elif FILTER_SET[i] in {"HSV色空間(色相シフト)"}:
                        print("HSV色空間(色相シフト)")
                        fc.HSV_h(O_REAL_PATH)
                    elif FILTER_SET[i] in {"HSV色空間(彩度シフト)"}:
                        print("HSV色空間(彩度シフト)")
                        fc.HSV_s(O_REAL_PATH)
                    elif FILTER_SET[i] in {"HSV色空間(明度シフト)"}:
                        print("HSV色空間(明度シフト)")
                        fc.HSV_v(O_REAL_PATH)
                    elif FILTER_SET[i] in {"明るく"}:
                        print("明るく")
                        fc.Bright(O_REAL_PATH)
                    elif FILTER_SET[i] in {"暗く"}:
                        print("暗く")
                        fc.Dark(O_REAL_PATH)
                    elif FILTER_SET[i] in {"ガンマ補正"}:
                        print("ガンマ補正")
                        fc.Gamma(O_REAL_PATH)
                    elif FILTER_SET[i] in {"セピア"}:
                        print("セピア")
                        fc.Sepia(O_REAL_PATH)
                    elif FILTER_SET[i] in {"モザイク"}:
                        print("モザイク")
                        fc.Moza(O_REAL_PATH)
                    elif FILTER_SET[i] in {"ネガポジ反転"}:
                        print("ネガポジ反転")
                        fc.NegaPosi(O_REAL_PATH)
                    elif FILTER_SET[i] in {"ミラー"}:
                        print("ミラー")
                        fc.Mirror(O_REAL_PATH)
                    elif FILTER_SET[i] in {"アフィン変換(90度)"}:
                        print("アフィン変換")
                        fc.Rotate(O_REAL_PATH)
                    else:
                        print("ぶっこわれ")

            self.img_2 = ImageTk.PhotoImage(file=O_REAL_PATH)
            self.o_canvas.create_image(127, 127, image=self.img_2)

        else:
            print("命令セットが組み込まれていません")

    
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
