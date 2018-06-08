import json
import requests
import random

import randomcolor

from config import get as get_config

config = get_config()

def month_string_to_number(month):
    m = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr': 4,
        'may': 5,
        'jun': 6,
        'jul': 7,
        'aug': 8,
        'sep': 9,
        'oct': 10,
        'nov': 11,
        'dec': 12
    }

    try:
        s = month.strip()[:3].lower()
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')

def get_explosion_gif():
    r = requests.get(
            config['giphy']['host'] +
            config['giphy']['endpoints']['search'] +
            '?api_key=' + config['giphy']['api_key'] +
            '&q=nuclear explosion'
        )
    if r.status_code == 200:
        data = json.loads(r.text)
        gifs = data['data']
        return random.choice(gifs)
    else:
        return {
            url: ''
        }

def get_random_palette(nb_colors):
    rand_color = randomcolor.RandomColor()
    return rand_color.generate(count=nb_colors)