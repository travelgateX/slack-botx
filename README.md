[![Build Status](https://travis-ci.org/travelgateX/slack-botx.svg?branch=master)](https://travis-ci.org/travelgateX/slack-botx)

Bot for [TravelgateX Slack](https://travelgatex.slack.com) 

## Features

* Based on slack [Real Time Messaging API](https://api.slack.com/rtm)

## Install requirements
```
pip install -r requirements.txt
```

## Environment
Modify slackbot/config.ini or set environment:

```
export SLACK_API_TOKEN="xoxb-your-token"
export SLACK_VERIFICATION_TOKEN="xoxv-your-token"
```

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


# Runbook
- Create heroku app
- 