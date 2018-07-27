# -*- coding: utf-8 -*-

# 実のところ、このプログラムは画像を読み込む時に一旦リサイズし、保存している。
# 新規のリサイズ画像は指定された絶対パスにある。

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
from PIL import Image, ImageFilter, ImageMath, ImageOps, ImageDraw, ImageFont
import random

# カレントディレクトリ取得
CD = os.getcwd()

# 出力絶対パス
O_REAL_PATH = os.path.join(CD, "output_img", "output_img.jpg")

# OpenCV
FACE_CASCADE_PATH = "/usr/local/Cellar/opencv/3.4.1_5/"\
                    "share/OpenCV/haarcascades/"\
                    "haarcascade_frontalface_default.xml"




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


def Gray(self):
    img = Image.open(self, 'r')
    gray = img.convert("L")
    gray.save(O_REAL_PATH, "JPEG", quality=100, optimize=True)
    img.close()

# 赤・緑・青 分解
def Red(self):
    img = Image.open(self)
    im_a = np.array(img)
    im_r = im_a.copy()
    im_r[:, :, (1, 2)] = 0

    red = Image.fromarray(im_r)
    red.save(O_REAL_PATH, "JPEG", quality=100, optimize=True)
    img.close()
    
def Green(self):
    img = Image.open(self)
    im_a = np.array(img)
    im_g = im_a.copy()
    im_g[:, :, (0, 2)] = 0

    green = Image.fromarray(im_g)
    green.save(O_REAL_PATH, "JPEG", quality=100, optimize=True)
    img.close()
    
def Blue(self):
    img = Image.open(self)
    im_a = np.array(img)
    im_b = im_a.copy()
    im_b[:, :, (0, 1)] = 0

    blue = Image.fromarray(im_b)
    blue.save(O_REAL_PATH, "JPEG", quality=100, optimize=True)
    img.close()


# 色交換(R <-> B)
def RtoB(self):
    img = Image.open(self)
    im_a = np.array(img)
    im_swap_rb = im_a.copy()
    im_swap_rb[:, :, 0] = im_a[:, :, 2]
    im_swap_rb[:, :, 2] = im_a[:, :, 0]

    rtob = Image.fromarray(im_swap_rb)
    rtob.save(O_REAL_PATH, "JPEG", quality=100, optimize=True)
    img.close()

# (R <-> G)
def RtoG(self):
    img = Image.open(self)
    im_a = np.array(img)
    im_swap_rg = im_a.copy()
    im_swap_rg[:, :, 1] = im_a[:, :, 2]
    im_swap_rg[:, :, 2] = im_a[:, :, 1]

    rtog = Image.fromarray(im_swap_rg)
    rtog.save(O_REAL_PATH, "JPEG", quality=100, optimize=True)
    img.close()

# (G <-> B)
def GtoB(self):
    img = Image.open(self)
    im_a = np.array(img)
    im_swap_gb = im_a.copy()
    im_swap_gb[:, :, 0] = im_a[:, :, 1]
    im_swap_gb[:, :, 1] = im_a[:, :, 0]

    gtob = Image.fromarray(im_swap_gb)
    gtob.save(O_REAL_PATH, "JPEG", quality=100, optimize=True)
    img.close()


# HSV 色相シフト
def HSV_h(self):
    img = Image.open(self, 'r')
    h, s, v = img.convert("HSV").split()
    _h = ImageMath.eval("(h + 128) % 255", h=h).convert("L")
    hsv_h = Image.merge("HSV", (_h, s, v)).convert("RGB")
    hsv_h.save(O_REAL_PATH, "JPEG", quality=100, optimize=True)
    img.close()

# HSV 彩度シフト
def HSV_s(self):
    img = Image.open(self, 'r')
    h, s, v = img.convert("HSV").split()
    _s = ImageMath.eval("(s + 128) % 255", s=s).convert("L")
    hsv_s = Image.merge("HSV", (h, _s, v)).convert("RGB")
    hsv_s.save(O_REAL_PATH, "JPEG", quality=100, optimize=True)
    img.close()

# HSV 明度シフト
def HSV_v(self):
    img = Image.open(self, 'r')
    h, s, v = img.convert("HSV").split()
    _v = ImageMath.eval("(v + 128) % 255", v=v).convert("L")
    hsv_v = Image.merge("HSV", (h, s, _v)).convert("RGB")
    hsv_v.save(O_REAL_PATH, "JPEG", quality=100, optimize=True)
    img.close()


# 明るく
def Bright(self):
    img = Image.open(self, 'r')
    img_b = img.point(lambda x: x * 1.5)
    img_b.save(O_REAL_PATH, "JPEG", quality=100, optimize=True)
    img.close()
    

