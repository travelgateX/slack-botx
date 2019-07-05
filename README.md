<p>
<a href="https://travis-ci.org/travelgateX/slack-botx" target="_blank">
    <img src="https://travis-ci.org/travelgateX/slack-botx.svg?branch=master" alt="Build Status">
</a>
<a href="https://codecov.io/gh/travelgateX/slack-botx" target="_blank">
    <img src="https://codecov.io/gh/travelgateX/slack-botx/branch/master/graph/badge.svg" alt="Coverage">
</a>
<a href="https://slack.travelgatex.com" target="_blank">
    <img src="https://slack.travelgatex.com/badge.svg" alt="Slack">
</a>
</p>


## Features
[TravelgateX Slack](https://travelgatex.slack.com) bot written in Python.

The key features are:

* Based on slack [Events API](https://api.slack.com/events-api)
* Powered by [FastAPI web framework](https://fastapi.tiangolo.com/)

## Requirements

Python 3.7+

### Dependencies

```bash
pip install -r requirements.txt
```

## Environment

Modify app/config.ini or set environment variables:

```bash
export SLACK_BOT_TOKEN="xoxb-your-token"
export SLACK_SIGNING_SECRET="your-signing-secret"
```

## Run

### Local

Start the server

```bash
uvicorn app.main:app --reload
```

## Tests

```bash
pytest
```

### Docker

Build the image and run the container

```bash
docker build -t myimage .
docker run -d --name mycontainer -p 80:80 myimage
```

## Heroku

Heroku [deployment url](https://slack-botx.herokuapp.com/)