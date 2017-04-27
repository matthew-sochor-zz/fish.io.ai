import os
import sys
import time

import logging as log

import numpy as np

from keras.models import load_model
from keras.preprocessing.image import load_img
from keras.applications.resnet50 import ResNet50, preprocess_input

from .models import FishPic
from .sqlite_queue import SqliteQueue


# TODO: allow for this to be parameterized
img_width = 224
img_height = 224

# TODO: replace this listdir with a mapping tbl/json
CATS = ['black_bullhead',
        'black_crappie',
        'black_redhorse',
        'bluegill',
        'carp',
        'channel_catfish',
        'largemouth_bass',
        'northern_pike',
        'pumpkinseed_sunfish',
        'rainbow_trout',
        'smallmouth_bass',
        'smallmouth_buffalo',
        'walleye',
        'white_bass',
        'white_crappie',
        'white_perch',
        'yellow_perch']

def cat_from_int(cat_int):
    return CATS[cat_int]

# TODO: make this assumptions more robust
# input_dims = (2048,)
# nbr_classes = len(CATS)
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
res50 = ResNet50(include_top=False, weights='imagenet',
                 input_shape=(img_height, img_width, 3), pooling='avg')

popped = pop_layer(res50, 12)

# TODO: make this more scalable with TF serving
model = load_model('data/models/resnet-4-24-2017-fish-17-acc-89.hdf5')


def predict(fish_pic_id, img_path):
    img_name = os.path.basename(img_path)

    x = np.array(load_img(img_path, target_size=(img_height, img_width)))
    X = preprocess_input(x[np.newaxis].astype(np.float32))

    X_fea = res50.predict_on_batch(X)

    y_pred = np.squeeze(model.predict_on_batch(X_fea), axis=0)

    log.info('-' * 30)
    log.info('img_name: %s', img_name)
    log.info('y_pred: %s', np.round(y_pred, 3))
    log.info('sorted cat list: %s', CATS)
    log.info('predicted class: %s', cat_from_int(np.argmax(y_pred)))
    log.info('-' * 30)

    # cache the model score to DB
    # TODO: add to ENV vs a hard code path to DB
    fish_pic_db = FishPic('data/dbs/fishr.db')
    fish_pic_dict = fish_pic_db.get(fish_pic_id)
    species_pred = cat_from_int(np.argmax(y_pred))

    fish_pic_dict['species_pred'] = species_pred
    fish_pic_dict['y_pred'] = y_pred.tolist()
    fish_pic_dict['y_labs'] = CATS

    fish_pic_db.replace(fish_pic_id, fish_pic_dict)
    log.debug('Commited update to db: %s', fish_pic_id)


def model_serve_from_queue(queue_path):
    fish_pic_queue = SqliteQueue(queue_path)
    while True:
        fish_pic_to_score = fish_pic_queue.popleft()
        predict(*fish_pic_to_score)


if __name__ == '__main__':
    file_path = sys.argv[1]

    if '.db' in file_path:
        # if given a database queue
        model_serve_from_queue(file_path)
