from PIL import Image
import glob
import os
import numpy as np
import cv2
import re
import argparse

# https://qiita.com/derodero24/items/f22c22b22451609908ee
def pil2cv(image):
    ''' PIL型 -> OpenCV型 '''
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image

def cv2pil(image):
    ''' OpenCV型 -> PIL型 '''
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
    return new_image


# imageはOpenCV型
def to_transparent(image, transparent):
    idxes = np.where(image[:,:,3] <= transparent)
    image[idxes][3] = 0


def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


def png2gif(dir_path, output_path="./anime.gif", size_magnification=1.0, transparent=0):
    # 画像配列
    pictures = []
    # 指定されてパスからpngファイルを読み取りソート
    pathes = glob.glob(dir_path + "*.png")
    pathes.sort(key=natural_keys)
    # 画像を表示させる時間の配列
    frames_num = []
    # 1枚ずつ画像を処理
    for path in pathes:
        # ファイル名からn(画像の順番)とm(画像のフレーム数)を取得
        file_name = (os.path.split(path)[1]).replace(".png", "")
        n = int(file_name.split("_")[0])
        m = int(file_name.split("_")[1])
        # cv2で画像を読み込み透過処理
        image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        to_transparent(image, transparent)
        # pil型に画像を変換
        image = cv2pil(image)
        
        # マスクを使って透過処理
        alpha = image.split()[3]
        image = image.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        mask = Image.eval(alpha, lambda a:255 if a <= 127 else 0)
        image.paste(255, mask=mask)
        # リサイズ
        image = image.resize(
            (int(image.width * size_magnification), int(image.height * size_magnification))
        )
        # 画像とフレーム数配列に追加
        pictures.append(image)
        frames_num.append(m)
    # 60fpsであるのでフレーム数から時間を計算
    # 20ms未満でだとdurationが正しく動作しない
    durations = [20.0 if(frame*1000/60 < 20.0) else (frame*1000/60) for frame in frames_num]
    print(durations)
    print(sum(durations))
    pictures[0].save(
        output_path, 
        save_all=True, 
        append_images=pictures[1:],
        optimize=False, 
        duration=durations,
        loop=0, 
        transparency=255,
        disposal=2
    )
    print("completed!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="画像が入っているディレクトリのパス", type=str)
    parser.add_argument("-o", "--output_path", help="出力先のパスと名前", type=str, default="./anime.gif")
    parser.add_argument("-s", "--size_magnification", help="画像の拡大縮小倍率", type=float, default=1.0)
    parser.add_argument("-t", "--transparent_threshold", help="透明度が強い部分を完全に透過します", type=int, default=0)
    
    args = parser.parse_args()

    png2gif(args.input_path, args.output_path, args.size_magnification, args.transparent_threshold)