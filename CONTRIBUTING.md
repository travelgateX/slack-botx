# Contributing

1. Open a [new issue][] to discuss the changes you would like to make.  This is
   not strictly required but it may help reduce the amount of rework you need
   to do later.
1. Make changes to `app` or contribute with new commands or events:
   - [Events](event-development)
   - [Commands](command-development)
1. Ensure you have added proper tests and documentation.
1. Open a new [pull request][].

## Common development tasks

These contributions goes under `contrib` folder using [Python plugins discovery](https://packaging.python.org/guides/creating-and-discovering-plugins/)

### Event development

Manage [Slack Event API](https://api.slack.com/events-api) event loop.
You can view an Event sample [here](https://github.com/travelgateX/slack-botx/blob/master/contrib/plugins/events/team_join.py)

1. Ask to your Slack Admin to subscribe the event do you plan to develop. Event must be compatible with Event API as described [here](https://api.slack.com/events)
1. Under `contrib/plugins/events` create a file named _event name_
1. Create a class named _Task_ inherit from class _Event_
1. Hack the _abstract methods_ required

### Command development

Response to [Slash Commands](https://api.slack.com/slash-commands).
You can view an Command sample [here](https://github.com/travelgateX/slack-botx/blob/master/contrib/plugins/commands/alertsx.py)

1. Ask to your Slack Admin to create the new command do you plan to develop as described [here](https://api.slack.com/slash-commands#creating_commands)
1. Under `contrib/plugins/commands` create a file named _command name_
1. Create a class named _Task_ inherit from class _Command_
1. Hack the _abstract methods_ required

[new issue]: https://github.com/travelgateX/slack-botx/issues/new
[pull request]: https://github.com/travelgateX/slack-botx/compare
