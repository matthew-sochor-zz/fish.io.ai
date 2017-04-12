import os
import subprocess

import tqdm

import numpy as np

from keras.layers import Input
from keras.applications.resnet50 import ResNet50, preprocess_input


# TODO: allow for this to be parameterized
img_width = 224
img_height = 224


# TODO: replace this listdir with a mapping tbl/json
CATS = sorted(os.listdir('data/raw/train'))


def cat_from_int(cat_int):
    return CATS[cat_int]


def gen_XY_from_dir(arr_dir, with_name=False):
    arr_files = sorted(os.listdir(arr_dir))
    arr_names = list(filter(lambda x: r'-img-' in x, arr_files))
    lab_names = list(filter(lambda x: r'-lab-' in x, arr_files))

    assert len(arr_names) == len(lab_names), '# labels != images'

    for arr_name, lab_name in zip(arr_names, lab_names):
        X = np.load(os.path.join(arr_dir, arr_name))
        Y = np.load(os.path.join(arr_dir, lab_name))
        if with_name:
            out = X, Y, arr_name, lab_name
        else:
            out = X, Y
        yield out

def pop_layer(model, count=1):
    if not model.outputs:
        raise Exception('Sequential model cannot be popped: model is empty.')

    popped = [model.layers.pop() for i in range(count)]

    if not model.layers:
        model.outputs = []
        model.inbound_nodes = []
        model.outbound_nodes = []
    else:
        model.layers[-1].outbound_nodes = []
        model.outputs = [model.layers[-1].output]
    model.built = False
    return popped

# define the model features to extract
arr_input = Input(shape=(img_height, img_width, 3))
model = ResNet50(include_top=False, weights='imagenet',
                 input_tensor=arr_input, pooling='avg')

popped = pop_layer(model, 12)

model.summary()

def arrs_to_aug(arr_dir, emb_dir):

    subprocess.call(['mkdir', '-p', emb_dir])

    arr_gen = tqdm.tqdm(gen_XY_from_dir(arr_dir, with_name=True))
    for (x, y, arr_name, lab_name) in arr_gen:
        # TODO: refactor this to batch inputs via chunker

        X = preprocess_input(x[np.newaxis].astype(np.float32))
        x_emb = np.squeeze(model.predict(X, batch_size=1))
        y_emb = y

        emb_name = arr_name.split('.')[0]
        lab_name = lab_name.split('.')[0]
        emb_path = os.path.join(emb_dir, emb_name)
        lab_path = os.path.join(emb_dir, lab_name)
        np.save(emb_path, x_emb)
        np.save(lab_path, y_emb)


if __name__ == '__main__':
    arrs_to_aug('data/arr/test', 'data/emb/test')
    arrs_to_aug('data/aug/train', 'data/emb/train')