# 暗く
def Dark(self):
    img = Image.open(self, 'r')
    img_d = img.point(lambda x: x * 0.5)
    img_d.save(O_REAL_PATH, "JPEG", quality=100, optimize=True)
    img.close()


# ガンマ補正
def Gamma(self):
    img = Image.open(self, 'r')

    def gamma_table(g_r, g_g, g_b, gain_r=1.0, gain_g=1.0, gain_b=1.0):
        r_t = [min(255, int((x / 255.) ** (1. /g_r) * gain_r * 255.)) for x in range(256)]
        g_t = [min(255, int((x / 255.) ** (1. /g_g) * gain_g * 255.)) for x in range(256)]
        b_t = [min(255, int((x / 255.) ** (1. /g_b) * gain_b * 255.)) for x in range(256)]
        return r_t + g_t + b_t

    img_g = img.point(gamma_table(1.2, 0.5, 0.5))
    img_g.save(O_REAL_PATH, "JPEG", quality=100, optimize=True)
    img.close()


# セピア
def Sepia(self):
    img = Image.open(self, 'r')
    gray_img = img.convert("L")

    sepia = Image.merge(
        "RGB",
        (
            gray_img.point(lambda x: x * 240 / 255),
            gray_img.point(lambda x: x * 200 / 255),
            gray_img.point(lambda x: x * 145 / 255)
        )
    )

    sepia.save(O_REAL_PATH, "JPEG", quality=100, optimize=True)
    img.close()
    

