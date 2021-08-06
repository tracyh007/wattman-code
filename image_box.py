# --*-- coding:utf-8 --*--

"""
@author: chenjun
@file: image_box.py
@time: 2021/8/6
@desc: question 1
"""
import os
import cv2
import json
import argparse


def print_name(file_path):
    """
    question 1.1 将json文件里面的name为"box_b"的“rectangle”字段打印出来。
    Args:
        file_path: file path
    Returns:
        bbox: box_b bbox
    """

    if not os.path.exists(file_path):
        raise ValueError("file path not exist, please check !")

    file_ = open(file_path)
    # get json file
    box = json.load(file_)
    # get bbox
    bbox = box['boxes'][1]['rectangle']
    # print
    print(bbox)
    return bbox


def image_fill(image_file, mask_image, bbox, model="keep"):
    """
    question 1.2 将任意一张图像填充到另一张图像的box_b所指定的区域中
    Args:
        image_file: image file path.
        mask_image: mask image file path.
        bbox: image bbox pos.
        model: "keep" or "draw".
    Returns:
        image
    """
    # read image
    image = cv2.imread(image_file)
    image_mask = cv2.imread(mask_image)

    # mask image height, width
    mask_h = image_mask.shape[0]
    mask_w = image_mask.shape[1]

    # The pos in image_1
    x1, y1 = bbox['left_top']
    x2, y2 = bbox['right_bottom']
    width = x2 - x1
    height = y2 - y1

    # Stretch fill
    if model == "draw":
        image_mask = cv2.resize(image_mask, (width, height))
        image[y1:y2, x1:x2, :] = image_mask

    # keep mask ratio fill
    elif model == "keep":
        ratio = min(width / mask_w, height / mask_h)

        fill_w = mask_w * ratio
        fill_h = mask_h * ratio

        image_mask = cv2.resize(image_mask, (fill_w, fill_h))
        image[y1:y1 + fill_h, x1:x1+fill_w, :] = image_mask
    # args error
    else:
        raise ValueError("model error, please choose from ['keep', 'draw']")

    return image


if __name__ == "__main__":

    # question 1.1
    file_name = "./boxes.json"
    bbox_ = print_name(file_name)

    # question 1.2
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=str, help="image path")
    parser.add_argument("image_mask", type=str, help="mask image path")
    parser.add_argument("model", type=str, default="keep", help="choose from ['keep', 'draw'")
    args = parser.parse_args()

    filled = image_fill(args.image, args.image_mask, bbox_, args.model)

    cv2.imshow('image_fill', filled)
