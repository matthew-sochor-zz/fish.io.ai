import os
import subprocess

import numpy as np

from keras.applications.resnet50 import ResNet50, preprocess_input
from keras.layers import Dense, Dropout, Input, BatchNormalization, Conv2D, Activation, AveragePooling2D, GlobalAveragePooling2D
from keras.models import Model
from keras.optimizers import Adam
from keras import layers
from keras.callbacks import ModelCheckpoint

from dotenv import load_dotenv, find_dotenv
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

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


def predict_test():
    subprocess.call(['mkdir', '-p', model_dir])

    nbr_tst_samples = len(os.listdir('data/arr/test'))

    gen_tst = gen_XY_from_dir('data/arr/test', with_name=True)

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
        print('loading: ',model_weights)
        model.load_weights(model_dir + '/' + model_weights)

    Y_test = []
    Y_pred = []
    for (x_test, y_test, arr_name, lab_name) in gen_tst:
        # TODO: refactor this to batch inputs via chunker
        Y_test.append(y_test)
        x_test_preproc = preprocess_input(x_test[np.newaxis].astype(np.float32))
        x_features = resnet_model.predict(x_test_preproc, batch_size=1)
        y_pred = model.predict(x_features, batch_size=1)
        print(CATS[np.argmax(y_test)], CATS[np.argmax(y_pred)])
        Y_pred.append(y_pred)

    Y_test = np.argmax(Y_test, axis=1)
    Y_pred = np.argmax(np.concatenate(Y_pred), axis=1)
    print('Model test:', np.mean(Y_test == Y_pred))

    cm = confusion_matrix(Y_test, Y_pred)
    print(cm)
    sns.heatmap(pd.DataFrame(cm, CATS, CATS), annot=True, fmt='g', cbar=False)
    plt.yticks(rotation=0) 
    plt.xticks(rotation=90) 
    plt.gcf().subplots_adjust(bottom=0.30, left=0.20)
    plt.savefig('data/plots/' + model_weights.split('.')[0] + '.png')

    return model


if __name__ == '__main__':
    # current code should get close to 81 percent acc
    model = predict_test()
