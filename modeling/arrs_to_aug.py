import os
import subprocess
import tqdm
import numpy as np
from keras.preprocessing.image import ImageDataGenerator

aug_rounds = 4
# TODO: replace this listdir with a mapping tbl/json
CATS = sorted(os.listdir('data/raw/train'))


def cat_from_int(cat_int):
    return CATS[cat_int]


def gen_XY_from_dir(arr_dir):
    arr_files = sorted(os.listdir(arr_dir))
    arr_names = list(filter(lambda x: r'-img-' in x, arr_files))
    lab_names = list(filter(lambda x: r'-lab-' in x, arr_files))

    assert len(arr_names) == len(lab_names), '# labels != images'

    for arr_name, lab_name in zip(arr_names, lab_names):
        X = np.load(os.path.join(arr_dir, arr_name))
        Y = np.load(os.path.join(arr_dir, lab_name))
        yield X, Y


def augment_XY(x, y, aug_rounds):
    auggen = ImageDataGenerator(rotation_range=10,
                                width_shift_range=0.1,
                                height_shift_range=0.1,
                                horizontal_flip=True)

    X_aug, Y_aug = next(auggen.flow(np.tile(x[np.newaxis],
                                            (aug_rounds, 1, 1, 1)),
                                    np.tile(y[np.newaxis],
                                            (aug_rounds, 1)),
                                    batch_size=aug_rounds))

    for x_aug, y_aug in zip(X_aug, Y_aug):
        yield x_aug, y_aug


def arrs_to_aug(arr_dir, aug_dir):

    subprocess.call(['mkdir', '-p', aug_dir])

    for img_idx, (x, y) in tqdm.tqdm(enumerate(gen_XY_from_dir(arr_dir))):
        for aug_idx, (x_aug, y_aug) in enumerate(augment_XY(x, y, aug_rounds)):
            cat_idx = np.argmax(y_aug)
            cat = cat_from_int(cat_idx)
            img_name = '{:04d}-{:02d}-img-{}-{}'.format(img_idx, aug_idx,
                                                        cat, cat_idx)
            lab_name = '{:04d}-{:02d}-lab-{}-{}'.format(img_idx, aug_idx,
                                                        cat, cat_idx)
            aug_path = os.path.join(aug_dir, img_name)
            lab_path = os.path.join(aug_dir, lab_name)
            np.save(aug_path, x_aug)
            np.save(lab_path, y_aug)


if __name__ == '__main__':
    arrs_to_aug('data/arr/train', 'data/aug/train')
