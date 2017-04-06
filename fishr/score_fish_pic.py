import os
import sys

import numpy as np

from keras.models import load_model
from keras.preprocessing.image import load_img
from keras.applications.resnet50 import ResNet50, preprocess_input


def predict(img_path):
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

    img_name = os.path.basename(img_path)

    x = np.array(load_img(img_path, target_size=(img_height, img_width)))
    X = preprocess_input(x[np.newaxis].astype(np.float32))

    X_fea = res50.predict_on_batch(X)

    model = load_model('data/models/resnet50_1layer_moreopts.h5')
    y_pred = np.squeeze(model.predict_on_batch(X_fea), axis=0)

    print('-' * 30)
    print('img_name:', img_name)
    print('y_pred:', np.round(y_pred, 3))
    print('sorted cat list:', CATS)
    print('predicted class:', cat_from_int(np.argmax(y_pred)))
    print('-' * 30)

    # cache score
    score_path = os.path.join(os.path.dirname(img_path), os.pardir, 'scores')
    # TODO: move directories to init script
    if not os.path.exists(score_path):
        os.mkdir(score_path)

    # TODO: back with DB vs file system
    with open(os.path.join(score_path, img_name), 'w') as f:
        f.write(cat_from_int(np.argmax(y_pred)))

    # For purposes of using this script as an API
    # output the class name last.
    print(cat_from_int(np.argmax(y_pred)))


if __name__ == '__main__':
    img_path = sys.argv[1]
    predict(img_path)
