# directions are approximate WIP thus far

adduser fishioai
adduser fishioai sudo

su fishioai

sudo apt update -y

sudo apt install -y git htop tmux

curl -O https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh

bash Miniconda3-*-Linux-x86_64.sh -b
rm Miniiconda3-*-Linux-x86_64.sh

export PATH="$HOME/miniconda3/bin:$PATH"
echo "# Miniconda3" >> $HOME/.bashrc
echo 'export PATH="$HOME/miniconda3/bin:$PATH"' >> $HOME/.bashrc

conda create --name fishr python=3.6 -y
source activate fishr

pip install gunicorn
pip install flask flask_bootstrap
conda install numpy h5py pillow -y
pip install keras tensorflow

pip freeze > requirements.txt

sudo apt install -y supervisor
