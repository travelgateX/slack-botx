[![PyPI](https://badge.fury.io/py/slackbot.svg)](https://pypi.python.org/pypi/slackbot) [![Build Status](https://secure.travis-ci.org/lins05/slackbot.svg?branch=master)](http://travis-ci.org/lins05/slackbot)

Bot for [TravelgateX Slack](https://travelgatex.slack.com) 

## Features

* Based on slack [Real Time Messaging API](https://api.slack.com/rtm)

## Install requirements
```
pip install -r requirements.txt
```

## Environemnt
Modify slackbot/config.ini or set environment:

export SLACK_API_TOKEN="xoxb-your-token"
export SLACK_VERIFICATION_TOKEN="xoxv-your-token"


### Schedule messages

```

python scheduled.py

```

### Slash Commands
Start the server
```
uvicorn main:app --reload
```

### Docker
Build the image and run the container
```
docker build -t myimage .
docker run -d --name mycontainer -p 80:80 myimage
```


#Runbook
- Create heroku app
- 