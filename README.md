# KrProCessAS (Kr-ProCesser Assembly System)

Ver0.50  
　　　　　*ようこそ*

## 概要
誰でも簡単に画像処理を行えるアプリ作成を目指す。  
あらかじめ準備された命令セットを好きなように組み込み、実行した結果から期待したものが得られているかどうかを最重要事項とする。

着想・発想はNintendoDSのゲーム、メイドイン俺(2009 - INTELLIGENT SYSTEMS)から。

## できること
簡単な画像処理ができ、処理過程を組み込める。  
また、命令セットとそのマニュアルを比較して実装することで、画像処理の基本を学習できる。

### 一連の使い方例
1. 画像を開く  
2. 命令セットを開く
3. 好きな命令を組み込む  
4. Quitボタンでメインウィンドウに戻る 
5. 実行を押すと、組み込んだ順に画像処理が施され、結果画像が得られる

カメラ起動ボタンを押すと、カメラモジュールを開くことができる。  
Spaceキーで撮影。escキーで終了。
カメラ起動時はアプリを操作できないので注意。

## 命令セット
命令の中身は `func_collection.py` に記述。  
命令セットは以下の通り。(**太字は未実装**)
参考は[こっち](https://qiita.com/pashango2/items/145d858eff3c505c100a)

- 2値化
- グレイスケール
- 赤・緑・青分解
- 色交換
- HSV色空間(色相・彩度・明度シフト)
- 明暗変化(1.5倍明るく/0.5倍暗く)
- ガンマ補正
- セピア
- モザイク
- ネガポジ反転
- ミラー
- 減色
- ソーラライズ
- ポスタライズ
- イコライズ
- 回転
- 平均化
- メディアンフィルタ
- ガウシアンフィルタ
- バイラテラル
- ノンローカルミーン
- 一次微分(横・縦)
- Prewitt
- Sobel
- ラプラシアン
- エンボス
- アンシャープマスキング
- ごま塩ノイズ
- ガウシアンノイズ
- フーリエ変換
- ローパスフィルタ
- ハイパスフィルタ
- 顔検出
- 顔面モザイク

そのほか。

`func_collection.py` をいじれば命令を追加できる。
自由に組み込んでください。  


## 命令セット概要
[wiki](https://github.com/nyanten/KPCAS/wiki/Image-Processing)をみてくだし。


## 環境構築(macOS)
Python3.6.5は[Pythonの公式サイト](https://www.python.org/downloads/)からダウンロード。  
macOSの場合、デフォルトでPython2.xがインストールされている。
ターミナルで `python` と入力してバージョン情報、  
`which python` と入力して場所を確認する。  

Python3.6.5以外の動作は確認していないが、Python3.x.xより後のバージョンならばおそらく問題ない。  

パッケージの管理にはpipを用いた。Pythonをインストールした時にデフォルトでインストールされる。  

macOSにはデフォルトで入っていない、あるいはすでに入っているかのどちらかである。  
ターミナルで `pip --version` と入力して、入っているなら **Python2.xのpip** が入っていることになる。  
Python3.xを後からインストールした場合は、`pip3` となることがあるため、注意。

### 追記:8/6
MacにはPython2.xがデフォルトでインストールされている以上、Python3.xの環境を新たに構築する場合、pyenvを使うことを進める。

今回、この製作物を作るにあたり、Pythonの実行環境変化による動作不良を考慮して、pyenvを使うことはなかった。別バージョンのPythonを使う際にはpyenvによるバージョン管理を推奨する。

## Windows用ソース 2018/7/25 追加
別環境のWindowsにてPyInstallerを用いたところ、実行ファイルを作成できた。
[Windowsファイル](https://github.com/nyanten/KPCAS/tree/master/Windows)に入っている。Windows環境に合わせて作り直してあるため、環境さえ整って入ればおそらく動作する。  

以下、Windowsでの環境構築。  

### Windows 環境構築
Python公式サイトから、[Python3.6.5のインストーラをダウンロード](https://www.python.org/ftp/python/3.6.5/python-3.6.5-amd64.exe)する。  
既にPythonがインストールされている場合はそのままでもよいと思われる。
別に3.6.5じゃなくてもいい。  

Pythonのインストーラを起動して、お好みの場所にインストールする。  

次に、OpenCVを導入するが、[次の非公式サイト](https://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv)からダウンロードする。  
OpenCVの項目から、`opencv python-3.4.2-cp36-cp36m-win amd64.whl` を選択。  
適宜、自分にあったものをダウンロードする。  

opencv python-XXX-cpYY-cpYYm-win ZZZZ.whl  
- X: OpenCVのバージョン
- Y: Pythonのバージョン
- Z: 使用PCのCPUビット数

CPUはコントロールパネルなどから確認できる。  

次に、Windowsのコマンドプロンプトを起動する。
`python pip install --upgrade pip` と入力してpipをアップグレードする。  
このコマンドでアップグレードされない場合は、`pip list` とでも入力すればわかる。  
オレンジ色で警告文が出てくると思うので、その通りにすればアップグレードできる。

`pip install numpy` と入力してNumpyを導入する。
OpenCVはNumpy必須となっているので注意。  
`pip install Pillow` と入力してPILを導入する。  

`cd Downloads` で先ほどダウンロードした `opencv python-3.4 ....` のあるところに移動する。  
`pip install opencv python-3.4.2-cp36-cp36m-win amd64.whl` と入力。

完了後、`pip list` で必要項目がインストールされているかチェック。  

そして、 `python` と入力。pythonが立ち上がるので、  

```
>>> import cv2
>>> 
```

と入力して、cv2がインポートできているか確認する。  

`python KPCAS_beta.py` でEnterを押すと起動する。

## ~py2app を使ったビルドメモ~
~setup.pyをそのまんまmakeしたが、うまくいかずsetupのみで構成したファイルを実行。~  
~以下、ビルドするための実行コマンド。アイコンを埋め込むため、--iconfileで指定。~  

~python3 setup.py py2app --iconfile test.icns~

py2appはPython3.5くらいまでしか対応していないらしい。

### QRコードについて
こちらは未実装。
出力結果画像を携帯端末でお手軽に読み込めるようにしようとしたが...

あたりまえのことだが、画像データがQRコードに収まるわけがない。

Dropboxなどに保存してURLをはっつけようとも考えたが、
画像データをほいほいとネットに上げるのは危険すぎると判断。

何かしら応用できるといい。

## 参考
[Tkinterの基本はこちら](https://qiita.com/nnahito/items/41be8e02a6ebc91386e7)  
[ファイル参照方法](http://spcx8.hatenablog.com/entry/2017/12/24/112528)


## 作業環境
<dl>
  <dt>MacBook Air Early 2015</dt>
  <dd>OS: macOS High Sierra ver10</dd>
  <dd>Proessor: 1.6Ghz Intel Core i5</dd>
  <dd>Memory: 8GB 1600 MHz DDR3</dd>
  <dt>Edit</dt>
  <dd>Emacs Version 25.2 (9.0)</dd>
  <dt>Python</dt>
  <dd>Python 3.6.5</dd>
  <dd>tkinter ver8.5</dd>
  <dt>use package(Package Manager is pip)</dt>
  <dd>OpenCV ver3.4.1</dd>
  <dd>Numpy ver1.14.3</dd>
  <dd>Pillow ver5.1.0</dd>
  <dd>py2app ver0.14</dd>
</dl> 