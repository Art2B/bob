from datetime import datetime
import requests
import json
import re

with open('config.json', 'r') as f:
    config = json.load(f)

#LOG FOR DEV PURPOSES
logFile = open('results.log', 'w')
year = 1932

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
  # Remove remaining tokens
  event = event.replace("[[", "")
  event = event.replace("]]", "")
  event = event.replace("''", "'")
  event = event.replace("  ", " ")
  return event

def getFormattedDate (text):
  dateRegex = re.compile("^\[{2}([a-zA-Z]*?) ([0-9]+)\]{2}", re.M)
  # Get data from text
  date = re.search(dateRegex, text)
  # Format date depending on regex match
  if date:
    date = date.group(2) + " " + date.group(1) + " " + str(year)
  else:
    date = str(year)
  return date

def getEventsFromMultilineDate ( eventType, dateText ):
  date = getFormattedDate(dateText[1])
  events = re.findall("^\*{2}(.*)$", dateText[0], re.M)
  formattedEventsList = []
  for event in events:
    formattedEventsList.append(getFormattedEvent(eventType, date, event))
  return formattedEventsList

def formatData ( data ):
  events = []
  #Remove mounth from text
  data = re.sub(re.compile("(^={3}[a-zA-Z\s]*={3}$)", re.M), "", data)
  # Sort by events types
  results = re.findall("(^={2}[a-zA-Z\s]*={2}$)(.*?)(?=(?:^={2}[a-zA-Z\s]*={2}$)|\Z)", data, re.S|re.M)
  for match in results:
    eventType = match[0].replace("=", "").lower()
    eventData = re.sub(re.compile("^(?!\*)(.*)$", re.M), '', match[1])

    if any(eventType in s for s in config['formatting']['typesHandled']):
      # Format multiline date events
      multilineRegex = re.compile("(?P<full_match>^\*{1} (.*)\n(^\*{2}(.*?)\n)+)", re.M)
      multilineDates = re.findall(multilineRegex, eventData)
      eventData = re.sub(multilineRegex, "", eventData)
      for el in multilineDates:
        for item in getEventsFromMultilineDate(eventType, el):
          events.append(item)

      # Format single lined events
      singlelineEvent = re.findall("^\* (.+?)$", eventData, re.M)
      for el in singlelineEvent:
        events.append(getFormattedEvent( eventType, getFormattedDate(el), re.sub(r"^\[{2}[a-zA-Z]*?\s[0-9]+\]{2}\s–\s", "", el)))
  return events

# Get and format data
eventList = formatData(getYearData(year))

for item in eventList:
  logFile.write("%s\n" % item)

logFile.close()