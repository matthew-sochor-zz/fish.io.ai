import base64
import os
import random
import subprocess

import logging as log

from flask import Flask, redirect, render_template,\
    request, url_for
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename


log.basicConfig(level=log.DEBUG)


# Flask extensions
bootstrap = Bootstrap()


app = Flask(__name__)


# Initialize flask extensions
bootstrap.init_app(app)


log.basicConfig(level=log.DEBUG)


# env vars for tmp purposes
class Config(object):
    # DEBUG = False
    # TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY',
                                'superSecretDoNotUseOnOpenWeb')


# init config
app.config.from_object(Config)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/regulations')
def regulations():
    return render_template('regulations.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # TODO: add data validation step
        if True:
            log.debug('data:')
            log.debug(request.data)
            log.debug('files:')
            log.debug(request.files)
            fish_pic_file = request.files['fish-pic-input']
            # TODO: path should be updated before production
            dump_path = os.path.join('data',
                                     'fish_pics')
            log.debug('dump_path:')
            log.debug(os.listdir(dump_path))
            fish_pic_ext = (secure_filename(fish_pic_file.filename)
                            .split('.')[-1])
            # TODO: refactor this to use DB with primary key
            if len(os.listdir(dump_path)) > 0:
                fish_pic_id = max(os.listdir(dump_path)).split('-')[0]
                fish_pic_id = int(fish_pic_id) + 1
            else:
                fish_pic_id = 0
            fish_pic_base = 'fish_pic'
            fish_pic_name = '{:03d}-{}.{}'.format(fish_pic_id,
                                                  fish_pic_base,
                                                  fish_pic_ext)
            fish_pic_path = os.path.join(dump_path,
                                         fish_pic_name)
            log.debug(fish_pic_path)
            fish_pic_file.save(fish_pic_path)
            return redirect(url_for('loading_splash',
                                    fish_pic_id=fish_pic_id))

    # art for photo upload page
    art_sel = 'CameraIconPIC.png'
    art_url = url_for('static',
                      filename='{}/{}'.format('images',
                                              art_sel))

    # if not a post request return html
    return render_template('upload.html',
                           art_url=art_url)


# TODO: remove this global dict in favor of actual model
FISH_PIC_DICT = {}


def fish_pic_results(fish_pic_id):
    try:
        counter = FISH_PIC_DICT[fish_pic_id]['counter']
    except KeyError:
        FISH_PIC_DICT[fish_pic_id] = {}
        counter = 0

    # increment the counter to simulate model running
    counter += 1

    # TODO: refactor to DB for PROD
    dump_path = os.path.join('data',
                             'fish_pics')
    fish_pic_name = [fish_pic_name for fish_pic_name in os.listdir(dump_path)
                     if (int(fish_pic_name.split('-')[0]) ==
                         int(fish_pic_id))][0]
    fish_pic_path = os.path.join(dump_path, fish_pic_name)

    if counter == 1:
        subprocess.call(['python', 'fishr/score_fish_pic.py', fish_pic_path,
                         '>>', 'score_fish_pic.log', '2&>1'])

        # return null data until scoring job finishes
        FISH_PIC_DICT[fish_pic_id]['counter'] = counter
        FISH_PIC_DICT[fish_pic_id]['results'] = None

        log.debug('fish_pic_dict: %s', FISH_PIC_DICT[fish_pic_id])
        return FISH_PIC_DICT[fish_pic_id]['results']
    elif counter < 10:
        score_path = os.path.join('data/scores', fish_pic_name)
        print(score_path)
        if os.path.exists(score_path):
            log.debug('Scoring finished for: %s', score_path)
            with open(score_path, 'r') as f:
                species_pred = f.read().strip()
            # TODO: move to DB
            species_to_invasive = {'walleye': False,
                                   'carp': True,
                                   'white_perch': True,
                                   'yellow_perch': False
                                   }

            results = {'invasive': species_to_invasive[species_pred],
                       'species': species_pred,
                       'length': 8}

            return results

        else:
            log.debug('Waiting on model for: %s', score_path)
            FISH_PIC_DICT[fish_pic_id]['counter'] = counter
            FISH_PIC_DICT[fish_pic_id]['results'] = None

            log.debug('fish_pic_dict: %s', FISH_PIC_DICT[fish_pic_id])
            return FISH_PIC_DICT[fish_pic_id]['results']
    else:
        log.warn('Model scoring timed out')
        # TODO: don't return a random model here as done now
        FISH_PIC_DICT[fish_pic_id]['counter'] = counter

        # TODO: this should return real model results
        if int(fish_pic_id) % 2 == 0:
            results = {'invasive': True, 'length': 12, 'species': 'unknown'}
        else:
            results = {'invasive': False, 'length': 8, 'species': 'unknown'}
        FISH_PIC_DICT[fish_pic_id]['results'] = results

        log.debug('fish_pic_dict: %s', FISH_PIC_DICT[fish_pic_id])
        return FISH_PIC_DICT[fish_pic_id]['results']


@app.route('/loading_splash/<string:fish_pic_id>')
def loading_splash(fish_pic_id):
    results = fish_pic_results(fish_pic_id)
    # TODO: what if model results are never returned
    if not results:
        # random loading art
        art_sel = random.choice(ART_IDX['loading'])
        art_url = url_for('static',
                          filename='{}/{}'.format('images',
                                                  art_sel))

        # return the loading page if model results are None
        return render_template('loading_splash.html',
                               fish_pic_id=fish_pic_id,
                               art_url=art_url)
    else:
        # if model results are availible redirect
        return redirect(url_for('submission_results',
                                fish_pic_id=fish_pic_id))


ART_IDX = {'keeper': ['GoodFish1PIC.png',
                      'GoodFish2PIC.png',
                      'GoodFish3PIC.png',
                      'GoodFish4PIC.png'],
           'release': ['ReleaseFish1PIC.png',
                       'ReleaseFish2PIC.png',
                       'ReleaseFish3PIC.png'],
           'invasive': ['BadFish1PIC.png',
                        'BadFish2PIC.png',
                        'BadFish3PIC.png'],
           'loading': ['Loading1PIC.png',
                       'Loading2PIC.png',
                       'Loading3PIC.png',
                       'Loading4PIC.png']
           }


@app.route('/submission_results/<string:fish_pic_id>')
def submission_results(fish_pic_id):
    results = fish_pic_results(fish_pic_id)

    # TODO: more robust redirect strategy
    if not results:
        return redirect(url_for('index'))

    # TODO: refactor to DB for PROD
    dump_path = os.path.join('data',
                             'fish_pics')
    fish_pic_name = [fish_pic_name for fish_pic_name in os.listdir(dump_path)
                     if (int(fish_pic_name.split('-')[0]) ==
                         int(fish_pic_id))][0]

    fish_pic_path = os.path.join(dump_path, fish_pic_name)

    with open(fish_pic_path, 'rb') as f:
        fish_pic_file = f.read()

    fish_pic_base64 = base64.b64encode(fish_pic_file).decode('utf-8')

    # TODO: refactor this into lookup functions
    # based on state rules database(s).
    if results['invasive']:
        catch_type = 'invasive'
    else:
        if int(fish_pic_id) % 2 == 0:
            catch_type = 'keeper'
        else:
            catch_type = 'release'

    results_heading_dict = {
        'invasive': 'Invasive Species: Don\'t release',
        'keeper': 'This Catch is a Keeper',
        'release': 'Please Release this Fish'
    }

    species_pred = results['species']

    # the heading is the bold message displayed to user
    results_heading = results_heading_dict[catch_type]

    art_sel = random.choice(ART_IDX[catch_type])
    log.debug('art_sel: %s', art_sel)
    art_url = url_for('static',
                      filename='{}/{}'.format('images',
                                              art_sel))

    return render_template('submission_results.html',
                           results_heading=results_heading,
                           species_pred=species_pred,
                           art_url=art_url,
                           fish_pic_base64=fish_pic_base64)
