#!/bin/bash

if [[ "$2" == "--start" ]]; then
    echo "Starting App"

    mkdir -p data
    mkdir -p data/queues
    mkdir -p data/dbs

    mkdir -p data/fish_pics

    mkdir -p logs
    mkdir -p logs/fishr
    mkdir -p logs/scoring

    python -m fishr.score_fish_pic data/queues/fish_pic_queue.db > logs/scoring/fish_pics.log 2>&1 &

    if [[ "$1" == "--prod" ]]; then
        source activate fishr
        # TODO: remove once scoring is non file based
        # rm -rf  data/fish_pics/*

        mkdir -p logs/nginx

        # there has to be a better way to do this with ENV vs sudo
        sudo service nginx start
        sudo rm -f /etc/nginx/sites-enabled/default
        sudo rm -f /etc/nginx/sites-enabled/default
        sudo touch /etc/nginx/sites-available/fishr
        sudo cp /home/fishioai/fish.io.ai/fishr/nginx/fishr.conf /etc/nginx/sites-available/fishr
        sudo rm -f /etc/nginx/sites-enabled/fishr
        sudo ln -s /etc/nginx/sites-available/fishr /etc/nginx/sites-enabled/fishr
        sudo service nginx restart

        gunicorn fishr:app -b 127.0.0.1 --threads=2 > logs/fishr/fishr.log 2>&1 &
    fi

    if [[ "$1" == "--dev" ]]; then
        export FLASK_APP=fishr/__init__.py
        export FLASK_DEBUG=1
        flask run &&
        echo "App killed"
    fi
fi


if [[ "$2" == "--kill" ]]; then
    echo "Killing App"

    if [[ "$1" == "--prod" ]]; then
        sudo service nginx stop
        pgrep "gunicorn" | xargs kill
    fi

    if [[ "$1" == "--dev" ]]; then
        pgrep "flask" | xargs kill
    fi

    pgrep -f "score_fish_pic" | xargs kill

    rm -f data/queues/fish_pic_queue.db
fi
