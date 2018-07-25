# -*- coding: utf-8 -*-
# build of python3.6 by OS X

# パッケージのインポート
# OpenCV使用
# 他のパッケージはpipコマンドでインストール
import sys, os, shutil
import datetime
import webbrowser as wb

import cv2
import numpy
import tkinter as tk
import tkinter.filedialog as tkFD
from tkinter import PhotoImage
from PIL import ImageTk, Image
import random

#print(sys.path)

# 外部ファイル
import func_collection as fc

root = tk.Tk()
root.title("KPCAS beta 0.1")
root.geometry("720x380") # ウィンドウサイズ

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
          '減色', 'ソーラライズ', 'ポスタライズ', 'イコライズ', '回転(90度)',
          '平均化', 'メディアンフィルタ', 'ガウシアンフィルタ', 'DoG',
          '一次微分(横)', '一次微分(縦)', 'Prewitt', 'Sobel', 'ラプラシアン', 'ラプラシアン(PIL)',
          'エンボス', 'エンボス(PIL)',
          'ごま塩ノイズ', 'ガウシアンノイズ', 'フーリエ変換', 'ローパスフィルタ', 'ハイパスフィルタ',
          '顔検出', '顔面モザイク')

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
ADD_FLAG = 0
PT_FLAG = 0

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
        global val_c
        # 各ウィジェット
        # 文字定義
        self.title = tk.Label(self, text=u"KrProCessAS", font=("", 20), bg='#ffaacc')

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
        self.button_output_clear = tk.Button(self, text=u"出力結果をクリア", command=self.output_clear, width=20)
        self.button_web = tk.Button(self, text=u"Wikiをみる", command=self.web_link, width=20)

        # キャンバス定義
        self.canvas = tk.Canvas(self, width=200, height=200, relief=tk.RIDGE, bd=2)
        self.o_canvas = tk.Canvas(self, width=256, height=256, relief=tk.RIDGE, bd=2)

        # リストボックス/スクロールバー
        self.frame = tk.Frame(root)
        self.frame.place(x=285, y=43)

        self.v = tk.StringVar(value=FILTER_SET)
        self.listbox_main = tk.Listbox(self.frame, listvariable=self.v, width=20, height=15, relief=tk.RIDGE, bd=2)
        self.scrollbar_m = tk.Scrollbar(self.frame, orient="v", command=self.listbox_main.yview)
        self.listbox_main['yscrollcommand'] = self.scrollbar_m.set

        # チェックボックス
        val_c = tk.BooleanVar()
        val_c.set(False)
        self.checkbox = tk.Checkbutton(self, text=u"リサイズしない", variable=val_c)


        # 各物体の位置(gridだとややこしいので、placeで直接指定する)
        # 文字など
        self.title.place(x=100, y=5)

        # エントリなど
        self.entry.place(x=500, y=30) #source
        self.entry.insert(tk.END, "開くを押して参照する")

        # ボタンなど
        self.button.place(x=655, y=2)
        self.button_qt.place(x=10, y=5)
        self.button_man.place(x=500, y=275)
        self.button_act.place(x=280, y=310)
        self.button_exe.place(x=280, y=340)
        self.button_save.place(x=40, y=310)
        self.button_output_clear.place(x=40, y=340)
        self.button_clear.place(x=500, y=310)
        self.button_web.place(x=500, y=340)
        #self.button.grid(column=2, row=0, sticky=tk.E)

        # キャンバスなど
        self.canvas.place(x=500, y=60)
        self.canvas.create_text(110, 110, text=u"Not Found Image...")
        self.o_canvas.place(x=10, y=40)
        self.o_canvas.create_text(127, 127, text=u"Not Output Image...")

        # リストボックス/スクロールバーなど
        self.listbox_main.grid(row=0, column=0)
        self.scrollbar_m.grid(row=0, column=1, sticky=tk.NS)

        # その他
        self.checkbox.place(x=500, y=5)

        # おまけ


    # 参照ファイルコマンド
    def button_pushed(self):
        # http://spcx8.hatenablog.com/entry/2017/12/24/112528
        # ファイルの参照方法はWindowsとmacOSで異なる
        # Windowsの場合は以下のようになる
        # fname = tkFD.askopenfilename(filetypes=[('data files','*.csv;*.txt')],initialdir=os.getcwd())
        # 参照ファイルの拡張子を絞る方法が異なるようで、Windowsの場合は'*.*'で全表示も可能
        global REAL_PATH
        global val_c

        fname = tkFD.askopenfilename(filetypes=[("jpg files","*.jpg"),("png files","*.png")],initialdir=os.getcwd())
        print(fname)
        if not fname:
            print("ファイルが指定されていません")

        if val_c.get() == True:
            img = Image.open(fname)
            img.save(REAL_PATH)
        else:
            img = Image.open(fname)
            im_r = img.resize((256, 256))
            im_r.save(REAL_PATH)


        # ソースコードの保存場所に気をつける

        # 以下、リサイズ後の絶対パス。なぜかはわからないが、絶対パスでないとエラーを吐く
        # ex) ~/Documents/... とするとエラー
        # 読み込み毎にリサイズされて上書きされる

        self.var_entry.set(fname)

        self.img = ImageTk.PhotoImage(file=REAL_PATH)
        self.canvas.create_image(110, 110, image=self.img)


    # マニュアルを開く
    def manual_op(self):
        man = open("./manual.txt","r", encoding="utf-8")

        man_win = tk.Toplevel(master=self.master)
        man_win.title("マニュアル")
        man_win.geometry("680x420+100+100")

        text_in = man.read()
        text_in.ljust(100)

        self.button = tk.Button(man_win, text="Quit", command=man_win.destroy)
        self.button.place(x=10, y=10)

        self.label = tk.Label(man_win, text=text_in, justify="left")
        self.label.place(x=10, y=50)

        #button.focus_set()
        man_win.transient(self.master)
        #man_win.grab_set()
        self.konami = tk.StringVar()
        self.K_COM = tk.Entry(man_win, textvariable=self.konami, width=14)
        self.K_COM.place(x=460, y=10)
        self.button_k = tk.Button(man_win, text="Go", command=self.check_K_COM)
        self.button_k.place(x=600, y=10)
        man.close()

    def check_K_COM(self):
        global FILTER
        global ADD_FLAG
        check = self.K_COM.get()
        if ADD_FLAG == 0:
            if check == "uuddlrlrAB":
                FILTER += ('ヒデオ1', 'ヒデオ2', 'FOXDIE', )
                ADD_FLAG = 1
                print("君は選ばれた")
            else:
                print("204863")
        else:
            print("俺は歩いたよ\n歩くことしかできなかったんだ\nやがて 俺の前を歩く俺が見えた\nだが あれは俺じゃない\n気をつけろ\nそのドアの隙間は 分断された現実(セパレート・リアリティ)だ\n俺なのは 俺だけだ\nお前なのは お前だけか？")


    # 保存
    def save(self):
        global FO
        shutil.copy(O_REAL_PATH, S_REAL_PATH + str(NOW) + "_" + str(FO) + ".jpg")
        FO += 1
        print("save")


    # リンクに飛ぶ
    def web_link(self):
        wb.open_new("https://github.com/nyanten/KPCAS/wiki")


    # すべてクリア
    def all_clear(self):
        global FILTER_SET
        FILTER_SET = ()
        print("All Set clear")

        self.clear_module()

        self.canvas.delete("all")
        self.canvas.create_text(110, 110, text=u"Not Found Image...")
        self.o_canvas.delete("all")
        self.o_canvas.create_text(127, 127, text=u"Not Output Image...")

        # メインのリストボックスを更新
        frame = tk.Frame(root)
        frame.place(x=285, y=43)

        v = tk.StringVar(value=FILTER_SET)
        self.listbox_main = tk.Listbox(frame, listvariable=v, width=20, height=15, relief=tk.RIDGE, bd=2)
        self.scrollbar_m = tk.Scrollbar(frame, orient="v", command=self.listbox_main.yview)
        self.listbox_main['yscrollcommand'] = self.scrollbar_m.set

        self.listbox_main.grid(row=0, column=0)
        self.scrollbar_m.grid(row=0, column=1, sticky=tk.NS)


    # 出力結果画像クリア
    def output_clear(self):
        flag2 = os.path.exists(O_REAL_PATH)
        if flag2 == True:
            os.remove(O_REAL_PATH)

        self.o_canvas.delete("all")
        self.o_canvas.create_text(127, 127, text=u"Not Output Image...")
        print("Output Image Delete")


    # Exitする 全リセットして終了
    def button_quit(self):
        global FILTER_SET
        FILTER_SET = ()
        print("Good Bye.")
        self.clear_module()
        exit()


    # クリア系統
    def clear_module(self):
        flag1 = os.path.exists(REAL_PATH)
        flag2 = os.path.exists(O_REAL_PATH)
        if flag1 == True:
            os.remove(REAL_PATH)
        if flag2 == True:
            os.remove(O_REAL_PATH)

        print("FILTER SET EMPTY")


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

                listbox_update()


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

                listbox_update()


        # 命令全クリア
        def action_all_clear():
            global lb_new
            global FILTER_SET
            FILTER_SET = ()
            lb_new = ()
            print("命令を全消去しました")

            listbox_update()


        # 命令入れ替え
        def action_change():
            global lb_new
            global FILTER_SET
            for i in lb_new.curselection():
                f = lb_new.get(i+1)
                if f != "":
                    clb = list(FILTER_SET) # リスト変換
                    clb[i] = lb_new.get(i+1)
                    clb[i+1] = lb_new.get(i)
                    FILTER_SET = tuple(clb) # タプル変換
                    print(clb[i+1] + "と" + clb[i] + "を入れ替えました")
                else:
                    print("下には何もありません")

                listbox_update()


        # 命令ソート
        def action_sort():
            global lb_new
            global FILTER_SET
            sort_l = list(FILTER_SET) # リスト変換
            sort_l.reverse()
            FILTER_SET = tuple(sort_l)
            print("全命令を逆順にソートしました")

            listbox_update()


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
        f6 = action_change
        f7 = action_sort

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

        button = tk.Button(sub_win, text="⇅", command=f6, font=("", 12))
        button.place(x=435, y=80)

        button = tk.Button(sub_win, text="↕", command=f7, font=("", 14))
        button.place(x=438, y=120)

        # 命令組み込み時にサブウィンドウへとフォーカスする、ウィンドウを無限に増やさない
        button.focus_set()
        sub_win.transient(self.master)
        sub_win.grab_set()


        # リストボックス更新
        def listbox_update():
            global lb_new
            global FILTER_SET
            # リストボックス更新
            frame2 = tk.Frame(sub_win)
            frame2.place(x=250, y=50)
            v2 = tk.StringVar(value=FILTER_SET)
            lb_new = tk.Listbox(frame2, listvariable=v2, width=18, height=10)
            lb_new.grid(row=0, column=0)
            scrollbar_2 = tk.Scrollbar(frame2, orient="v", command=lb_new.yview)
            lb_new['yscrollcommand'] = scrollbar_2.set
            scrollbar_2.grid(row=0, column=1, sticky=tk.NS)

            # メインのリストボックスを更新
            frame = tk.Frame(root)
            frame.place(x=285, y=43)

            v = tk.StringVar(value=FILTER_SET)
            self.listbox_main = tk.Listbox(frame, listvariable=v, width=20, height=15, relief=tk.RIDGE, bd=2)
            self.scrollbar_m = tk.Scrollbar(frame, orient="v", command=self.listbox_main.yview)
            self.listbox_main['yscrollcommand'] = self.scrollbar_m.set

            self.listbox_main.grid(row=0, column=0)
            self.scrollbar_m.grid(row=0, column=1, sticky=tk.NS)


    # 命令セット逐次実行
    def exe_action(self):
        global PT_FLAG
        PT_FLAG = 0
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
                    elif FILTER_SET[i] in {"減色"}:
                        print("減色")
                        fc.Loss(REAL_PATH)
                    elif FILTER_SET[i] in {"減色"}:
                        print("減色")
                        fc.Loss(REAL_PATH)
                    elif FILTER_SET[i] in {"ソーラライズ"}:
                        print("ソーラライズ")
                        fc.Solarize(REAL_PATH)
                    elif FILTER_SET[i] in {"ポスタライズ"}:
                        print("ポスタライズ")
                        fc.Posterize(REAL_PATH)
                    elif FILTER_SET[i] in {"イコライズ"}:
                        print("イコライズ")
                        fc.Equalize(REAL_PATH)
                    elif FILTER_SET[i] in {"回転(90度)"}:
                        print("回転(90度)")
                        fc.Rotate(REAL_PATH)
                    elif FILTER_SET[i] in {"平均化"}:
                        print("平均化")
                        fc.Average(REAL_PATH)
                    elif FILTER_SET[i] in {"メディアンフィルタ"}:
                        print("メディアンフィルタ")
                        fc.Median(REAL_PATH)
                    elif FILTER_SET[i] in {"ガウシアンフィルタ"}:
                        print("ガウシアンフィルタ")
                        fc.Gaussian(REAL_PATH)
                    elif FILTER_SET[i] in {"DoG"}:
                        print("DoG")
                        fc.DoG(REAL_PATH)
                    elif FILTER_SET[i] in {"一次微分(横)"}:
                        print("一次微分(横)")
                        fc.Diff_w(REAL_PATH)
                    elif FILTER_SET[i] in {"一次微分(縦)"}:
                        print("一次微分(縦)")
                        fc.Diff_h(REAL_PATH)
                    elif FILTER_SET[i] in {"Prewitt"}:
                        print("Prewitt")
                        fc.Prewitt(REAL_PATH)
                    elif FILTER_SET[i] in {"Sobel"}:
                        print("Sobel")
                        fc.Sobel(REAL_PATH)
                    elif FILTER_SET[i] in {"ラプラシアン"}:
                        print("ラプラシアン")
                        fc.Laplacian(REAL_PATH)
                    elif FILTER_SET[i] in {"ラプラシアン(PIL)"}:
                        print("ラプラシアン(PIL)")
                        fc.Laplacian_re(REAL_PATH)
                    elif FILTER_SET[i] in {"エンボス"}:
                        print("エンボス")
                        fc.Emboss(REAL_PATH)
                    elif FILTER_SET[i] in {"エンボス(PIL)"}:
                        print("エンボス(PIL)")
                        fc.Emboss_re(REAL_PATH)
                    elif FILTER_SET[i] in {"ごま塩ノイズ"}:
                        print("ごま塩ノイズ")
                        fc.Salt_Noise(REAL_PATH)
                    elif FILTER_SET[i] in {"ガウシアンノイズ"}:
                        print("ガウシアンノイズ")
                        fc.GaussianNoise(REAL_PATH)
                    elif FILTER_SET[i] in {"フーリエ変換"}:
                        print("フーリエ変換")
                        fc.FFT(REAL_PATH)
                    elif FILTER_SET[i] in {"ローパスフィルタ"}:
                        print("ローパスフィルタ")
                        fc.Lowpass(REAL_PATH)
                    elif FILTER_SET[i] in {"ハイパスフィルタ"}:
                        print("ハイパスフィルタ")
                        fc.Highpass(REAL_PATH)
                    elif FILTER_SET[i] in {"顔検出"}:
                        print("顔検出")
                        fc.Face_check(REAL_PATH)
                    elif FILTER_SET[i] in {"顔面モザイク"}:
                        print("顔面モザイク")
                        fc.Face_Moza(REAL_PATH)
                    elif FILTER_SET[i] in {"ヒデオ1"}:
                        print("Hideo")
                        fc.Hideo_1(REAL_PATH)
                    elif FILTER_SET[i] in {"ヒデオ2"}:
                        print("Hideo")
                        fc.Hideo_2(REAL_PATH)
                        PT_FLAG = 1
                    elif FILTER_SET[i] in {"FOXDIE"}:
                        print("FOXDIE")
                        fc.Foxdie(REAL_PATH)
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
                    elif FILTER_SET[i] in {"減色"}:
                        print("減色")
                        fc.Loss(O_REAL_PATH)
                    elif FILTER_SET[i] in {"ソーラライズ"}:
                        print("ソーラライズ")
                        fc.Solarize(O_REAL_PATH)
                    elif FILTER_SET[i] in {"ポスタライズ"}:
                        print("ポスタライズ")
                        fc.Posterize(O_REAL_PATH)
                    elif FILTER_SET[i] in {"イコライズ"}:
                        print("イコライズ")
                        fc.Equalize(O_REAL_PATH)
                    elif FILTER_SET[i] in {"回転(90度)"}:
                        print("回転(90度")
                        fc.Rotate(O_REAL_PATH)
                    elif FILTER_SET[i] in {"平均化"}:
                        print("平均化")
                        fc.Average(O_REAL_PATH)
                    elif FILTER_SET[i] in {"メディアンフィルタ"}:
                        print("メディアンフィルタ")
                        fc.Median(O_REAL_PATH)
                    elif FILTER_SET[i] in {"ガウシアンフィルタ"}:
                        print("ガウシアンフィルタ")
                        fc.Gaussian(O_REAL_PATH)
                    elif FILTER_SET[i] in {"DoG"}:
                        print("DoG")
                        fc.DoG(O_REAL_PATH)
                    elif FILTER_SET[i] in {"一次微分(横)"}:
                        print("一次微分(横)")
                        fc.Diff_w(O_REAL_PATH)
                    elif FILTER_SET[i] in {"一次微分(縦)"}:
                        print("一次微分(縦)")
                        fc.Diff_h(O_REAL_PATH)
                    elif FILTER_SET[i] in {"Prewitt"}:
                        print("Prewitt")
                        fc.Prewitt(O_REAL_PATH)
                    elif FILTER_SET[i] in {"Sobel"}:
                        print("Sobel")
                        fc.Sobel(O_REAL_PATH)
                    elif FILTER_SET[i] in {"ラプラシアン"}:
                        print("ラプラシアン")
                        fc.Laplacian(O_REAL_PATH)
                    elif FILTER_SET[i] in {"ラプラシアン(PIL)"}:
                        print("ラプラシアン(PIL)")
                        fc.Laplacian_re(O_REAL_PATH)
                    elif FILTER_SET[i] in {"エンボス"}:
                        print("エンボス")
                        fc.Emboss(O_REAL_PATH)
                    elif FILTER_SET[i] in {"エンボス(PIL)"}:
                        print("エンボス(PIL)")
                        fc.Emboss_re(O_REAL_PATH)
                    elif FILTER_SET[i] in {"ごま塩ノイズ"}:
                        print("ごま塩ノイズ")
                        fc.Salt_Noise(O_REAL_PATH)
                    elif FILTER_SET[i] in {"ガウシアンノイズ"}:
                        print("ガウシアンノイズ")
                        fc.GaussianNoise(O_REAL_PATH)
                    elif FILTER_SET[i] in {"フーリエ変換"}:
                        print("フーリエ変換")
                        fc.FFT(O_REAL_PATH)
                    elif FILTER_SET[i] in {"ローパスフィルタ"}:
                        print("ローパスフィルタ")
                        fc.Lowpass(O_REAL_PATH)
                    elif FILTER_SET[i] in {"ハイパスフィルタ"}:
                        print("ハイパスフィルタ")
                        fc.Highpass(O_REAL_PATH)
                    elif FILTER_SET[i] in {"顔検出"}:
                        print("顔検出")
                        fc.Face_check(O_REAL_PATH)
                    elif FILTER_SET[i] in {"顔面モザイク"}:
                        print("顔面モザイク")
                        fc.Face_Moza(O_REAL_PATH)
                    elif FILTER_SET[i] in {"ヒデオ1"}:
                        print("Hideo")
                        fc.Hideo_1(O_REAL_PATH)
                    elif FILTER_SET[i] in {"ヒデオ2"}:
                        print("Hideo")
                        fc.Hideo_2(O_REAL_PATH)
                        PT_FLAG = 1
                    elif FILTER_SET[i] in {"FOXDIE"}:
                        print("FOXDIE")
                        fc.Foxdie(O_REAL_PATH)
                    else:
                        print("ぶっこわれ")

            self.img_2 = ImageTk.PhotoImage(file=O_REAL_PATH)
            self.o_canvas.create_image(133, 134, image=self.img_2)

            if PT_FLAG == 1:
                self.do_PT()

        else:
            print("命令セットが組み込まれていません")


    # おまけ
    def do_PT(self):
        PT_win = tk.Toplevel(master=self.master)
        PT_win.title("204863")
        PT_win.geometry("1280x720+100+50")

        PT_l = ["./PT/PT_1.txt", "./PT/PT_2.txt", "./PT/PT_3.txt", "./PT/PT_4.txt"]

        str = random.choice(PT_l)
        PT_t = open(str, "r", encoding="utf-8")
        text_in = PT_t.read()

        if str == "./PT/PT_1.txt":
            canvas = tk.Canvas(PT_win, width=1280, height=720)
            canvas.create_rectangle(0, 0, 1280, 720, fill="black")
            canvas.pack(fill="x")
            label = tk.Label(PT_win, text=text_in, justify="left", foreground="white", background="black")
            label.place(x=40, y=50)
        elif str == "./PT/PT_2.txt":
            canvas = tk.Canvas(PT_win, width=1280, height=720)
            canvas.create_rectangle(0, 0, 1280, 720, fill="white")
            canvas.pack(fill="x")
            label = tk.Label(PT_win, text=text_in, justify="left", foreground="black", background="white")
            label.place(x=40, y=300)
        elif str == "./PT/PT_3.txt":
            canvas = tk.Canvas(PT_win, width=1280, height=720)
            canvas.create_rectangle(0, 0, 1280, 720, fill="gray")
            canvas.pack(fill="x")
            label = tk.Label(PT_win, text=text_in, justify="right", foreground="black", background="gray")
            label.place(x=700, y=50)
        elif str == "./PT/PT_4.txt":
            canvas = tk.Canvas(PT_win, width=1280, height=720)
            canvas.create_rectangle(0, 0, 1280, 720, fill="black")
            canvas.pack(fill="x")
            label = tk.Label(PT_win, text=text_in, justify="left", foreground="white", background="black")
            label.place(x=40, y=50)
        elif str == "./PT/PT_5.txt":
            canvas = tk.Canvas(PT_win, width=1280, height=720)
            canvas.create_rectangle(0, 0, 1280, 720, fill="yellow")
            canvas.pack(fill="x")
            label = tk.Label(PT_win, text=text_in, justify="left", foreground="black", background="yellow")
            label.place(x=10, y=10)


        PT_win.transient(self.master)
        PT_win.grab_set()
        PT_win.focus_set()

        PT_t.close()



# ひながた
if __name__ == "__main__":
    app = Application(master=root)
    app.pack()
    app.mainloop()
