# Big old Button

A python iot project who makes you learn history events from Wikipedia via Twitter.

## Installation
  - Clone project
  - `make install`
  - `make start`

### Requirements
  - Python 3.6.3 or higher
  - [pip](https://pypi.python.org/pypi/pip/) 9.0.1 or higher

## Config
  Details about `config.json` file

### Main
  - `scFrequency`: Number of seconds between each incrementation of year
  - `startingYear`: The year from which you start crawling events. I recommend 1 for now
  - `localMode`: Boolean to whether or not tweet events

### Api
  - `endpoint`: Wikipedia API endpoint
  - `urlParams`: API query url params

### Twitter
  - `consumer_key`: Your twitter API consumer key
  - `consumer_secret`: Your twitter API consumer secret
  - `access_token_key`: Your twitter API access token key
  - `access_token_secret`: Your twitter API access token secret
  - `maxChars`: The number of max characters you want in your tweets

### Formatting
  - `typesHandled`: The wikipedia events types handled. Used for parsing
  - `switcher`: Python dictionnary for formatting purpose
  - `noDay`: Text used when there is no specific day for event

## Licence

This project is under a MIT licence :)