source activate fishr

mkdir -p logs/nginx
mkdir -p logs/fishr
mkdir -p data/fish_pics

# there has to be a better way to do this with ENV vs sudo
sudo service nginx start
sudo rm -f /etc/nginx/sites-enabled/default
sudo rm -f /etc/nginx/sites-enabled/default
#sudo touch /etc/nginx/sites-available/fishr
sudo cp /home/fishioai/fish.io.ai/fishr/nginx/fishr.conf /etc/nginx/sites-available/fishr
sudo rm -f /etc/nginx/sites-enabled/fishr
sudo ln -s /etc/nginx/sites-available/fishr /etc/nginx/sites-enabled/fishr
sudo service nginx restart

gunicorn fishr:app -b 127.0.0.1 --threads=4 > logs/fishr/fishr.log 2>&1 &
