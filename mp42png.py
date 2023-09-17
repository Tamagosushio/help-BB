import cv2
import os
import argparse
import numpy as np
import sys


def mp42png(input_path, output_path="./pngs", threshold=0):
    if(not os.path.isfile(input_path)):
        print("Not found video file!")
        sys.exit(1)
    cap = cv2.VideoCapture(input_path)
    os.makedirs(output_path, exist_ok=True)
    images = []
    while (True):
        ret, frame = cap.read()
        if ret:
            images.append(frame)
        else:
            break
    
    n = 0
    m = 1
    i = 0
    for i in range(len(images) - 1):
        im_diff = images[i].astype(int) - images[i+1].astype(int)
        print(n)
        if(np.array_equal(images[i], images[i+1]) or (abs(im_diff.max()) + abs(im_diff.min()) <= threshold)):
            m += 1
        else:
            cv2.imwrite(f"{output_path}/{n}_{m}.png", images[i])
            n += 1
            m = 1
    cv2.imwrite(f"{output_path}/{n}_{m}.png", images[i])

        


if (__name__=="__main__"):
    
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="変換を行う動画ファイルのパス", type=str)
    parser.add_argument("-t", "--threshold", help="どのくらいの違いまで同一画像と見なすかの程度", type=int, default=0)
    parser.add_argument("-o", "--output_path", help="出力先", type=str, default="./png/")

    args = parser.parse_args()

    mp42png(args.input_path, args.output_path,  args.threshold)
