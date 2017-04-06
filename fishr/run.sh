mkdir -p data
mkdir -p data/fish_pics

export FLASK_APP=fishr/fishr.py
export FLASK_DEBUG=1
flask run --host=0.0.0.0
