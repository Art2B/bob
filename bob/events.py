# coding: utf-8
import datetime
import random
import requests
import json
import re

from helpers import month_string_to_number
from config import get as get_config

config = get_config()

dateRegex = re.compile("^\[{2}([a-zA-Z]*?) ([0-9]+)\]{2}", re.M)

def eventTypeToString(argument):
    return config['formatting']['switcher'].get(argument, "")

def getYearData ( year ):
    r = requests.get(config['api']['endpoint'] + config['api']['urlParams'] + str(year))
    data = json.loads(r.text)['query']['pages']
    data = data[next(iter(data))]['revisions'][0]['*']
    return data

def getFormattedEvent (eventType, date, eventText):
    event = date + ": "
    event = event + eventTypeToString(eventType) + eventText
    # Replace years from [[1932]] to 1932
    event = re.sub(r"\[{2}([0-9]+)\]{2}", r"\1", event)
    # Remove html tags from text
    event = re.sub(r"<.+?>.+?</.+?>", "", event)
    # Remove remaining tags
    event = re.sub(r"<.+?>", "", event)
    # Replace links with two spelling separeted by "|"
    event = re.sub(r"\[{2}(.+?)\|.+?\]{2}", r"\1", event)
    # Replace markup with {..} separated by "|" inside
    event = re.sub(r"\{{2}(.+?)\|.+?\}{2}", r"\1", event)
    # Remove all [[...]] from links
    event = re.sub(r"\[{2}(.+?)\]{2}", r"\1", event)
    # Remove html chars
    event = re.sub(r"&.+?;(\s| )", "", event)
    # Remove remaining tokens
    event = event.replace("[[", "")
    event = event.replace("]]", "")
    event = event.replace("''", "'")
    event = event.replace("  ", " ")
    return event

def getEventDatetime(text, year):
    dateReResults = re.search(dateRegex, text)
    if dateReResults:
        month = month_string_to_number(dateReResults.group(1))
        day = dateReResults.group(2)
    else:
        month = 1
        day = 1
    return datetime.date(int(year), int(month), int(day))

def getFormattedDate (text, year):
    # Get data from text
    date = re.search(dateRegex, text)
    # Format date depending on regex match
    if date:
        date = date.group(2) + " " + date.group(1) + " " + str(year)
    else:
        date = config['formatting']['noDay'] + str(year)
    return date

def getEventsFromMultilineDate ( eventType, dateText, year):
    date = getFormattedDate(dateText[1], year)
    events = re.findall("^\*{2}(.*)$", dateText[0], re.M)
    formattedEventsList = []
    for event in events:
        eventText = getFormattedEvent(eventType, date, event)
        formattedEventsList.append({
            'date': getEventDatetime(eventText, year),
            'text': eventText
        })
    return formattedEventsList

def formatData ( data, year ):
    events = []
    #Remove sub categories from text
    data = re.sub(re.compile("(^={3,}[a-zA-Z\s]*={3,}$)", re.M), "", data)
    # Sort by events types
    results = re.findall("(^={2}[a-zA-Z\s]*={2}$)(.*?)(?=(?:^={2}[a-zA-Z\s]*={2}$)|\Z)", data, re.S|re.M)
    for match in results:
        eventType = match[0].replace("=", "").replace(" ", "").lower()
        eventData = re.sub(re.compile("^(?!\*)(.*)$", re.M), '', match[1])

        if any(eventType in s for s in config['formatting']['typesHandled']):
            # Format multiline date events
            multilineRegex = re.compile("(?P<full_match>^\*{1} (.*)\n(^\*{2}(.*?)\n)+)", re.M)
            multilineDates = re.findall(multilineRegex, eventData)
            eventData = re.sub(multilineRegex, "", eventData)
            for el in multilineDates:
                for item in getEventsFromMultilineDate(eventType, el, year):
                    events.append(item)

            # Format single lined events
            singlelineEvent = re.findall("^\* (.+?)$", eventData, re.M)
            for el in singlelineEvent:
                events.append({
                  'date': getEventDatetime(el, year),
                  'text': getFormattedEvent( eventType, getFormattedDate(el, year), re.sub(r"^\[{2}[a-zA-Z]*?\s[0-9]+\]{2}((\s|)–(\s|)|(\s|)&.+?;(\s|))", "", el))
                })

    return events
 
def getEventFromYear(year):
    formatted_events = formatData(getYearData(year), year)
    return random.choice(formatted_events)