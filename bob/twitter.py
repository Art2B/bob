from TwitterAPI import TwitterAPI

from config import get as get_config

config = get_config()

# Setup twitter api credentials
api = TwitterAPI(
    config['twitter']['consumer_key'],
    config['twitter']['consumer_secret'],
    config['twitter']['access_token_key'],
    config['twitter']['access_token_secret']
)

def tweet(text):
    # Tweet the event if localMode is false in config
    if config['main']['verbose'] == True:
        print('Twitter.py - Tweet: ' + text)

    if config['main']['localMode'] == False:
        r = api.request(
            'statuses/update',
            {
                'status': text[:config['twitter']['maxChars']]
            }
        )
        return r.json()['id_str']

def udpate_name(iteration_number):
    new_name = config['twitter']['baseName'] + ' #' + str(iteration_number)

    if config['main']['verbose'] == True:
        print('Twitter.py - Update account name: ' + new_name)

    if config['main']['localMode'] == False:
        r = api.request(
            'account/update_profile',
            {
                'name': new_name
            }
        )
        return r.json()

def update_profile_pic(base64Picture):
    if config['main']['verbose'] == True:
        print('Twitter.py - Update profile picture')

    if config['main']['localMode'] == False:
        r = api.request(
            'account/update_profile_image',
            {
                'image': base64Picture
            }
        )