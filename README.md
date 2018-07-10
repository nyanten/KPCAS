# Hello.
This is test upload.

# py2app を使ったビルドメモ
setup.pyをそのまんまmakeしたが、うまくいかずsetupのみで構成したファイルを実行  
以下、ビルドするための実行コマンド。アイコンを埋め込むため、--iconfileで指定。

`python3 setup.py py2app --iconfile test.icns` 

## 参考
[Tkinterの基本はこちら](https://qiita.com/nnahito/items/41be8e02a6ebc91386e7)  
[ファイル参照方法](http://spcx8.hatenablog.com/entry/2017/12/24/112528)


## 作業環境
<dl>
  <dt>MacBook Air Early 2015</dt>
  <dd>OS: macOS High Sierra ver10</dd>
  <dd>Proessor: 1.6Ghz Intel Core i5</dd>
  <dd>Memory: 8GB 1600 MHz DDR3</dd>
  <dt>Python</dt>
  <dd>Python 3.6.5</dd>
  <dd>tkinter ver8.5</dd>
  <dt>use package(Package Manager is pip)</dt>
  <dd>OpenCV ver3.4.1</dd>
  <dd>Numpy ver1.14.3</dd>
  <dd>Pillow ver5.1.0</dd>
  <dd>py2app ver0.14</dd>
</dl> 