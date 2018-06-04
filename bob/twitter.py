from TwitterAPI import TwitterAPI

# Open config file
with open('config.json', 'r') as f:
    config = json.load(f)

# Setup twitter api credentials
api = TwitterAPI(
    config["twitter"]["consumer_key"],
    config["twitter"]["consumer_secret"],
    config["twitter"]["access_token_key"],
    config["twitter"]["access_token_secret"]
)

def tweet(text):
    # Tweet the event if localMode is false in config
    if config["main"]["localMode"] == False:
        r = api.request(
            'statuses/update',
            {
                'status': text[:config["twitter"]["maxChars"]]
            }
        )
        return r.json()['id_str']
