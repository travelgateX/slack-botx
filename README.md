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

[TravelgateX Slack](https://travelgatex.slack.com) bot written in Python:

* Based on [Slack Events](https://api.slack.com/events-api)
* Powered by [FastAPI web framework](https://fastapi.tiangolo.com/)
* Using standard [Python 3.7+ type hints](https://docs.python.org/3/library/typing.html)
* Event background execution.

## Features

* [x] Welcome and onboard new members providing support resources
* [ ] Interactive commands wrapping [TravelgateX GraphQL API](https://api.travelgatex.com)
* [ ] User answers to __very simple__ support questions

## Development

### Environment

Modify app/config.ini or set environment variables:

```bash
export SLACK_BOT_TOKEN="xoxb-your-token"
export SLACK_SIGNING_SECRET="your-signing-secret"
```

### Dependencies

```bash
pip install -r requirements.txt
```

## Run

### Local

Run the server with:

```bash
uvicorn app.main:app --reload
```

### Docker

Build the image and run the container

```bash
docker build -t myimage .
docker run -d --name mycontainer -p 80:80 myimage
```

## Tests

```bash
pytest
```

## Cloud deployment

### Heroku

Heroku [deployment url](https://slack-botx.herokuapp.com/)

