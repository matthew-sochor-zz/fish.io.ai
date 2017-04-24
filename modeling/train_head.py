import os
import subprocess

import numpy as np

from keras.applications.resnet50 import ResNet50
from keras.layers import Dense, Dropout, Input, BatchNormalization, Conv2D, Activation, AveragePooling2D, GlobalAveragePooling2D
from keras.models import Model
from keras.optimizers import Adam
from keras import layers
from keras.callbacks import ModelCheckpoint

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

batch_size = int(os.environ.get("BATCH_SIZE"))

img_dim = 224

model_dir = 'data/models'
model_name = os.environ.get("MODEL_NAME")
model_weights = os.environ.get("MODEL_WEIGHTS")
num_epochs = int(os.environ.get("EPOCHS"))

input_dims = (7, 7, 2048)

# TODO: replace this listdir with a mapping tbl/json
CATS = sorted(os.listdir('data/raw/train'))
nbr_classes = len(CATS)

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

def cat_from_int(cat_int):
    return CATS[cat_int]




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
    subprocess.call(['mkdir', '-p', model_dir])

    nbr_trn_samples = len(os.listdir('data/emb/train'))
    nbr_tst_samples = len(os.listdir('data/emb/test'))

    gen_trn = gen_minibatches('data/emb/train')
    gen_tst = gen_minibatches('data/emb/test')

    arr_input = Input(shape=(img_dim, img_dim, 3))
    resnet_model = ResNet50(include_top=False, weights='imagenet',
                     input_tensor=arr_input, pooling='avg')

    popped = pop_layer(resnet_model, 12)

    # Take last 12 layers from resnet 50 with their starting weights!
    x_in = Input(shape=input_dims)

    x = popped[11](x_in)
    x = popped[10](x)
    x = Activation('relu')(x)

    x = popped[8](x)
    x = popped[7](x)
    x = Activation('relu')(x)

    x = popped[5](x)
    x = popped[4](x)

    x = layers.add([x, x_in])
    x = Activation('relu')(x)

    x = AveragePooling2D((7, 7), name='avg_pool')(x)
    x = GlobalAveragePooling2D()(x)

    x = BatchNormalization()(x)
    x = Dropout(0.2)(x)
    x = Dense(nbr_classes, activation='softmax')(x)

    model = Model(x_in, x)
    if len(model_weights) > 0:
        model.load_weights(model_dir + '/' + model_weights)
    model.summary()

    model.compile(optimizer=Adam(lr=float(os.environ.get("LOSS_RATE"))),
                  loss='categorical_crossentropy',
                  metrics=['categorical_accuracy'])

    model.summary()
    filepath="data/models/" + model_name.split('.')[0] + "-weights-improvement-{epoch:02d}-{val_categorical_accuracy:.4f}.hdf5"
    checkpoint = ModelCheckpoint(filepath, monitor='val_categorical_accuracy', verbose=1, save_best_only=True, mode='max')
    callbacks_list = [checkpoint]
    steps_per_epoch = (nbr_trn_samples // batch_size)
    validation_steps = (nbr_tst_samples // batch_size)

    model.fit_generator(gen_trn,
                        steps_per_epoch=steps_per_epoch,
                        epochs=num_epochs,
                        verbose=2,
                        validation_data=gen_tst,
                        validation_steps=validation_steps,
                        initial_epoch=0,
                        callbacks = callbacks_list)

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