# モザイク
def Moza(self):
    img = Image.open(self, 'r')
    pix = img.resize([x // 8 for x in img.size]).resize(img.size)
    pix.save(O_REAL_PATH, "JPEG", quality=100, optimize=True)
    img.close()


# ネガポジ反転
def NegaPosi(self):
    img = Image.open(self, 'r')
    im_np = ImageOps.invert(img)
    im_np.save(O_REAL_PATH, "JPEG", quality=100, optimize=True)
    img.close()


# ミラー
def Mirror(self):
    img = Image.open(self, 'r')
    im_m = ImageOps.mirror(img)
    im_m.save(O_REAL_PATH, "JPEG", quality=100, optimize=True)
    img.close()


# 減色
def Loss(self):
    img = Image.open(self, 'r')
    im_a = np.array(img)

    im_32 = im_a // 32 * 32
    
    im_los = Image.fromarray(im_32)
    im_los.save(O_REAL_PATH, "JPEG", quality=100, optimize=True)
    img.close()


# ソーラライズ
def Solarize(self):
    img = Image.open(self, 'r')
    im_s = ImageOps.solarize(img, 127)
    im_s.save(O_REAL_PATH, "JPEG", quality=100, optimize=True)
    img.close()


# ポスタライズ
def Posterize(self):
    img = Image.open(self, 'r')
    im_p = ImageOps.posterize(img, 2)
    im_p.save(O_REAL_PATH, "JPEG", quality=100, optimize=True)
    img.close()


# イコライズ
def Equalize(self):
    img = Image.open(self, 'r')
    im_e = ImageOps.equalize(img)
    im_e.save(O_REAL_PATH, "JPEG", quality=100, optimize=True)
    img.close()


# アフィン変換(90度)
def Rotate(self):
    img = Image.open(self, 'r')
    r90 = img.rotate(90, expand=True)
    r90.save(O_REAL_PATH, "JPEG", quality=100, optimize=True)
    img.close()


# 平均化(1/9)
def Average(self):
    img = cv2.imread(self)

    # カーネル
    kernel = np.array([[1/9, 1/9, 1/9],
                       [1/9, 1/9, 1/9],
                       [1/9, 1/9, 1/9]])
    
    dst2 = cv2.filter2D(img, -1, kernel)

    cv2.imwrite(O_REAL_PATH, dst2)


# メディアンフィルタ
def Median(self):
    img = cv2.imread(self)

    # メディアン(カーネルサイズ)
    dst2 = cv2.medianBlur(img, ksize=5)

    cv2.imwrite(O_REAL_PATH, dst2)


# ガウシアンフィルタ
def Gaussian(self):
    img = cv2.imread(self)

    # カーネル
    kernel = np.array([[1/16, 1/8, 1/16],
                       [1/8, 1/4, 1/8],
                       [1/16, 1/8, 1/16]])

    dst2 = cv2.filter2D(img, -1, kernel)

    cv2.imwrite(O_REAL_PATH, dst2)


# DoG
def DoG(self):
    def dog_12(gray, kernel, sigma1, sigma2):
        g1 = cv2.GaussianBlur(gray, kernel, sigma1)
        g2 = cv2.GaussianBlur(gray, kernel, sigma2)

        return g1 - g2

    img = cv2.imread(self)

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    dst = dog_12(gray, (3, 3), 1.5, 3.0)

    cv2.imwrite(O_REAL_PATH, dst)


# Bilateral
def Bilateral(self):
    img = cv2.imread(self)

    dst = cv2.bilateralFilter(img, 15, 20, 20)

    cv2.imwrite(O_REAL_PATH, dst)


# Nonlocalmean
def Nonlocal(self):
    img = cv2.imread(self)

    dst = cv2.fastNlMeansDenoisingColored(img,None,10,10,5,16)

    cv2.imwrite(O_REAL_PATH, dst)


# 一次微分(横)
def Diff_w(self):
    img = cv2.imread(self)

    kernel = np.array([[0, 0, 0],
                       [-1, 0, 1],
                       [0, 0, 0]])

    dst2 = cv2.filter2D(img, -1, kernel)

    cv2.imwrite(O_REAL_PATH, dst2)


# 一次微分(縦)
def Diff_h(self):
    img = cv2.imread(self)

    kernel = np.array([[0, -1, 0],
                       [0, 0, 0],
                       [0, 1, 0]])

    dst2 = cv2.filter2D(img, -1, kernel)

    cv2.imwrite(O_REAL_PATH, dst2)


# Prewitt
def Prewitt(self):
    img = cv2.imread(self)

    kernel = np.array([[-1, 0, 1],
                       [-1, 0, 1],
                       [-1, 0, 1]])

    dst2 = cv2.filter2D(img, -1, kernel)

    cv2.imwrite(O_REAL_PATH, dst2)


# Sobel
def Sobel(self):
    img = cv2.imread(self)

    kernel = np.array([[-1, 0, 1],
                       [-2, 0, 2],
                       [-1, 0, 1]])

    dst2 = cv2.filter2D(img, -1, kernel)

    cv2.imwrite(O_REAL_PATH, dst2)


# ラプラシアン
def Laplacian(self):
    img = cv2.imread(self)
    
    kernel = np.array([[1, 1, 1],
                       [1, -8, 1],
                       [1, 1, 1]])

    dst2 = cv2.filter2D(img, -1, kernel)

    cv2.imwrite(O_REAL_PATH, dst2)


# PIL(CONTOUR)
def Laplacian_re(self):
    img = Image.open(self, 'r')
    
    im_l = img.filter(ImageFilter.CONTOUR)

    im_l.save(O_REAL_PATH, "JPEG", quality=100, optimize=True)
    img.close()


# エンボス
def Emboss(self):
    img = cv2.imread(self)

    kernel = np.array([[-2, -1, 0],
                       [-1, 1, 1],
                       [0, 1, 2]])

    offs = 128

    dst2 = cv2.filter2D(img, -1, kernel, delta=offs)

    cv2.imwrite(O_REAL_PATH, dst2)


# エンボス(PIL)
def Emboss_re(self):
    img = Image.open(self, 'r')

    im_e = img.filter(ImageFilter.EMBOSS)

    im_e.save(O_REAL_PATH, "JPEG", quality=100, optimize=True)
    img.close()
    

# ごま塩
def Salt_Noise(self):

    def sn_add(img, p):
        output = np.zeros(img.shape, np.uint8)
        thres = 1 - p
        
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                rdn = random.random()
                
                if rdn < p:
                    output[i][j] = 0
                elif rdn > thres:
                    output[i][j] = 255
                else:
                    output[i][j] = img[i][j]

        return output

    img = cv2.imread(self)
    img_n = sn_add(img, 0.05)
    cv2.imwrite(O_REAL_PATH, img_n)


# ガウシアンノイズ
def GaussianNoise(self):

    def addGauNoi(img):
        row, col, ch = img.shape
        mean = 0
        var = 0.1
        sigma = 15

        gauss = np.random.normal(mean, sigma, (row, col, ch))
        gauss = gauss.reshape(row, col, ch)

        img_n = img + gauss

        return img_n

    
    img = cv2.imread(self)
    im_gn = addGauNoi(img)
    cv2.imwrite(O_REAL_PATH, im_gn)


# FFT
def FFT(self):
    global FFT_FLAG
    img = cv2.imread(self)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 高速フーリエ変換
    fimg = np.fft.fft2(gray)
    # 各象限の入れ替え
    fimg = np.fft.fftshift(fimg)
    # パワースペクトル
    mag = 20*np.log(np.abs(fimg))

    cv2.imwrite(O_REAL_PATH, mag)
    
    
# ローパス
def Lowpass(self):
    img = cv2.imread(self)

    def low(img, a=0.5):
        src = np.fft.fft2(img)
        
        h, w = img.shape
        
        cy, cx = int(h/2), int(w/2)
        
        rh, rw = int(a*cy), int(a*cx)

        fsrc = np.fft.fftshift(src)
        fdst = np.zeros(src.shape, dtype=complex)

        fdst[cy-rh:cy+rh, cx-rw:cx+rw] = fsrc[cy-rh:cy+rh, cx-rw:cx+rw]

        fdst = np.fft.fftshift(fdst)

        dst = np.fft.ifft2(fdst)

        return np.uint8(dst.real)

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    limg = low(gray, 0.3)

    cv2.imwrite(O_REAL_PATH, limg)


# ハイパス
def Highpass(self):
    img = cv2.imread(self)
    
    def high(img, a=0.5):
        src = np.fft.fft2(img)
        
        h, w = img.shape
        
        cy, cx = int(h/2), int(w/2)
        
        rh, rw = int(a*cy), int(a*cx)

        fsrc = np.fft.fftshift(src)
        
        fdst = fsrc.copy()
        
        fdst[cy-rh:cy+rh, cx-rw:cx+rw] = 0

        fdst = np.fft.fftshift(fdst)

        dst = np.fft.ifft2(fdst)

        return np.uint8(dst.real)

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    himg = high(gray, 0.8)

    cv2.imwrite(O_REAL_PATH, himg)
    

# 顔検出
def Face_check(self):
    img = cv2.imread(self)

    cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)
    im_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(im_g)

    # 顔の部分に矩形
    for x, y, w, h in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face = img[y: y + h, x: x + w]
        face_gray = im_g[y: y + h, x: x + w]

    cv2.imwrite(O_REAL_PATH, img)


# 顔にモザイク
def Face_Moza(self):
    img = cv2.imread(self)

    ratio = 0.05
    cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)
    im_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(im_g)

    # 顔の部分だけモザイク
    for x, y, w, h in faces:
        small = cv2.resize(img[y: y + h, x: x + w], None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
        img[y: y + h, x: x + w] = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)

    cv2.imwrite(O_REAL_PATH, img)


