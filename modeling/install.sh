#!/bin/bash

# ubuntu installs
sudo apt update -y

sudo apt install -y htop tmux awscli imagemagick

sudo apt install -y gcc g++ gfortran build-essential git wget

# python install
curl -O https://repo.continuum.io/archive/Anaconda3-4.3.1-Linux-x86_64.sh
bash Anaconda3-*-Linux-x86_64.sh -b
rm Anaconda3-*-Linux-x86_64.sh
export PATH="$HOME/anaconda3/bin:$PATH"
echo -e "\n# Anaconda3" >> $HOME/.bashrc
echo 'export PATH="$HOME/anaconda3/bin:$PATH"' >> $HOME/.bashrc

python -c "import numpy as np; print(np.__config__.show())"
# output should contain substring: mkl_intel_lp64

# cuda 8 install
curl -O http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_8.0.61-1_amd64.deb
sudo dpkg -i cuda-repo-*_amd64.deb
sudo apt update -y
sudo apt install -y cuda
rm cuda-repo-*_amd64.deb
# add cuda to path
echo -e "\n# CUDA Environment Variables" >> .bashrc
echo -e 'export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64"' >> .bashrc
echo -e 'export CUDA_HOME="/usr/local/cuda"' >> .bashrc
echo -e 'export PATH="/usr/local/cuda/bin:$PATH"' >> .bashrc
echo -e 'export CUDA_ROOT="/usr/local/cuda"' >> .bashrc
export CUDA_ROOT=/usr/local/cuda
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64
export CUDA_HOME=/usr/local/cuda
export PATH=/usr/local/cuda/bin:$PATH

nvidia-smi
# should contain substring: "0 Tesla K80"

cd /usr/local/cuda/samples/1_Utilities/deviceQuery
sudo make
./deviceQuery
cd ~/
cat cudatest.txt
rm cudatest.txt
# should contain substring: "Result = PASS"

# manually get cuddn via scp here
tar -xvzf cudnn*.tgz
sudo cp cuda/include/cudnn.h /usr/local/cuda/include
sudo cp cuda/lib64/libcudnn* /usr/local/cuda/lib64
sudo chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda/lib64/libcudnn*
rm -rf cuda

# tensorflow install
pip install https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-1.0.1-cp36-cp36m-linux_x86_64.whl

# keras install
pip install keras

# save keras settings
mkdir -p ~/.keras
echo '{
    "image_data_format": "channels_last",
    "epsilon": 1e-07,
    "floatx": "float32",
    "backend": "tensorflow"
}' > ~/.keras/keras.json

# test tensorflow 
python -c 'import os; import inspect; import tensorflow; print(os.path.dirname(inspect.getfile(tensorflow)))'
# should contain substring: "libcudnn.so.* locally"
python -c "import numpy as np; import time; import tensorflow as tf; d = 10000; x = tf.constant(np.random.random((d, d))); sess = tf.Session(); s = time.time(); print(sess.run(tf.matmul(x, x))); print('time:', time.time() - s);"
# running on p2.xlarge: time: 100 sec
# while true; do (clear; nvidia-smi); sleep 1; done
