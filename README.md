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
* Powered by [FastAPI web framework](https://fastapi.tiangolo.com)
* Using standard [Python 3.7+ type hints](https://docs.python.org/3/library/typing.html)
* Easy to contribute using standard [Plugins Ecosystem](https://packaging.python.org/guides/creating-and-discovering-plugins/)
* Easy background execution with [Starlette Background Tasks](https://www.starlette.io/background)
* Complex background execution with [Apache Airflow](https://airflow.apache.org/)
* Command help with [Python commandline argparse](https://docs.python.org/3/library/argparse.html)

## Features

* Respond to Slack Events API:
  * [x] team_join:
    * Welcome and onboard new members providing support resources 
* Interactive commands wrapping [TravelgateX GraphQL API](https://api.travelgatex.com)
  * [x] `alertsx`
    * Status
  * [ ] Insights-X
* Advise on external events
  * [x] [OnWebChange](https://onwebchange.com)
    * Advise on changelog updates
* User answers to __very simple__ questions (aka Chatbot)
  * [ ] Common support questions

## Requirements

Requires Python 3.7+

```bash
pip install -r requirements.txt
```

## Development

### Environment

Modify app/config.ini and/or set environment variables:

* Linux

```bash
export SLACK_BOT_TOKEN="xoxb-your-token"
export SLACK_SIGNING_SECRET="your-signing-secret"
export TRAVELGATEX_GRAPHQL_API_KEY="your-travelgatex-api-key"
```

* Windows

```bash
set SLACK_BOT_TOKEN=xoxb-your-token
set SLACK_SIGNING_SECRET=your-signing-secret
set TRAVELGATEX_GRAPHQL_API_KEY=your-travelgatex-api-key
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

* [Heroku deployment url](https://slack-botx.herokuapp.com/)

## Contributing

Refer to [CONTRIBUTING.md](https://github.com/travelgateX/slack-botx/blob/master/CONTRIBUTING.md)