# Hideo 1
def Hideo_1(self):
    fontsize = 22
    font_d = "/Users/nyanten/Library/Fonts/EXO-Bold.otf"
    img = Image.open(self, 'r')

    x = 180
    y = 16
    text = "Hideo 1"

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_d, fontsize)
    draw.text((x, y), text, font=font, fill=(0, 255, 0, 0))

    img.save(O_REAL_PATH, "JPEG", quality=100, optimize=True)
    img.close()
    

# Hideo 2
def Hideo_2(self):
    fontsize = 22
    font_d = "/Users/nyanten/Library/Fonts/JNR-SB-Font.otf"
    img = Image.open(self, 'r').convert('L')
    im_n = np.array(img)

    t = 128
    im_bool = im_n > t
    h, w = im_n.shape

    im_dst = np.empty((h, w, 3))
    
    r, g, b = 128, 160, 192
    
    im_dst[:, :, 0] = im_bool * r
    im_dst[:, :, 1] = ~im_bool * g
    im_dst[:, :, 2] = im_bool * b
    
    im_2 = Image.fromarray(np.uint8(im_dst))
    im_2.save(O_REAL_PATH, "JPEG", quality=100, optimize=True)
    img.close()
    

# FOX DIE
def Foxdie(self):
    img = Image.open(self, 'r')
    
    im_np = ImageOps.invert(img)

    h, s, v = im_np.convert("HSV").split()
    _s = ImageMath.eval("(s + 128) % 255", s=s).convert("L")
    hsv_s = Image.merge("HSV", (h, _s, v)).convert("RGB")

    im_s = ImageOps.solarize(hsv_s, 127)

    im_s.filter(ImageFilter.GaussianBlur(1.5))

    img_b = im_s.point(lambda x: x * 1.5)
    img_b.save(O_REAL_PATH, "JPEG", quality=100, optimize=True)
    img.close()


# お好きな処理を組み込む際は以下にどうぞ
#def sample(self):
    # 読み込み
    # Pillow
    # img = Image.open(self, 'r')
    # OpenCV
    # img = cv2.imread(self)

    
    #
    # 処理をかく
    #


    # 書き込み
    # output.save(O_REAL_PATH) 
    # cv2.imwrite(O_REAL_PATH, output)


