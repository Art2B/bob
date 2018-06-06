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
        print('Tweet: ' + text)

    if config['main']['localMode'] == False:
        r = api.request(
            'statuses/update',
            {
                'status': text[:config['twitter']['maxChars']]
            }
        )
        return r.json()['id_str']
