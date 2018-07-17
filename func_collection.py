# -*- coding: utf-8 -*-

# 実のところ、このプログラムは画像を読み込む時に一旦リサイズし、保存している。
# 新規のリサイズ画像は指定された絶対パスにある。

# 絶対パスはわかっちゃっているため、プログラムを楽に組み込むならこっち。
# 但し、環境を変えたりファイルの置き場所によってはエラーになるので注意。
# REAL_PATH = "/Users/nyanten/Documents/Documents /killtime2/RealPython/OC/resize_picture/import_pic.jpg"

# 前提知識
# 画像は画素(ピクセル)という単位の細かな正方形でできている。
# 色の表現は、赤・緑・青の色の組み合わせで構成されている。
# このピクセルがたくさんあって画像一枚が成り立っている。
# カラー画像の場合、赤・緑・青の濃度を0~255の256階調で表現する。
# グレイスケール(白と黒の濃淡を表現した画像)は、0~255(0=黒, 127=灰, 255=白)となる。


# パッケージ
import sys, os
import cv2
import numpy as np


# 出力パス
O_REAL_PATH = "/Users/nyanten/Documents/Documents /killtime2/RealPython/OC/output_img/output_img.jpg"


# ２値化処理
def Binary(self):
    print(self)

    # しきい値
    t = 127

    # 読み込んだ画像の読み込み
    img = cv2.imread(self)

    # グレイスケール
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 出力(行列)
    output_img = gray.copy()

    # しきい値で色分け
    output_img[gray < t] = 0
    output_img[gray > t] = 255

    # 結果
    cv2.imwrite(O_REAL_PATH, output_img)


def Blue(self):
    img = cv2.imread(self)
    c1 = cv2.split(img)
    blue = c1[0]

    cv2.imwrite(O_REAL_PATH, blue)


    


def Rotate(self):
    img = cv2.imread(self)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 回転角・拡大率
    theta = 90
    scale = 1.0

    # 中心座標
    cy, cx = int(gray.shape[0]/2), int(gray.shape[1]/2)

    # 回転変換行列の算出
    R = cv2.getRotationMatrix2D((cx, cy), theta, scale)

    # アフィン変換
    dst = cv2.warpAffine(gray, R, gray.shape, flags=cv2.INTER_CUBIC)

    # 出力
    cv2.imwrite(O_REAL_PATH, dst)


    
    
    
