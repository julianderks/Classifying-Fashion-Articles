import pandas as pd
from urllib.request import urlopen

import cv2
import numpy as np
import matplotlib.pyplot as plt
import re


def preprocess():
    #  Load raw data
    df = pd.read_csv(".\data\zalando_articles_raw.csv")

    #  We only want packshot images (i.e. just the article with white background)
    df = df[df["image_url"].str.contains("filter=packshot")]

    df = df.drop_duplicates(subset=["article_id"])

    #  Drop some categories
    # print(df["category"].unique())
    # exit()

    # Load images in same size
    regex_pat = re.compile("imwidth=\d+")
    df["image_url"] = df["image_url"].str.replace(regex_pat, "imwidth=600", regex=True)

    article_index = 0
    index_list = []
    for index, row in df.iterrows():
        img = load_img(row.image_url)

        if validate_proportion_background(img):
            cv2.imwrite(f"./data/img/img_{article_index:05d}.png", img)
            index_list.append(article_index)
            article_index += 1
        else:
            df.drop(index, inplace=True)
    df["article_index"] = index_list

    df.to_csv(".\data\zalando_articles_cleaned.csv", index=False)
    # used_img = df["image_url"].apply(load_img)
    # df[["image_url", "article_index"]].apply(load_img, axis=1)
    # img = img[:, :, [2, 1, 0]]  # Re-order image to RGB


def load_img(image_url):
    req = urlopen(image_url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)

    return img


def validate_proportion_background(img, threshold=0.30):
    """indicate if image contains transparent or white background above some treshold"""

    background = [235, 235, 235]

    #  Get the percentage of pixels that have the exact same color values
    logical_mask = (img >= background).all(axis=2)
    percent = logical_mask.sum() / logical_mask.size

    if percent >= threshold:
        return True
    else:
        return False


def center_crop(img, dim):
    width, height = img.shape[1], img.shape[0]

    # process crop width and height for max available dimension
    crop_width = dim[0] if dim[0] < img.shape[1] else img.shape[1]
    crop_height = dim[1] if dim[1] < img.shape[0] else img.shape[0]

    mid_x, mid_y = int(width / 2), int(height / 2)
    cw2, ch2 = int(crop_width / 2), int(crop_height / 2)

    crop_img = img[mid_y - ch2 : mid_y + ch2, mid_x - cw2 : mid_x + cw2]
    return crop_img


if __name__ == "__main__":
    preprocess()
