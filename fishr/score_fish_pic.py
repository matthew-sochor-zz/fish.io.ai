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
CATS = ['carp', 'walleye', 'white_perch', 'yellow_perch']

def cat_from_int(cat_int):
    return CATS[cat_int]

# TODO: make this assumptions more robust
# input_dims = (2048,)
# nbr_classes = len(CATS)

res50 = ResNet50(include_top=False, weights='imagenet',
                 input_shape=(img_height, img_width, 3), pooling='avg')

# TODO: make this more scalable with TF serving
model = load_model('data/models/resnet50_1layer_moreopts.h5')


def predict(fish_pic_id, img_path):
    img_name = os.path.basename(img_path)

    x = np.array(load_img(img_path, target_size=(img_height, img_width)))
    X = preprocess_input(x[np.newaxis].astype(np.float32))

    X_fea = res50.predict_on_batch(X)

    y_pred = np.squeeze(model.predict_on_batch(X_fea), axis=0)

    log.info('-' * 30)
    log.info('img_name:', img_name)
    log.info('y_pred:', np.round(y_pred, 3))
    log.info('sorted cat list:', CATS)
    log.info('predicted class:', cat_from_int(np.argmax(y_pred)))
    log.info('-' * 30)

    # cache the model score to DB
    # TODO: add to ENV vs a hard code path to DB
    fish_pic_db = FishPic('data/dbs/fishr.db')
    fish_pic_dict = fish_pic_db.get(fish_pic_id)
    species_pred = cat_from_int(np.argmax(y_pred))
    fish_pic_dict['species_pred'] = species_pred
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
