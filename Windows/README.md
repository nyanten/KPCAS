# KrProCessAS (Kr-ProCesser Assembly System)
　　　　　Build now(beta)
　　　　　*ようこそ*

## 概要
Windows用にウィンドウサイズなどをいじったバージョン。
Macで作業していたものとの違いは以下の通り。

- .txtファイルを読み込む際、utf-8 にエンコードするようにした。
- 保存の仕方を変更。アプリを一旦閉じると上書きされる。
- .exeファイルの配布。環境によっては動かない可能性あり。
- カメラモジュールを使っての画像撮影は未実装。

## PyInstaller を使ったビルド方法
`pip install pyinstaller` でダウンロード。  

ダウンロード後、ソースコードを以下のように入力して.exeを作成する。  

`pyinstaller -F -w ***.py`

`--iconfile=hoge.ico` でアプリアイコンを指定できる。  

distディレクトリが作成され、そこに.exeファイルが作られる。

[こちらを参考](http://edosha.hatenablog.jp/entry/2017/05/11/121204)にした。
ここの方がおっしゃっているように、環境に依存しまくりなので.exeはうまく実行できないかもしれない。

## 作業環境
<dl>
  <dt>EPSON MR7300E-L</dt>
  <dd>OS: Windows 10 Pro</dd>
  <dd>Proessor: Intel(R) Core(TM) i7-4790K CPU 4.00GHz</dd>
  <dd>Memory: 16GB</dd>
  <dt>Edit</dt>
  <dd>Atom 1.28.2 x64</dd>
  <dt>Python</dt>
  <dd>Python 3.6.5</dd>
  <dd>tkinter ver8.5</dd>
  <dt>use package(Package Manager is pip)</dt>
  <dd>OpenCV ver3.4.1</dd>
  <dd>Numpy ver1.15.0</dd>
  <dd>Pillow ver5.2.0</dd>
  <dd>PyInstaller 3.3.1</dd>
</dl> 