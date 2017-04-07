import os
import subprocess

import numpy as np

from keras.layers import Dense, Dropout, Input, BatchNormalization
from keras.models import Model
from keras.optimizers import Adam


batch_size = 8


# TODO: replace this listdir with a mapping tbl/json
CATS = sorted(os.listdir('data/raw/train'))


def cat_from_int(cat_int):
    return CATS[cat_int]


input_dims = (2048,)
nbr_classes = len(CATS)


def gen_minibatches(arr_dir):
    # TODO: refactor this to be more performative HHD
    # reading pattern if necessary

    # reset seed for multiprocessing issues
    np.random.seed()

    arr_files = sorted(os.listdir(arr_dir))
    arr_names = list(filter(lambda x: r'-img-' in x, arr_files))
    lab_names = list(filter(lambda x: r'-lab-' in x, arr_files))

    xy_names = list(zip(arr_names, lab_names))

    while True:
        # in place shuffle
        np.random.shuffle(xy_names)
        xy_names_mb = xy_names[:batch_size]

        X = []
        Y = []
        for arr_name, lab_name in xy_names_mb:
            x = np.load(os.path.join(arr_dir, arr_name))
            y = np.load(os.path.join(arr_dir, lab_name))
            X.append(x)
            Y.append(y)

        yield np.array(X), np.array(Y)


def train_model():
    model_name = 'resnet50_1layer.h5'

    model_dir = 'data/models'
    subprocess.call(['mkdir', '-p', model_dir])

    nbr_trn_samples = len(os.listdir('data/emb/train'))
    nbr_tst_samples = len(os.listdir('data/emb/test'))

    gen_trn = gen_minibatches('data/emb/train')
    gen_tst = gen_minibatches('data/emb/test')

    x_in = Input(shape=input_dims)
    x = BatchNormalization()(x_in)
    x = Dropout(0.5)(x)
    x = Dense(256, activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.2)(x)
    x = Dense(nbr_classes, activation='softmax')(x)

    model = Model(x_in, x)

    model.compile(optimizer=Adam(lr=1e-4, decay=1e-4),
                  loss='categorical_crossentropy',
                  metrics=['categorical_accuracy'])

    model.fit_generator(gen_trn,
                        steps_per_epoch=(nbr_trn_samples // batch_size),
                        epochs=5, verbose=2, validation_data=gen_tst,
                        validation_steps=(nbr_tst_samples // batch_size),
                        initial_epoch=0)

    Y_test = []
    Y_pred = []
    for _, (x_test, y_test) in zip(range(nbr_tst_samples // batch_size), gen_tst):
        Y_test.append(y_test)
        Y_pred.append(model.predict_on_batch(x_test))

    print('Model test:', np.mean(np.argmax(np.concatenate(Y_test), axis=1) == np.argmax(np.concatenate(Y_pred), axis=1)))

    model.save(os.path.join(model_dir, model_name))

    return model


if __name__ == '__main__':
    # current code should get close to 81 percent acc
    model = train_model()
    model.summary()
