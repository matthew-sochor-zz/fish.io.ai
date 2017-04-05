import os
import subprocess

import tqdm

import numpy as np

from keras.preprocessing.image import load_img


# TODO: allow for this to be parameterized
img_width = 224
img_height = 224


def imgdir_to_arr(data_dir, arr_dir):
    print('Converting from: "{}"'.format(data_dir))
    print('Saving to: "{}"'.format(arr_dir))

    subprocess.call(['mkdir', '-p', arr_dir])

    cats = sorted(os.listdir(data_dir))
    cat_nbr = len(cats)
    print('Iterating over all categories')

    for cat_idx, cat in tqdm.tqdm(enumerate(cats)):
        cat_path = os.path.join(data_dir, cat)
        img_files = sorted(os.listdir(cat_path))
        for img_idx, img_file in enumerate(img_files):
            img_path = os.path.join(cat_path, img_file)
            img = load_img(img_path, target_size=(img_height, img_width))
            img_name = '{:04d}-img-{}-{}'.format(img_idx, cat, cat_idx)
            lab_name = '{:04d}-lab-{}-{}'.format(img_idx, cat, cat_idx)
            lab = np.eye(cat_nbr, dtype=np.float32)[cat_idx]
            arr_path = os.path.join(arr_dir, img_name)
            lab_path = os.path.join(arr_dir, lab_name)
            np.save(arr_path, img)
            np.save(lab_path, lab)


if __name__ == '__main__':
    imgdir_to_arr('data/raw/train', 'data/arr/train')
    imgdir_to_arr('data/raw/test', 'data/arr/test')
