import os
import numpy as np
import sys
import subprocess

fish_name = sys.argv[1]
source_path = sys.argv[2]
test_path = sys.argv[3]
train_path = sys.argv[4]
percent = float(sys.argv[5])

fish = os.listdir(source_path + '/' + fish_name)
fish = [f for f in fish if f.find('.jpg') > -1]

index = int(len(fish) * percent)
np.random.shuffle(fish)
train, test = fish[:index], fish[index:]

for fish in train:
    subprocess.call(['cp', '/'.join([source_path, fish_name, fish]), '/'.join([train_path, fish_name, fish])])

for fish in test:
    subprocess.call(['cp', '/'.join([source_path, fish_name, fish]), '/'.join([test_path, fish_name, fish])])