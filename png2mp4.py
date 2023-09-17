import cv2
import os
import glob
import argparse
import re
import sys
import numpy as np

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


def png2mp4(input_path, output_path, background_color, threshold=0):
    # 指定されてパスからpngファイルを読み取りソート
    pathes = glob.glob(input_path + "*.png")
    pathes.sort(key=natural_keys)
    
    height, width, layers = cv2.imread(pathes[0]).shape
    size = (width, height)
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), 60, size)
    
    for path in pathes:
        # ファイル名からn(画像の順番)とm(画像のフレーム数)を取得
        image = cv2.imread(path, -1)
        # 透明部分を変色
        idxes = np.where(image[:,:,3] <= threshold)
        image[idxes] = background_color
        # RGBAからRGBに変換
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        file_name = (os.path.split(path)[1]).replace(".png", "")
        n = int(file_name.split("_")[0])
        m = int(file_name.split("_")[1])
        for _ in range(m):
            out.write(image)
    
    out.release()
    
    

if (__name__ == "__main__"):
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("input_path", help="画像が入っているディレクトリのパス", type=str)
    parser.add_argument("-o", "--output_path", help="出力先のパスと名前", type=str, default="./anime.mp4")
    parser.add_argument("-t", "--transparent_threshold", help="透明度が強い部分を完全に透過します", type=int, default=0)
    parser.add_argument("-c", "--color", choices=["blue", "green", "red"], default="green")

    args = parser.parse_args()

    if(not os.path.isdir(args.input_path)):
        print("Not found directory!")
        sys.exit(1)

    background_color = (255,255,255,255)
    if(args.color == "blue"):
        background_color = (255,0,0,255)
    elif(args.color == "green"):
        background_color = (0,255,0,255)
    elif(args.color == "red"):
        background_color = (0,0,255,255) 

    png2mp4(args.input_path, args.output_path, background_color, args.transparent_threshold)