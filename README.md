# help-BB
BB素材や透過GIFの作成を補助します。
## Requirement
- opencv-python     4.6.0.66
- numpy             1.23.3
- Pillow            9.3.0
## Installation
```sh
pip3 install opencv-python
pip3 install numpy
pip3 install Pillow
```
## Usage
```sh
python3 mp42png.py ./hoge/fuga.mp4 -o ./hoge/fuga -t 30
#
# 生成された画像ファイルを透過する
#
python3 png2gif.py ./hoge/fuga -o ./hoge/fuga.gif -s 0.5 -t 127
python3 png2mp4.py ./hoge/fuga -o ./hoge/bb_fuga.mp4 -c blue -t 63
```
## Note
- ディレクトリ名やファイル名に日本語が入っていると正常に動かない可能性があります。
- png2gif.pyでgifを作成する際、1フレームの画像は表示時間が20msになります。<br>
  これはPillowの仕様上、短すぎると正常にgifが生成されなくなるからです。
## mp42png.py
### option
- input_path : 変換を行う動画ファイルのパス。
- -o (--output_path) : 出力するディレクトリのパス。存在しなければ作成する。(default: ./pngs)
- -t (--threshold) : 次フレームと同一画像をみなすかの閾値。 (default: 0)
## png2gif.py
### option
- input_path: 変換を行うpngファイルが入ったディレクトリのパス。
- -o (--output_path) : 出力するファイルのパス。(default: ./anime.gif)
- -s (--size_magnification) : 画像の倍率。(default: 1.0)
- -t (--transparent_threshold) : この値以下の透明度部分は完全に透明化する。(default: 0)
## png2mp4.py
### option
- input_path: 変換を行うpngファイルが入ったディレクトリのパス。
- -c (--color) : blue,green,redのいずれかを指定して、BB,GB,RB素材化する。(defualt: 白色)
- -t (--transparent_threshold) : この値以下の透明度部分は完全に透明化する。(default: 0)
